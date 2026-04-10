import streamlit as st

st.set_page_config(page_title="Cura AI", layout="centered")

st.title("🛡️ CURA AI: Integrated Health System")

# --- BIOLOGICAL PROFILE ---
st.subheader("👤 Biological Profile")
col1, col2 = st.columns(2)

with col1:
    # Starting at 0.0 forces the user to interact
    w_input = st.number_input("Weight (kg):", min_value=0.0, value=0.0, step=0.1, key="weight_val")
    h_input = st.number_input("Height (cm):", min_value=0.0, value=0.0, key="height_val")

with col2:
    a_input = st.number_input("Age:", min_value=0, value=0, key="age_val")
    g_input = st.selectbox("Gender:", ["Select...", "Male", "Female", "Other"], key="gender_val")

st.divider()

if st.button("Start Assessment ➡️"):
    # Validation: Ensure they didn't leave them at 0
    if w_input <= 0 or h_input <= 0 or a_input <= 0 or g_input == "Select...":
        st.error("⚠️ Please enter valid biological metrics to proceed.")
    else:
        st.session_state["user_weight"] = w_input
        st.session_state["user_height"] = h_input
        st.session_state["user_age"] = a_input
        st.session_state["user_gender"] = g_input
        st.switch_page("pages/1_Health.py")
