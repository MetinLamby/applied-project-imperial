'''
# Load factorZoo.csv
try:
    factors = pd.read_csv('factorZoo.csv')

    # Convert 'Date' column to string (if not already)
    factors['Date'] = factors['Date'].astype(str)

    # Convert to datetime format
    factors['Date'] = pd.to_datetime(factors['Date'], format='%Y%m%d')

    st.subheader("🗂️ FactorZoo Data (Sample)")
    st.dataframe(factors.head())

except FileNotFoundError:
    st.warning("factorZoo.csv file not found. Please upload it to the app directory.")
'''