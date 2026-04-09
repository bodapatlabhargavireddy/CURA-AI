import streamlit as st

st.set_page_config(page_title="Cura AI", layout="centered")

st.title("🛡️ CURA AI: Integrated Health System")

# --- BIOLOGICAL PROFILE ---
st.subheader("👤 Biological Profile")

col1, col2 = st.columns(2)

with col1:
    # Adding 'key' makes these persistent across pages
    st.number_input("Weight (kg):", min_value=10.0, value=70.0, key="weight")
    st.number_input("Height (cm):", min_value=50, value=170, key="height")

with col2:
    st.number_input("Age:", min_value=1, value=25, key="age")
    st.selectbox("Sex:", ["Male", "Female", "Other"], key="gender")

st.divider()
# --- In cura.py ---

if st.button("Start Assessment 🏥"):
    st.session_state["weight"] = st.session_state.weight
    st.session_state["height"] = st.session_state.height
    st.session_state["age"] = st.session_state.age
    st.session_state["gender"] = st.session_state.gender
    
    st.switch_page("pages/1_Health.py") # Use the simple filename we discussed
