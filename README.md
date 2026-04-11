## On-Chain Whale Tracker

### Overview
The On-Chain Whale Tracker is a Python-based tool that monitors large cryptocurrency wallet activity on the Ethereum blockchain. It focuses on detecting high-value token transfers ("whale activity") and providing insights into potential market signals.

---

### Version 1 Scope
Version 1 is designed as a **watched-wallet ERC-20 whale tracker**.

It monitors a manually selected list of Ethereum wallet addresses, fetches recent ERC-20 token transfers, enriches them with USD pricing, and flags transactions that exceed a configurable whale threshold.

---

### Features
- Fetches ERC-20 transfer data using Etherscan API  
- Tracks selected Ethereum wallet addresses  
- Filters for major tokens (USDC, USDT, WETH, DAI)  
- Converts raw blockchain values into readable token amounts  
- Enriches transactions with USD pricing via CoinGecko  
- Identifies whale transactions based on USD thresholds  
- Outputs readable transaction summaries in the terminal  
- Stores detected whale transactions in SQLite  

---

### Limitations (Current Version)
- Does not scan the full Ethereum network  
- Does not track native ETH transfers  
- Does not decode swaps or classify buys/sells  
- Requires manually selected wallet addresses  
- Not a real-time monitoring system  

---

### Key Insight
This project focuses on **analyzing wallet-specific whale activity**, not full on-chain market scanning. The accuracy and usefulness depend on the selected wallet addresses and token filters.

---

### Tech Stack
- Python  
- Etherscan API  
- CoinGecko API  
- SQLite  