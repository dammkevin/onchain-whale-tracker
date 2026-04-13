from app.config import WATCHED_ADDRESSES
from app.fetcher import (
    fetch_erc20_transfers_for_address,
    fetch_eth_transfers_for_address,
    fetch_token_prices_usd,
    fetch_eth_price_usd,
)
from app.processor import (
    normalize_and_filter_supported_tokens,
    normalize_eth_transfers,
)
from app.filters import filter_whale_transactions
from app.analyzer import attach_signal
from app.storage import init_db, save_transactions
from app.utils import print_transaction


def main():
    init_db()

    all_raw_erc20_transfers = []
    all_raw_eth_transfers = []

    for address in WATCHED_ADDRESSES:
        print(f"Fetching ERC-20 transfers for watched address: {address}")
        raw_erc20 = fetch_erc20_transfers_for_address(address, offset=1000, page=1)
        print(f"Found {len(raw_erc20)} raw ERC-20 transfer(s) for {address}")
        all_raw_erc20_transfers.extend(raw_erc20)

        print(f"Fetching native ETH transfers for watched address: {address}")
        raw_eth = fetch_eth_transfers_for_address(address, offset=1000, page=1)
        print(f"Found {len(raw_eth)} raw ETH transaction(s) for {address}")
        all_raw_eth_transfers.extend(raw_eth)

    if not all_raw_erc20_transfers and not all_raw_eth_transfers:
        print("No transfers found at all.")
        return

    contract_addresses = [
        tx.get("contractAddress", "").lower()
        for tx in all_raw_erc20_transfers
        if tx.get("contractAddress")
    ]

    price_lookup = fetch_token_prices_usd(contract_addresses)
    eth_price_usd = fetch_eth_price_usd()

    normalized_erc20_transactions = normalize_and_filter_supported_tokens(
        all_raw_erc20_transfers,
        price_lookup
    )
    normalized_eth_transactions = normalize_eth_transfers(
        all_raw_eth_transfers,
        eth_price_usd
    )

    print(f"Normalized {len(normalized_erc20_transactions)} ERC-20 transaction(s)")
    print(f"Normalized {len(normalized_eth_transactions)} ETH transaction(s)")

    all_normalized_transactions = normalized_erc20_transactions + normalized_eth_transactions

    if not all_normalized_transactions:
        print("No normalized transactions found.")
        return

    sorted_transactions = sorted(
        all_normalized_transactions,
        key=lambda tx: tx["usd_value"],
        reverse=True
    )

    print("\nTop 10 transactions by USD value:")
    for tx in sorted_transactions[:10]:
        print(
            tx["token_symbol"],
            "| type:", tx["transaction_type"],
            "| amount:", tx["token_amount"],
            "| usd_price:", tx["usd_price"],
            "| usd_value:", tx["usd_value"]
        )

    whale_transactions = filter_whale_transactions(all_normalized_transactions)
    print(f"\n{len(whale_transactions)} transaction(s) passed the whale threshold")

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
