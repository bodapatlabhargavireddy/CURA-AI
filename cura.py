import streamlit as st

st.set_page_config(page_title="Cura AI", layout="centered")

st.title("🛡️ CURA AI: Integrated Health System")
st.write("Welcome to your personal performance ecosystem. Please enter your metrics below.")

# --- BIOLOGICAL PROFILE ONLY ---
st.subheader("👤 Biological Profile")

col1, col2 = st.columns(2)

with col1:
    # Capturing Weight and Height with keys for data persistence
    st.number_input("Weight (kg):", min_value=10.0, max_value=300.0, value=70.0, step=0.1, key="weight")
    st.number_input("Height (cm):", min_value=50, max_value=250, value=170, key="height")

with col2:
    # Capturing Age and Sex
    st.number_input("Age (years):", min_value=1, max_value=120, value=25, key="age")
    st.selectbox("Sex:", ["Male", "Female", "Other"], key="gender")

st.divider()

# --- NAVIGATION ---
# Make sure the file in your 'pages' folder is named exactly "1_🏥_Health.py" 
# or update the string below to match your filename.
if st.button("Start Assessment "):
    st.switch_page("pages/1_Health.py")
