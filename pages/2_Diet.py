import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid='collapsedControl'] {display: none;}</style>", unsafe_allow_html=True)

st.title("🥘 Step 3: Nutrition Style")
st.selectbox("Choose your primary diet style:",
             ["Indian", "Western", "Continental", "Mediterranean"],
             key="cuisine")

st.progress(60)

col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Back"): st.switch_page("pages/1_Health.py")
with col2:
    if st.button("Next: Set Goal ➡️"): st.switch_page("pages/3_Goals.py")
