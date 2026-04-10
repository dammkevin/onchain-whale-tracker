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
    "0x000000000000000000000000000000000000dead",
]

# Basic exchange label placeholders for later interpretation.
# Add real known exchange wallets once you want better classification.
KNOWN_EXCHANGE_WALLETS = {
    # "0xexampleaddress": "Binance",
    # "0xanotherexample": "Coinbase",
}

# Optional: only track these tokens at first.
# Leaving this empty means "allow all tokens returned".
TRACKED_TOKEN_CONTRACTS = set()
