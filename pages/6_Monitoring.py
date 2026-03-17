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
# We use .get() to find the height from the first page for BMI math
height_cm = st.session_state.get("height", 170.0) 
goal = st.session_state.get("goal", "Maintenance")

# --- WEIGHT TRACKING (AUTO-SYNCED) ---
st.subheader("⚖️ Weight & BMI Progress")
w_col1, w_col2, w_col3 = st.columns(3)

with w_col1:
    # IMPORTANT: By using key="weight", this input stays the same on every page.
    # No more resetting when you switch pages!
    current_weight = st.number_input("Enter Today's Weight (kg)", 30.0, 200.0, key="weight")

with w_col2:
    # LIVE BMI MATH: Updates automatically as you type
    bmi = round(current_weight / ((height_cm / 100) ** 2), 1)
    
    if bmi < 18.5: status, color = "Underweight", "blue"
    elif 18.5 <= bmi < 25: status, color = "Healthy", "green"
    elif 25 <= bmi < 30: status, color = "Overweight", "orange"
    else: status, color = "Obese", "red"
    
    st.metric("Live BMI", f"{bmi}", delta=status)
    st.markdown(f"Status: :{color}[**{status}**]")

with w_col3:
    # This assumes 'starting_weight' was the very first value entered
    # We store the very first weight in a separate 'initial' key if you want to track total loss
    if "initial_weight" not in st.session_state:
        st.session_state["initial_weight"] = current_weight
        
    diff = round(current_weight - st.session_state["initial_weight"], 2)
    st.metric("Total Change", f"{diff} kg", delta=diff, delta_color="inverse")

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
    with st.spinner("Cura AI is analyzing your live data..."):
        prompt = f"""
        Act as a Clinical Dietician. 
        User Goal: {goal}. 
        Current Weight: {current_weight}kg, BMI: {bmi} ({status}).
        Vitals: HR {hr}, Sleep {sleep}hrs, BP {bp_sys}.
        
        Task: 
        1. Give a 1-day Food Menu (Breakfast, Lunch, Dinner) based on BMI status: {status}.
        2. Provide 2 health tips for a {goal} goal.
        """

        success = False
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.markdown(response.text)
            success = True
        except Exception:
            try:
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                model = genai.GenerativeModel(available_models[0])
                response = model.generate_content(prompt)
                st.markdown(response.text)
                success = True
            except:
                st.error("🚨 AI Nodes Busy. Your live BMI is still calculated above!")

        if success:
            st.balloons()

# Sidebar Navigation
if st.sidebar.button("🔄 Back to Dashboard"):
    st.switch_page("pages/4_Dashboard.py")
