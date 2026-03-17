import streamlit as st

st.title("🛡️ Cura: User Profile")

# We check if weight exists, if not, set a default. This prevents the reset.
if "weight" not in st.session_state:
    st.session_state.weight = 70.0
if "height" not in st.session_state:
    st.session_state.height = 170.0

# By using key="weight", the value is saved globally automatically
st.number_input("Enter Your Weight (kg)", 30.0, 200.0, key="weight")
st.number_input("Enter Your Height (cm)", 100.0, 250.0, key="height")
st.selectbox("Your Goal", ["Weight Loss", "Muscle Gain", "Maintenance"], key="goal")

st.success(f"Current Memory: {st.session_state.weight}kg")

if st.button("Go to Monitor"):
    st.switch_page("pages/3_Monitor.py")
