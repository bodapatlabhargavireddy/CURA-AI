import streamlit as st

st.set_page_config(page_title="Cura AI", initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid='collapsedControl'] {display: none;}</style>", unsafe_allow_html=True)

st.title("🛡️ Cura AI: Step 1")
st.subheader("Physical Profile")

# Save directly to session_state using 'key'
st.number_input("Age", 15, 95, 25, key="age")
st.selectbox("Gender", ["Male", "Female"], key="gender")
st.number_input("Weight (kg)", 35.0, 180.0, 70.0, key="weight")
st.number_input("Height (cm)", 100.0, 250.0, 170.0, key="height")

st.progress(20) # Progress bar

if st.button("Next: Health Profile ➡️"):
    st.switch_page("pages/1_Health.py")
