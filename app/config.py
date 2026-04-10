import os
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")
COINGECKO_API_MODE = os.getenv("COINGECKO_API_MODE", "demo").lower()
WHALE_THRESHOLD_USD = float(os.getenv("WHALE_THRESHOLD_USD", "100000"))

ETHERSCAN_BASE_URL = "https://api.etherscan.io/v2/api"

if COINGECKO_API_MODE == "pro":
    COINGECKO_BASE_URL = "https://pro-api.coingecko.com/api/v3"
else:
    COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

CHAIN_ID = "1"  # Ethereum

# Start with addresses you want to monitor.
# Replace these placeholders with real wallet addresses later.
WATCHED_ADDRESSES = [
    "0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97",
]

# Basic exchange label placeholders for later interpretation.
# Add real known exchange wallets once you want better classification.
KNOWN_EXCHANGE_WALLETS = {
    # "0xexampleaddress": "Binance",
    # "0xanotherexample": "Coinbase",
}

# Optional: only track these tokens at first.
# Leaving this empty means "allow all tokens returned".
TRACKED_TOKEN_CONTRACTS = {
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
    "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",  # WETH
    "0x6b175474e89094c44da98b954eedeac495271d0f",  # DAI
}
