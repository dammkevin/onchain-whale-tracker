import os
import sqlite3

DB_PATH = "data/whale_transactions.db"


def init_db():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS whale_transactions (
            tx_hash TEXT PRIMARY KEY,
            block_number INTEGER,
            timestamp INTEGER,
            readable_time TEXT,
            from_address TEXT,
            to_address TEXT,
            contract_address TEXT,
            token_name TEXT,
            token_symbol TEXT,
            token_decimals INTEGER,
            token_amount REAL,
            usd_price REAL,
            usd_value REAL,
            transaction_type TEXT,
            signal TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_transactions(transactions):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for tx in transactions:
        cursor.execute("""
            INSERT OR IGNORE INTO whale_transactions (
                tx_hash,
                block_number,
                timestamp,
                readable_time,
                from_address,
                to_address,
                contract_address,
                token_name,
                token_symbol,
                token_decimals,
                token_amount,
                usd_price,
                usd_value,
                transaction_type,
                signal
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tx["tx_hash"],
            tx["block_number"],
            tx["timestamp"],
            tx["readable_time"],
            tx["from_address"],
            tx["to_address"],
            tx["contract_address"],
            tx["token_name"],
            tx["token_symbol"],
            tx["token_decimals"],
            tx["token_amount"],
            tx["usd_price"],
            tx["usd_value"],
            tx["transaction_type"],
            tx["signal"],
        ))

    conn.commit()
    conn.close()
