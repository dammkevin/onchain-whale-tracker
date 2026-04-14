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


def shorten_address(address, left=6, right=4):
    if not address or len(address) < (left + right):
        return address
    return f"{address[:left]}...{address[-right:]}"


def format_transaction_type(transaction_type):
    if transaction_type == "erc20_transfer":
        return "ERC-20"
    if transaction_type == "eth_transfer":
        return "ETH"
    return transaction_type


def prepare_display_dataframe(df):
    display_df = df.copy()

    display_df["transaction_type"] = display_df["transaction_type"].apply(format_transaction_type)
    display_df["from_address"] = display_df["from_address"].apply(shorten_address)
    display_df["to_address"] = display_df["to_address"].apply(shorten_address)

    display_df = display_df.rename(columns={
        "readable_time": "Time",
        "token_symbol": "Token",
        "token_name": "Token Name",
        "transaction_type": "Transaction Type",
        "token_amount": "Amount",
        "usd_value": "USD Value",
        "from_address": "From",
        "to_address": "To",
        "signal": "Signal",
        "tx_hash": "Transaction Hash",
    })

    display_df = display_df[
        [
            "Time",
            "Token",
            "Transaction Type",
            "Amount",
            "USD Value",
            "From",
            "To",
            "Signal",
            "Transaction Hash",
        ]
    ]

    return display_df


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

    total_transactions = len(filtered_df)
    total_usd_value = filtered_df["usd_value"].sum() if not filtered_df.empty else 0.0
    largest_transaction = filtered_df["usd_value"].max() if not filtered_df.empty else 0.0
    eth_count = len(filtered_df[filtered_df["transaction_type"] == "eth_transfer"])
    erc20_count = len(filtered_df[filtered_df["transaction_type"] == "erc20_transfer"])

    st.subheader("Summary Metrics")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Transactions", f"{total_transactions:,}")
    col2.metric("Total USD Value", f"${total_usd_value:,.2f}")
    col3.metric("Largest Transaction", f"${largest_transaction:,.2f}")
    col4.metric("ETH Transfers", f"{eth_count:,}")
    col5.metric("ERC-20 Transfers", f"{erc20_count:,}")

    st.subheader("Whale Transactions")
    st.write(f"Showing {len(filtered_df)} transaction(s)")

    display_df = prepare_display_dataframe(filtered_df)

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
    )


if __name__ == "__main__":
    main()
