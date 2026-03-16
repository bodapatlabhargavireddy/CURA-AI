import streamlit as st
import google.generativeai as genai
import time

# 1. Page Config
st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# 2. Retrieve User Data from Session State
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# --- 3. DYNAMIC CALCULATIONS ---
# Calories (Mifflin-St Jeor)
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Water (35ml per kg)
water_target = round(w * 0.035, 1)

# Goal-Based logic for Steps and Exercise
if "Loss" in u_goal:
    calories = int(bmr * 1.2) - 500
    steps = 10000
    ex_type, ex_time = "Cardio (Running/Cycling)", "45-60 Minutes"
elif "Gain" in u_goal:
    calories = int(bmr * 1.2) + 400
    steps = 5000
    ex_type, ex_time = "Hypertrophy (Weight Lifting)", "45 Minutes"
else:
    calories = int(bmr * 1.2)
    steps = 8000
    ex_type, ex_time = "Brisk Walking / Yoga", "30 Minutes"

# --- 4. DASHBOARD UI ---
st.title("📊 Health Hub Dashboard")
st.info(f"Analysis for: {w}kg | {g} | Goal: {u_goal}")

# Metrics Display
m1, m2, m3, m4 = st.columns(4)
m1.metric("🔥 Calories", f"{calories} kcal")
m2.metric("💧 Water", f"{water_target} L")
m3.metric("🍗 Protein", f"{int(w * 1.6)} g")
m4.metric("👟 Step Goal", f"{steps:,}")

st.divider()

# Exercise Suggestion Feature
st.subheader("🏋️ Exercise & Activity Plan")
ec1, ec2 = st.columns(2)
with ec1:
    st.success(f"**Recommended Activity:**\n\n{ex_type}")
with ec2:
    st.success(f"**Required Duration:**\n\n{ex_time} Daily")

st.divider()

# --- 5. AI FOOD MENU (With Anti-Crash Logic) ---
st.subheader(f"🍱 Personalized {u_cuisine} Menu")

if st.button("✨ Generate AI Menu"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key missing in Streamlit Secrets!")
    else:
        with st.spinner("Connecting to AI Nodes... Please wait."):
            prompt = f"Diet plan for {a}yo {g}, {w}kg. Goal: {u_goal}. Target: {calories} cal. Exercise: {ex_type} for {ex_time}."
            
            # ATTEMPT 1: Try Flash Model
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception:
                # ATTEMPT 2: Wait 2 seconds and try Pro Model
                time.sleep(2)
                try:
                    model_pro = genai.GenerativeModel('gemini-1.5-pro')
                    response = model_pro.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error("⚠️ The AI is currently overloaded due to high traffic at the expo. Please wait 10 seconds and click again.")

# Sidebar Navigation
if st.sidebar.button("🔄 Restart Profile"):
    st.switch_page("cura.py")
