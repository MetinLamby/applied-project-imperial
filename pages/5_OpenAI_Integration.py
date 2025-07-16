import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
import openai



st.title("📈 Open AI Part")

# Define data
data = {
    'Factor': ['MktRf', 'SMB', 'ww', 'ato', 'os', 'ta', 'mve_ia', 'cfp_ia', 'IPO', 'dnco', 'ms',
               'mom6m', 'std_dolvol', 'LIQ_PS', 'chempia'],
    'Coef': [0.042774, -0.004119, 0.000950, 0.000439, 0.000337, 0.000305, -0.000278, 0.000161,
             -0.000145, 0.000126, 0.000097, -0.000071, -0.000030, 0.000018, 0.000003],
    'Description': ['Excess Market Return', 'Small Minus Big', 'Whited-Wu Index', 'Asset turnover',
                    'OhlsonÕs O-score', 'Total accruals', 'Industry-adjusted size',
                    'Industry-adjusted cash flow to price ratio', 'New equity issue',
                    'Change in Net Noncurrent Operating Assets', 'Financial statements performance',
                    '6-month momentum', 'Volatility of liquidity (dollar trading volume)',
                    'Liquidity', 'Industry-adjusted change in employees']
}

# Create DataFrame
df = pd.DataFrame(data)

df

# Set your OpenAI API key safely (you can also use st.secrets for production)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Example: merged_with_descriptions DataFrame is already loaded in session_state
if df is not None:

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
