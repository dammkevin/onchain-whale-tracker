import os
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")
COINGECKO_API_MODE = os.getenv("COINGECKO_API_MODE", "demo").lower()
WHALE_THRESHOLD_USD = float(os.getenv("WHALE_THRESHOLD_USD", "100"))

ETHERSCAN_BASE_URL = "https://api.etherscan.io/v2/api"

if COINGECKO_API_MODE == "pro":
    COINGECKO_BASE_URL = "https://pro-api.coingecko.com/api/v3"
else:
    COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

CHAIN_ID = "1"  # Ethereum

# Replace this with real wallet addresses you want to monitor.
WATCHED_ADDRESSES = [
    "0x28C6c06298d514Db089934071355E5743bf21d60"
]

# Known exchange wallet labels for basic signal interpretation
KNOWN_EXCHANGE_WALLETS = {
    # Binance
    "0x28c6c06298d514db089934071355e5743bf21d60": "Binance",

    # Coinbase
    "0x503828976d22510aad0201ac7ec88293211d23da": "Coinbase",

    # Kraken
    "0x267be1c1d684f78cb4f6a176c4911b741e4ffdc0": "Kraken",
}

# Restrict to major supported Ethereum token contracts for cleaner testing.
TRACKED_TOKEN_CONTRACTS = {
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
    "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",  # WETH
    "0x6b175474e89094c44da98b954eedeac495271d0f",  # DAI
}
