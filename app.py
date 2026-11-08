import streamlit as st

st.set_page_config(page_title="Rogue Aerospace Recovery", layout="wide")

st.navigation([
    st.Page("pages/background.py", title="Background"),
    st.Page("pages/parachutes.py", title="Parachutes & Shock Cords"),
    st.Page("pages/ejection.py", title="Ejection Charges"),
]).run()
