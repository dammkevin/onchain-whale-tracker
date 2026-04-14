from app.config import KNOWN_EXCHANGE_WALLETS


def shorten_address(address, left=6, right=4):
    if not address or len(address) < (left + right):
        return address
    return f"{address[:left]}...{address[-right:]}"


def label_address(address):
    if not address:
        return address

    name = KNOWN_EXCHANGE_WALLETS.get(address.lower())
    if name:
        return f"{name} ({shorten_address(address)})"

    return shorten_address(address)


def format_transaction_type(transaction_type):
    if transaction_type == "erc20_transfer":
        return "ERC-20 Transfer"
    if transaction_type == "eth_transfer":
        return "Native ETH Transfer"
    return transaction_type


def print_transaction(tx):
    print("=" * 80)
    print(f"Time:             {tx['readable_time']}")
    print(f"Transaction Type: {format_transaction_type(tx['transaction_type'])}")
    print(f"Token:            {tx['token_symbol']} ({tx['token_name']})")
    print(f"Amount:           {tx['token_amount']:,.4f}")
    print(f"USD Value:        ${tx['usd_value']:,.2f}")
    print(f"From:             {label_address(tx['from_address'])}")
    print(f"To:               {label_address(tx['to_address'])}")
    print(f"Hash:             {tx['tx_hash']}")
    print(f"Signal:           {tx['signal']}")
    print("=" * 80)
