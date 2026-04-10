import requests
from app.config import (
    ETHERSCAN_API_KEY,
    ETHERSCAN_BASE_URL,
    CHAIN_ID,
    COINGECKO_API_KEY,
    COINGECKO_API_MODE,
    COINGECKO_BASE_URL,
)


def fetch_erc20_transfers_for_address(address, offset=100, page=1, startblock=0, endblock=9999999999):
    """
    Fetch recent ERC-20 transfers for a single Ethereum address from Etherscan.
    """
    params = {
        "chainid": CHAIN_ID,
        "module": "account",
        "action": "tokentx",
        "address": address,
        "startblock": startblock,
        "endblock": endblock,
        "page": page,
        "offset": offset,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY,
    }

    response = requests.get(ETHERSCAN_BASE_URL, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()

    # Etherscan often returns status/message/result even on no results.
    if "result" not in data:
        return []

    if isinstance(data["result"], list):
        return data["result"]

    return []


def fetch_token_prices_usd(contract_addresses):
    """
    Fetch USD prices from CoinGecko using token contract addresses on Ethereum.
    Returns a dict like:
    {
        "0x...": {"usd": 1.0},
        ...
    }
    """
    if not contract_addresses:
        return {}

    unique_addresses = sorted({addr.lower() for addr in contract_addresses if addr})
    joined_addresses = ",".join(unique_addresses)

    url = f"{COINGECKO_BASE_URL}/simple/token_price/ethereum"
    params = {
        "contract_addresses": joined_addresses,
        "vs_currencies": "usd",
    }

    headers = {}
    if COINGECKO_API_MODE == "pro":
        headers["x-cg-pro-api-key"] = COINGECKO_API_KEY
    else:
        headers["x-cg-demo-api-key"] = COINGECKO_API_KEY

    response = requests.get(url, params=params, headers=headers, timeout=20)
    response.raise_for_status()

    return response.json()
