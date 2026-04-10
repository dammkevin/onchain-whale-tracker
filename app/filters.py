from app.config import WHALE_THRESHOLD_USD


def is_whale_transaction(tx):
    return tx.get("usd_value", 0) >= WHALE_THRESHOLD_USD


def filter_whale_transactions(transactions):
    return [tx for tx in transactions if is_whale_transaction(tx)]
