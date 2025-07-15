import streamlit as st
import yfinance as yf
import pandas as pd

# Initialize session state
if "portfolio_items" not in st.session_state:
    st.session_state.portfolio_items = []

if "show_form" not in st.session_state:
    st.session_state.show_form = False

st.title("📈 Portfolio Builder")

# Add portfolio item button
if st.button("➕ Add portfolio item"):
    st.session_state.show_form = True

# Form for ticker + shares
if st.session_state.show_form:
    with st.form("add_item_form", clear_on_submit=True):
        ticker = st.text_input("Ticker symbol")
        shares = st.number_input("Number of shares", min_value=0, step=1)
        submitted = st.form_submit_button("Add")
        if submitted:
            if ticker and shares > 0:
                st.session_state.portfolio_items.append({"ticker": ticker.upper(), "shares": shares})
                st.success(f"Added {shares} shares of {ticker.upper()}")
            else:
                st.warning("Please provide a valid ticker and number of shares.")

# Display portfolio
if st.session_state.portfolio_items:
    st.subheader("📋 Current Portfolio")
    for idx, item in enumerate(st.session_state.portfolio_items):
        st.write(f"{idx + 1}. **{item['ticker']}** — {item['shares']} shares")

    # Finished button
    if st.button("✅ Finished setting up portfolio"):
        st.write("Fetching historical data...")

        # Get tickers and shares
        tickers = [item['ticker'] for item in st.session_state.portfolio_items]
        shares = [item['shares'] for item in st.session_state.portfolio_items]

        # Download adjusted close prices
        data = yf.download(tickers, interval='1d')['Close']

        # Handle single vs multi ticker
        if isinstance(data, pd.Series):
            data = data.to_frame()

        # Calculate daily returns
        returns = data.pct_change().dropna()

        # Calculate portfolio weights based on shares
        last_prices = data.iloc[-1]
        weights = (last_prices * shares) / (last_prices * shares).sum()

        # Calculate weighted portfolio daily returns
        portfolio_returns = returns @ weights

        st.subheader("📊 Portfolio Daily Returns (Last 6 Months)")
        st.line_chart(portfolio_returns)

        st.subheader("🔍 Portfolio Summary")
        st.write("Portfolio weights (based on latest prices):")
        st.write(weights)
else:
    st.info("Add portfolio items to get started.")
