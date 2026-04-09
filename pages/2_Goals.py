import streamlit as st

st.set_page_config(page_title="Set Your Goal", layout="centered", page_icon="🎯")

# Data Guard - ensures we don't lose the Bio or Health data
if "user_weight" not in st.session_state:
    st.error("⚠️ Data connection lost. Returning to Home.")
    st.switch_page("cura.py")
    st.stop()

st.title("🎯 Define Your Goal")
st.write("What is your primary objective?")

# --- UPDATED GOAL SELECTION ---
st.radio(
    "Select your target objective:",
    options=[
        "Weight Loss", 
        "Weight Gain", 
        "Muscle Gain", 
        "Maintenance", 
        "Recover from health issues"
    ],
    key="goal_val"
)

st.divider()

st.subheader("Activity Level")
st.select_slider(
    "How active is your current lifestyle?",
    options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active"],
    key="activity_val"
)

# Navigation
if st.button("Next: Diet Preferences 🥗"):
    # Lock data for the next page
    st.session_state["user_goal"] = st.session_state.goal_val
    st.session_state["user_activity"] = st.session_state.activity_val
    
    # Switch to the next simplified filename
    st.switch_page("pages/3_Diet.py")
