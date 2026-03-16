import streamlit as st

st.title("🎯 Step 2: Your Goal")

st.selectbox("What is your primary target?", 
             ["Maintenance", "Weight Loss", "Weight Gain", "Manage PCOD/PCOS", 
              "Diabetes Control", "Thyroid Control", "BP Control"], 
             key="goal")

st.progress(50)

if st.button("Next: Diet Preference 🥗"):
    st.switch_page("pages/3_Diet.py")
