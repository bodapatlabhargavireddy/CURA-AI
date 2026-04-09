import streamlit as st

st.set_page_config(page_title="Set Your Goal", layout="centered", page_icon="🎯")

# Data Guard
if "user_weight" not in st.session_state:
    st.error("⚠️ Data connection lost.")
    st.switch_page("cura.py")
    st.stop()

st.title("🎯 Define Your Goal")

st.radio(
    "What is your target?",
    options=["Weight Loss", "Muscle Gain", "Maintenance"],
    key="goal_val"
)

st.divider()

st.select_slider(
    "How active are you?",
    options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active"],
    key="activity_val"
)

if st.button("Next: Diet Preferences 🥗"):
    # Lock data for the next page
    st.session_state["user_goal"] = st.session_state.goal_val
    st.session_state["user_activity"] = st.session_state.activity_val
    st.switch_page("pages/3_Diet.py")
