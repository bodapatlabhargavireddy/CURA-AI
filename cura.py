import streamlit as st

st.set_page_config(page_title="Cura AI", initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid='collapsedControl'] {display: none;}</style>", unsafe_allow_html=True)

st.title("🛡️ Cura AI: Step 1")
st.subheader("Physical Profile")

# Save directly to session_state using 'key'
# Example: In your first page
st.number_input("Enter your Weight (kg)", min_value=30, max_value=200, value=70, key="weight")
st.number_input("Enter your Height (cm)", min_value=100, max_value=250, value=170, key="height")
st.number_input("Enter your Age", min_value=10, max_value=100, value=25, key="age")
st.selectbox("Select Gender", ["Male", "Female"], key="gender")

st.progress(20) # Progress bar

if st.button("Next: Health Profile ➡️"):
    st.switch_page("pages/1_Health.py")
