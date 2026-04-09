import streamlit as st

st.set_page_config(page_title="Cura AI - Home", layout="centered")

st.title("🛡️ CURA AI: Integrated Health System")
st.write("Welcome to your personal performance ecosystem. Please enter your metrics.")

# --- BIOLOGICAL PROFILE ---
# Using 'key' automatically saves these to st.session_state
st.subheader("👤 Biological Profile")
col1, col2 = st.columns(2)

with col1:
    st.number_input("Weight (kg):", min_value=10.0, value=70.0, step=0.1, key="weight")
    st.number_input("Height (cm):", min_value=50, value=170, key="height")

with col2:
    st.number_input("Age:", min_value=1, value=25, key="age")
    st.selectbox("Sex:", ["Male", "Female", "Other"], key="gender")

st.divider()

# --- NAVIGATION ---
if st.button("Start Assessment ➡️"):
    # No manual assignment needed! The keys handle it.
    st.switch_page("pages/1_Health.py")
