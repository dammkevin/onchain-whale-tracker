from app.config import WATCHED_ADDRESSES
from app.fetcher import fetch_erc20_transfers_for_address, fetch_token_prices_usd
from app.processor import normalize_and_filter_supported_tokens
from app.filters import filter_whale_transactions
from app.analyzer import attach_signal
from app.storage import init_db, save_transactions
from app.utils import print_transaction


def main():
    init_db()

    all_raw_transfers = []

    for address in WATCHED_ADDRESSES:
        print(f"Fetching transfers for watched address: {address}")
        raw_transfers = fetch_erc20_transfers_for_address(address, offset=100, page=1)
        all_raw_transfers.extend(raw_transfers)

    if not all_raw_transfers:
        print("No transfers found.")
        return

    contract_addresses = [
        tx.get("contractAddress", "").lower()
        for tx in all_raw_transfers
        if tx.get("contractAddress")
    ]

    price_lookup = fetch_token_prices_usd(contract_addresses)

    normalized_transactions = normalize_and_filter_supported_tokens(all_raw_transfers, price_lookup)
    whale_transactions = filter_whale_transactions(normalized_transactions)
    whale_transactions = attach_signal(whale_transactions)

    if not whale_transactions:
        print("No whale transactions found for the current threshold.")
        return

    save_transactions(whale_transactions)

    print(f"\nFound {len(whale_transactions)} whale transaction(s):\n")
    for tx in whale_transactions:
        print_transaction(tx)


if __name__ == "__main__":
    main()
