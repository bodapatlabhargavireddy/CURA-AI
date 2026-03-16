import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid='collapsedControl'] {display: none;}</style>", unsafe_allow_html=True)

st.title("🏥 Step 2: Medical Context")
st.multiselect("Select any active conditions:", 
               ["None", "Diabetes", "BP", "Thyroid", "PCOD"], 
               key="meds")

st.progress(40)

col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Back"): st.switch_page("cura.py")
with col2:
    if st.button("Next: Diet Preference ➡️"): st.switch_page("pages/2_Diet.py")
