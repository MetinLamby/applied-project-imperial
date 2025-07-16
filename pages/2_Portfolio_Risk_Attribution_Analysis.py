import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit

############### PART 2: FACTOR ZOO AND PORTFOLIO RETURNS ###############


if "portfolio_daily_prices" in st.session_state and "portfolio_weights" in st.session_state:
    weights = st.session_state.portfolio_weights
    prices_df = st.session_state.portfolio_daily_prices
    # reset the index of prices_df to ensure 'Date' is a column
    prices_df.reset_index(inplace=True)
    prices_df['Date'] = pd.to_datetime(prices_df['Date'])

    try:
        factors = pd.read_csv('factorZoo.csv')

        # Ensure 'Date' column is datetime
        factors['Date'] = pd.to_datetime(factors['Date'], format='%Y%m%d')

        filtered_prices_df = prices_df[prices_df['Date'].isin(factors['Date'])].copy()


        filtered_prices_df

        # Extract asset columns (exclude 'Date')
        asset_cols = [col for col in filtered_prices_df.columns if col != 'Date']

        # Convert weights dataframe to Series, aligned to asset columns
        weights = weights.reindex(asset_cols)

        # Calculate returns
        price_data = filtered_prices_df.set_index('Date')[asset_cols]
        asset_returns = price_data.pct_change().dropna()

        # Calculate portfolio returns
        portfolio_returns = asset_returns.dot(weights)

        # Create new dataframe with portfolio returns
        portfolio_returns_df = pd.DataFrame({
            'Date': portfolio_returns.index,
            'Return': portfolio_returns.values
        })

        # merge portfolio_returns_df and factors in Date column
        return_factor_df = portfolio_returns_df.merge(factors, on='Date', how='left')
        st.session_state.return_factor_df = return_factor_df

        return_factor_df

    except FileNotFoundError:
        st.warning("factorZoo.csv file not found. Please upload it to the app directory.")
