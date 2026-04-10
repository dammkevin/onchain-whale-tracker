from app.config import KNOWN_EXCHANGE_WALLETS


def classify_transaction(tx):
    from_address = tx.get("from_address", "").lower()
    to_address = tx.get("to_address", "").lower()

    from_exchange = KNOWN_EXCHANGE_WALLETS.get(from_address)
    to_exchange = KNOWN_EXCHANGE_WALLETS.get(to_address)

    if from_exchange and not to_exchange:
        return f"Possible withdrawal from {from_exchange} / accumulation"
    if to_exchange and not from_exchange:
        return f"Possible deposit to {to_exchange} / sell pressure"
    if from_exchange and to_exchange:
        return f"Exchange-to-exchange transfer ({from_exchange} -> {to_exchange})"

    return "Large whale transfer"


def attach_signal(transactions):
    for tx in transactions:
        tx["signal"] = classify_transaction(tx)
    return transactions
