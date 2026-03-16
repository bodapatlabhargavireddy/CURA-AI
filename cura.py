import streamlit as st

st.set_page_config(page_title="Cura AI - Setup", layout="centered")

st.title("🛡️ Setup Your Health Profile")

# Using 'key' is mandatory so the Dashboard can see these values
st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, key="weight")
st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, key="height")
st.number_input("Age", min_value=10, max_value=100, value=25, key="age")
st.selectbox("Gender", ["Male", "Female"], key="gender")
st.selectbox("Goal", ["Maintenance", "Weight Loss", "Weight Gain"], key="goal")
st.selectbox("Cuisine Preference", ["Indian", "Continental", "Mediterranean"], key="cuisine")

if st.button("Go to Dashboard 🚀"):
    st.switch_page("pages/4_Dashboard.py")
