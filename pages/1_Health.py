import streamlit as st

st.title("🩺 Health Metrics")

# Using 'key' automatically saves this to st.session_state
st.number_input("Enter Weight (kg):", min_value=30.0, max_value=200.0, value=st.session_state.get("weight", 70.0), key="weight")
st.number_input("Enter Height (cm):", min_value=100, max_value=250, value=st.session_state.get("height", 170.0), key="height")
st.selectbox("Gender:", ["Male", "Female", "Other"], key="gender")

if st.button("Save & Next"):
    st.switch_page("pages/2_Goals.py")
