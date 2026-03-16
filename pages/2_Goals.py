import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")

st.title("🎯 Step 4: Your Goal")

# Capture the goal in session_state
st.selectbox("What is your primary target?", 
             ["Maintenance", "Weight Loss", "Weight Gain", "Manage PCOD/PCOS", "Diabetes Control","Thyroid Control",BP Control], 
             key="goal")

st.progress(80)

if st.button("🚀 Generate My Cura Dashboard"):
    st.switch_page("pages/4_Dashboard.py")
