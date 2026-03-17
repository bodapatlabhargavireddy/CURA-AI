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
# Use session_state to track the 'real' current weight across pages
starting_weight = st.session_state.get("weight", 70.0)
goal = st.session_state.get("goal", "Maintenance")

# --- NEW FEATURE: WEIGHT TRACKING ---
st.subheader("⚖️ Weight Progress Tracker")
w_col1, w_col2 = st.columns(2)

with w_col1:
    st.info(f"Initial Profile Weight: **{starting_weight} kg**")
    # We use a unique key 'weight_input' so it doesn't conflict with session_state['weight']
    current_weight = st.number_input("Enter Today's Weight (kg)", 30.0, 200.0, float(starting_weight))
    
    # CRITICAL UPDATE: Update the session state so the AI and Dashboard see the NEW weight
    if st.button("Update Weight Globally"):
        st.session_state["weight"] = current_weight
        st.success("Weight updated for all modules!")

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
    with st.spinner("Cura AI is scanning for an available medical node..."):
        # The prompt now clearly explains the change to the AI
        prompt = f"""
        Act as a Clinical Dietician. 
        User Goal: {goal}. 
        Initial Weight: {starting_weight}kg, Current Weight: {current_weight}kg.
        Trend: {'Gained' if weight_diff > 0 else 'Lost' if weight_diff < 0 else 'Stable'} {abs(weight_diff)}kg.
        Vitals: HR {hr}, Sleep {sleep}hrs, BP {bp_sys}.
        
        Task: 
        1. Analyze if the user is on track for their goal ({goal}).
        2. Give a 1-day Food Menu (Breakfast, Lunch, Dinner).
        3. Adjust calories and portions based on the {weight_diff}kg change.
        """

        success = False
        
        # MODEL RECOVERY LOOP
        # We try 'gemini-1.5-flash' first as it is the most modern and fastest
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.markdown(response.text)
            success = True
        except Exception:
            try:
                # Fallback to Pro
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                st.markdown(response.text)
                success = True
            except Exception:
                try:
                    # Universal Discovery
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    model = genai.GenerativeModel(available_models[0])
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    success = True
                except:
                    st.error("🚨 AI Nodes Busy. Use the data metrics above for your presentation.")

        if success:
            st.balloons()
            st.success("✅ Plan adjusted based on your progress!")

# Sidebar Navigation
if st.sidebar.button("🔄 Back to Dashboard"):
    st.switch_page("pages/4_Dashboard.py")
