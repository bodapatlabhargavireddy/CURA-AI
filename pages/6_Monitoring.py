import streamlit as st
import google.generativeai as genai

# --- CONFIG & API ---
st.set_page_config(page_title="Cura Monitoring", layout="wide")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key Missing!")

st.title("🛡️ Cura Live Monitoring & Progress")

# --- DATA RETRIEVAL ---
# 'weight' is the starting weight from the initial profile
starting_weight = st.session_state.get("weight", 70.0)
goal = st.session_state.get("goal", "Maintenance")

# --- NEW FEATURE: WEIGHT TRACKING ---
st.subheader("⚖️ Weight Progress Tracker")
w_col1, w_col2 = st.columns(2)

with w_col1:
    st.info(f"Starting Weight: **{starting_weight} kg**")
    current_weight = st.number_input("Enter Current Weight (kg)", 30.0, 200.0, float(starting_weight))

with w_col2:
    weight_diff = round(current_weight - starting_weight, 2)
    if weight_diff > 0:
        st.warning(f"Weight Gain: +{weight_diff} kg")
    elif weight_diff < 0:
        st.success(f"Weight Loss: {weight_diff} kg")
    else:
        st.info("Weight is Stable")

st.divider()

# --- VITAL SIGNS ---
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

# --- DAILY SCHEDULE ---
st.subheader("💊 Daily Schedule & Reminders")
c_med1, c_med2 = st.columns(2)

with c_med1:
    st.checkbox("Morning Multivitamin")
    st.checkbox("Pre-meal Fiber (Recommended)")
    
with c_med2:
    st.checkbox("Afternoon Hydration Goal (1L)")
    st.checkbox("Evening 15-min Walk")

st.divider()

# --- THE AI FOOD MENU GENERATOR ---
st.subheader("🍱 Personalized Food Menu")

if st.button("🍴 Generate Food Menu Based on Progress"):
    with st.spinner("Analyzing weight trends and vitals..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # The prompt now checks if the weight changed and asks for a plan adjustment
            prompt = f"""
            Act as a Clinical Dietician. 
            User Goal: {goal}. 
            Starting Weight: {starting_weight}kg, Current Weight: {current_weight}kg.
            Vitals: HR {hr}, Sleep {sleep}hrs, BP {bp_sys}.
            
            Task: 
            1. Analyze if the user is on track for their goal ({goal}).
            2. If weight has changed unexpectedly, suggest a 'Plan Adjustment'.
            3. Provide a 1-day Food Menu (Breakfast, Lunch, Dinner) optimized for their current vitals.
            """
            
            response = model.generate_content(prompt)
            st.markdown(response.text)
            
        except Exception:
            # Simple error message to keep it clean for the expo
            st.error("AI Node Busy. Please try again in a few seconds.")

# Sidebar Navigation
if st.sidebar.button("🔄 Back to Dashboard"):
    st.switch_page("pages/4_Dashboard.py")
