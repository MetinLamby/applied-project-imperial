import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit



############### PART 4: LASSO COEFFICIENTS AND DESCRIPTION ###############


if "lasso_coefficients" in st.session_state:
    lasso_coefs = st.session_state.lasso_coefficients

    try:
        factors_descriptions = pd.read_csv('factor_descriptions.csv', encoding='latin1', sep=";")

        merged_with_descriptions = pd.merge(lasso_coefs, factors_descriptions, on="Factor", how="left")

        # Display the result
        st.session_state.lasso_coefficients_desciptions = merged_with_descriptions


    except FileNotFoundError:
        st.warning("factorZoo.csv file not found. Please upload it to the app directory.")