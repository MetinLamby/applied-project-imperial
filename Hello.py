import streamlit as st

st.set_page_config(
    page_title="Landing Page",
    page_icon="⚙️",
)

st.write("# Equity Portfolio Risk Analysis App")

st.markdown(
    """
    This is the app I developed as part of my applied project at Imperial College London Business School.
    """
)

st.subheader("Set up your portfolio for analysis", divider="gray")
st.page_link("pages/1_Initialise_Portfolio.py", label="Lets get started", icon="➡️")


st.markdown(
    """
    ### Want to learn more about the project?
    - Check out the related repo on [GitHub](https://github.com/MetinLamby/applied-project-imperial)
    - Read the applied project [pdf](https://github.com/MetinLamby/applied-project-imperial/blob/main/README.md)
    - Watch the app [tutorial](https://github.com/MetinLamby/applied-project-imperial/blob/main/README.md)
    """
)