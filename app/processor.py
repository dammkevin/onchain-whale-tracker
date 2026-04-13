from datetime import datetime, UTC
from app.config import TRACKED_TOKEN_CONTRACTS


def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def convert_raw_amount(raw_value, decimals):
    raw_int = safe_int(raw_value, 0)
    decimals_int = safe_int(decimals, 0)

    if decimals_int < 0:
        decimals_int = 0

    return raw_int / (10 ** decimals_int) if decimals_int else float(raw_int)


def normalize_transfer(raw_tx, price_lookup):
    contract_address = raw_tx.get("contractAddress", "").lower()
    token_symbol = raw_tx.get("tokenSymbol", "UNKNOWN")
    token_name = raw_tx.get("tokenName", "Unknown Token")
    token_decimals = raw_tx.get("tokenDecimal", "0")
    from_address = raw_tx.get("from", "").lower()
    to_address = raw_tx.get("to", "").lower()

    token_amount = convert_raw_amount(raw_tx.get("value", "0"), token_decimals)
    usd_price = price_lookup.get(contract_address, {}).get("usd", 0)
    usd_value = token_amount * float(usd_price)

    timestamp = safe_int(raw_tx.get("timeStamp"))
    readable_time = datetime.fromtimestamp(timestamp, UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

    return {
        "tx_hash": raw_tx.get("hash", ""),
        "block_number": safe_int(raw_tx.get("blockNumber")),
        "timestamp": timestamp,
        "readable_time": readable_time,
        "from_address": from_address,
        "to_address": to_address,
        "contract_address": contract_address,
        "token_name": token_name,
        "token_symbol": token_symbol,
        "token_decimals": safe_int(token_decimals),
        "token_amount": token_amount,
        "usd_price": float(usd_price),
        "usd_value": usd_value,
        "transaction_type": "erc20_transfer",
    }


def normalize_eth_transfer(raw_tx, eth_price_usd):
    """
    Normalize a native ETH transaction into the same general structure
    used by ERC-20 transfers.
    """
    from_address = raw_tx.get("from", "").lower()
    to_address = raw_tx.get("to", "").lower()

    token_amount = convert_raw_amount(raw_tx.get("value", "0"), 18)
    usd_value = token_amount * float(eth_price_usd)

    timestamp = safe_int(raw_tx.get("timeStamp"))
    readable_time = datetime.fromtimestamp(timestamp, UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

    return {
        "tx_hash": raw_tx.get("hash", ""),
        "block_number": safe_int(raw_tx.get("blockNumber")),
        "timestamp": timestamp,
        "readable_time": readable_time,
        "from_address": from_address,
        "to_address": to_address,
        "contract_address": "eth",
        "token_name": "Ethereum",
        "token_symbol": "ETH",
        "token_decimals": 18,
        "token_amount": token_amount,
        "usd_price": float(eth_price_usd),
        "usd_value": usd_value,
        "transaction_type": "eth_transfer",
    }


def normalize_and_filter_supported_tokens(raw_transfers, price_lookup):
    normalized = []

    for tx in raw_transfers:
        contract_address = tx.get("contractAddress", "").lower()

        if TRACKED_TOKEN_CONTRACTS and contract_address not in TRACKED_TOKEN_CONTRACTS:
            continue

        normalized.append(normalize_transfer(tx, price_lookup))

    return normalized


def normalize_eth_transfers(raw_eth_transfers, eth_price_usd):
    normalized = []

    for tx in raw_eth_transfers:
        if safe_int(tx.get("value", "0")) == 0:
            continue

        normalized.append(normalize_eth_transfer(tx, eth_price_usd))

    return normalized
