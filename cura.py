import streamlit as st

st.set_page_config(page_title="Cura AI", layout="centered", page_icon="🛡️")

st.title("🛡️ CURA AI: Integrated Health System")
st.write("Welcome to your personal performance ecosystem.")

# --- BIOLOGICAL PROFILE ---
st.subheader("👤 Biological Profile")
col1, col2 = st.columns(2)

with col1:
    # We use key="weight_input" to avoid conflicts with the session storage
    weight = st.number_input("Weight (kg):", min_value=10.0, value=70.0, step=0.1, key="weight_val")
    height = st.number_input("Height (cm):", min_value=50, value=170, key="height_val")

with col2:
    age = st.number_input("Age:", min_value=1, value=25, key="age_val")
    gender = st.selectbox("Sex:", ["Male", "Female", "Other"], key="gender_val")

st.divider()

if st.button("Start Assessment ➡️"):
    # FORCED SYNC: Locking data into session state before moving
    st.session_state["user_weight"] = st.session_state.weight_val
    st.session_state["user_height"] = st.session_state.height_val
    st.session_state["user_age"] = st.session_state.age_val
    st.session_state["user_gender"] = st.session_state.gender_val
    
    st.switch_page("pages/1_Health.py")
