import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit

############### PART 3: LASSO REGRESSION ###############


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