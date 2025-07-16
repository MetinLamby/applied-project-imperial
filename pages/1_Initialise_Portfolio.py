import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit


# Initialize session state
if "portfolio_items" not in st.session_state:
    st.session_state.portfolio_items = []

if "show_form" not in st.session_state:
    st.session_state.show_form = False

st.title("📈 Equity Portfolio Builder")

# Add portfolio item button
if st.button("➕ Add portfolio item"):
    st.session_state.show_form = True

# Form for ticker + shares
if st.session_state.show_form:
    with st.form("add_item_form", clear_on_submit=True):
        ticker = st.text_input("Ticker symbol")
        shares = st.number_input("Number of shares", min_value=0, step=1)
        submitted = st.form_submit_button("Add Portfolio Item")
        if submitted:
            if ticker and shares > 0:
                st.session_state.portfolio_items.append({"ticker": ticker.upper(), "shares": shares})
                st.success(f"Added {shares} shares of {ticker.upper()}")
            else:
                st.warning("Please provide a valid ticker and number of shares.")



############### PART 1: PORTFOLIO DATA AND WEIGHTS ###############


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

        # if the data is empty, show a warning
        if data.empty:
            st.warning("The Yahoo finance API is down at the moment. or, there is no data found for the selected tickers. Please check the ticker symbols and try again.")

            st.page_link("pages/3_Help_Page.py", label="Help Page", icon="❓")

        else:  
            # Calculate portfolio weights based on shares
            last_prices = data.iloc[-1]
            weights = (last_prices * shares) / (last_prices * shares).sum()

            st.session_state.portfolio_daily_prices = data
            st.session_state.portfolio_weights = weights

            st.page_link("pages/2_Portfolio_Risk_Attribution_Analysis.py", label="Analyse risk factors of my portfolio", icon="✅")

else:
    st.info("Add portfolio items to get started.")

