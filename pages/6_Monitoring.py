import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Monitoring", layout="wide")

# --- DATA RETRIEVAL ---
w = st.session_state.get("weight", 70.0)
goal = st.session_state.get("goal", "Maintenance")

st.title("🛡️ Cura Live Monitoring")

# --- NEW FEATURE: VITAL SIGNS ---
st.subheader("💓 Live Vitals (Simulation)")
v_col1, v_col2, v_col3 = st.columns(3)

with v_col1:
    hr = st.number_input("Heart Rate (BPM)", 40, 200, 72)
    if hr > 100: st.warning("High Heart Rate detected.")
    elif hr < 60: st.info("Resting heart rate is low.")

with v_col2:
    bp_sys = st.number_input("Systolic BP (Upper)", 80, 200, 120)
    if bp_sys > 140: st.error("Hypertension Warning! 🚩")

with v_col3:
    sleep = st.slider("Sleep Duration (Hours)", 0, 12, 8)
    if sleep < 6: st.warning("Sleep deprivation detected.")

st.divider()

# --- NEW FEATURE: MEDICATION/SUPPLEMENT REMINDER ---
st.subheader("💊 Daily Schedule")
c_med1, c_med2 = st.columns(2)

with c_med1:
    st.checkbox("Morning Multivitamin")
    st.checkbox("Pre-meal Fiber (Recommended for Diabetes/PCOD)")
    
with c_med2:
    st.checkbox("Afternoon Hydration Goal (1L)")
    st.checkbox("Evening 15-min Walk")

st.divider()

# --- THE AI GEN (Keep this as your main feature) ---
if st.button("🥘 Generate Meal Plan Based on Vitals"):
    with st.spinner("Analyzing Vitals..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Updated prompt to include the new Vital data
            prompt = f"User has {goal}. Vitals: HR {hr}, Sleep {sleep}hrs. Create a recovery meal plan."
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error("AI Node Busy.")
