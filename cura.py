import streamlit as st

st.set_page_config(page_title="Cura AI", initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid='collapsedControl'] {display: none;}</style>", unsafe_allow_html=True)

st.title("🛡️ Cura AI: Step 1")
st.subheader("Physical Profile")

# These 'keys' are the most important part for updating the user input
st.number_input("Age", 15, 95, 25, key="age")
st.selectbox("Gender", ["Male", "Female"], key="gender")
st.number_input("Weight (kg)", 35.0, 180.0, 70.0, key="weight")
st.number_input("Height (cm)", 100.0, 250.0, 170.0, key="height")

st.progress(20) 

if st.button("Next: Health Profile ➡️"):
    # This moves to the next page while keeping the data in memory
    st.switch_page("pages/1_Health.py")
