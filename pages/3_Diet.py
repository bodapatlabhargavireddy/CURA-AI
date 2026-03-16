import streamlit as st

st.title("🥗 Step 3: Diet Preference")

st.radio("Choose your preferred cuisine:", 
         ["Indian", "Continental", "Mediterranean", "Keto"], 
         key="cuisine")

st.progress(75)

if st.button("🏁 Generate My Cura Dashboard"):
    st.switch_page("pages/4_Dashboard.py")
