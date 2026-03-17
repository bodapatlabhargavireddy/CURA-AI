import streamlit as st

st.set_page_config(page_title="Cura AI", initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid='collapsedControl'] {display: none;}</style>", unsafe_allow_html=True)

st.title("🛡️ Cura AI: Step 1")
st.subheader("Physical Profile")

# --- THE FIX: Use .get() to set the starting value ---
# This tells Streamlit: "Check if we already have a value. If not, use the default."

st.number_input("Age", 15, 95, value=st.session_state.get("age", 25), key="age")

st.selectbox("Gender", ["Male", "Female"], 
             index=0 if st.session_state.get("gender") == "Male" else 1, 
             key="gender")

st.number_input("Weight (kg)", 35.0, 180.0, 
                value=st.session_state.get("weight", 70.0), 
                key="weight")

st.number_input("Height (cm)", 100.0, 250.0, 
                value=st.session_state.get("height", 170.0), 
                key="height")

st.progress(20) 

if st.button("Next: Health Profile ➡️"):
    st.switch_page("pages/1_Health.py")
