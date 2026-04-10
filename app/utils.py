def shorten_address(address, left=6, right=4):
    if not address or len(address) < (left + right):
        return address
    return f"{address[:left]}...{address[-right:]}"


def print_transaction(tx):
    print("=" * 70)
    print(f"Time:   {tx['readable_time']}")
    print(f"Token:  {tx['token_symbol']} ({tx['token_name']})")
    print(f"Amount: {tx['token_amount']:,.4f}")
    print(f"USD:    ${tx['usd_value']:,.2f}")
    print(f"From:   {shorten_address(tx['from_address'])}")
    print(f"To:     {shorten_address(tx['to_address'])}")
    print(f"Hash:   {tx['tx_hash']}")
    print(f"Signal: {tx['signal']}")
    print("=" * 70)
