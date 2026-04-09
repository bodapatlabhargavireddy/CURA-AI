import streamlit as st

st.set_page_config(page_title="Cura AI", layout="centered")

st.title("🛡️ CURA AI: Integrated Health System")
st.write("Welcome to your personal performance ecosystem.")

# Initialize global data if not already present
if "weight" not in st.session_state:
    st.session_state.weight = 70.0
if "gender" not in st.session_state:
    st.session_state.gender = "Male"

st.info("Please navigate using the sidebar to begin your health assessment.")

if st.button("Start Assessment"):
    st.switch_page("pages/1_Health.py")
