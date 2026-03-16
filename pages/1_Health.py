import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")
st.title("🏥 Step 1: Medical Context")

st.multiselect("Select any active conditions:", 
               ["None", "Diabetes", "BP Control", "Thyroid", "PCOD/PCOS"], 
               key="meds")

st.progress(25)

if st.button("Next: Set Your Goal 🎯"):
    st.switch_page("pages/2_Goal.py") # Ensure filename matches exactly
