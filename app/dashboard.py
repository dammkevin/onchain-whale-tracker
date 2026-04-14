import sqlite3
import pandas as pd
import streamlit as st


DB_PATH = "data/whale_transactions.db"


def load_data():
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        readable_time,
        token_symbol,
        token_name,
        transaction_type,
        token_amount,
        usd_value,
        from_address,
        to_address,
        signal,
        tx_hash
    FROM whale_transactions
    ORDER BY timestamp DESC
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def main():
    st.set_page_config(page_title="On-Chain Whale Tracker", layout="wide")

    st.title("On-Chain Whale Tracker Dashboard")
    st.markdown(
        "This dashboard displays detected whale transactions stored in the SQLite database."
    )

    df = load_data()

    if df.empty:
        st.warning("No whale transactions found in the database.")
        return

    st.subheader("Whale Transactions")
    st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    main()
