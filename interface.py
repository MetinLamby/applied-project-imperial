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

        st.subheader("📊 Portfolio Daily Returns")
        st.line_chart(portfolio_returns)

        st.session_state.portfolio_daily_prices = data
        st.session_state.portfolio_weights = weights
else:
    st.info("Add portfolio items to get started.")


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


    except FileNotFoundError:
        st.warning("factorZoo.csv file not found. Please upload it to the app directory.")


if "return_factor_df" in st.session_state:
    df = st.session_state.return_factor_df

    # Drop rows with NaN
    df_clean = df.dropna()

    # Check necessary columns exist
    required_columns = ['Date', 'RF', 'Return']
    if not all(col in df_clean.columns for col in required_columns):
        st.error("The dataframe must include 'Date', 'RF', and 'Return' columns.")
    else:
        # Prepare X and y
        X = df_clean.drop(columns=['Date', 'RF', 'Return']).values
        y = df_clean['Return'].values

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Time series split setup
        tscv = TimeSeriesSplit(n_splits=5)

        # LassoCV with time series split
        lasso = LassoCV(cv=tscv)

        # Fit model
        lasso.fit(X_scaled, y)

        # Show best alpha
        st.write(f"Best alpha selected by LassoCV: {lasso.alpha_}")

        # Create and display coefficients
        coef = pd.Series(lasso.coef_, index=df_clean.drop(columns=['Date', 'RF', 'Return']).columns)

        # Sort by absolute value (largest effect first)
        coef_sorted = coef.reindex(coef.abs().sort_values(ascending=False).index)

        # Optionally: show only non-zero coefficients
        non_zero_coef = coef_sorted[coef_sorted != 0]
        nonzero_coefs_df = pd.DataFrame({
            'Factor': non_zero_coef.index,
            'Coef': non_zero_coef.values
        })

        st.session_state.lasso_coefficients = nonzero_coefs_df


if "lasso_coefficients" in st.session_state:
    lasso_coefs = st.session_state.lasso_coefficients

    try:
        factors_descriptions = pd.read_csv('factor_descriptions.csv', encoding='latin1', sep=";")

        merged_with_descriptions = pd.merge(lasso_coefs, factors_descriptions, on="Factor", how="left")

        # Display the result
        st.session_state.lasso_coefficients_desciptions = merged_with_descriptions


    except FileNotFoundError:
        st.warning("factorZoo.csv file not found. Please upload it to the app directory.")


if "lasso_coefficients_desciptions" in st.session_state:
    lasso_coefs_with_desc = st.session_state.lasso_coefficients_desciptions

    lasso_coefs_with_desc

    # NOW USE OPENAI API