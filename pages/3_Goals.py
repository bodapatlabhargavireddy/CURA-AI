import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid='collapsedControl'] {display: none;}</style>", unsafe_allow_html=True)

st.title("🎯 Step 4: Your Goal")
st.selectbox("What is your target?", 
             ["Maintenance", "Weight Loss", "Weight Gain"], 
             key="goal")

st.progress(80)

if st.button("🚀 Generate My Cura Dashboard"):
    st.switch_page("pages/4_Dashboard.py")
