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
        "Explore detected whale transactions with interactive filtering."
    )

    df = load_data()

    if df.empty:
        st.warning("No whale transactions found in the database.")
        return

    st.sidebar.header("Filters")

    selected_tokens = st.sidebar.multiselect(
        "Token",
        options=sorted(df["token_symbol"].unique()),
        default=sorted(df["token_symbol"].unique())
    )

    selected_transaction_types = st.sidebar.multiselect(
        "Transaction Type",
        options=sorted(df["transaction_type"].unique()),
        default=sorted(df["transaction_type"].unique())
    )

    selected_signals = st.sidebar.multiselect(
        "Signal",
        options=sorted(df["signal"].unique()),
        default=sorted(df["signal"].unique())
    )

    min_usd_value = st.sidebar.number_input(
        "Minimum USD Value",
        min_value=0.0,
        value=10000.0,
        step=1000.0
    )

    filtered_df = df[
        (df["token_symbol"].isin(selected_tokens)) &
        (df["transaction_type"].isin(selected_transaction_types)) &
        (df["signal"].isin(selected_signals)) &
        (df["usd_value"] >= min_usd_value)
    ]

    st.subheader("Whale Transactions")
    st.write(f"Showing {len(filtered_df)} transaction(s)")

    st.dataframe(filtered_df, width="stretch")


if __name__ == "__main__":
    main()
