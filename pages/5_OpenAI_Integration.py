import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
import openai



st.title("📈 Open AI Part")


if "lasso_coefficients_desciptions" in st.session_state:
    lasso_coefs_with_desc = st.session_state.lasso_coefficients_desciptions

    df = lasso_coefs_with_desc

    # NOW USE OPENAI API

    # Set your OpenAI API key safely (you can also use st.secrets for production)
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    # Example: merged_with_descriptions DataFrame is already loaded in session_state
    if lasso_coefs_with_desc is not None:

        # Prepare the summary text
        summary = "I ran a Lasso regression to test which factors explain asset returns.\n"
        summary += "Here are the factors and coefficients:\n"
        for _, row in df.iterrows():
            summary += f"- {row['Factor']} ({row['Description']}): Coef = {row['Coef']:.6f}\n"

        # Compose the OpenAI prompt
        prompt = (
            "You are a financial analyst. Please write a clear and human-readable interpretation "
            "of the following Lasso regression results on asset returns. Explain which factors appear useful "
            "based on their coefficients, and what this might mean for explaining asset returns.\n\n"
            + summary
        )

        # Button to trigger the interpretation
        if st.button("Generate Interpretation with OpenAI"):
            with st.spinner("Generating interpretation..."):
                try:
                    client = openai.OpenAI()
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a financial analyst who explains technical regression results in plain English."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.2,
                    )

                    # Extract the interpretation
                    interpretation = response.choices[0].message.content

                    # Display result in Streamlit
                    st.subheader("💬 Interpretation from OpenAI")
                    st.write(interpretation)

                except Exception as e:
                    st.error(f"Error while generating interpretation: {e}")
