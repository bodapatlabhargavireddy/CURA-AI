import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# --- DATA RETRIEVAL ---
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Maintenance")

# --- CALCULATIONS ---
# 1. Calories (Mifflin-St Jeor)
s = 5 if g == "Male" else -161
cal = int((10 * w) + (6.25 * h) - (5 * a) + s)

# 2. Water (35ml per kg)
water = round(w * 0.035, 1)

# 3. Steps & Exercise (Based on Goal)
if "Loss" in goal:
    steps = 10000
    ex_type = "High Intensity Cardio"
    ex_time = "50-60 Minutes"
elif "Gain" in goal:
    steps = 5000
    ex_type = "Heavy Weight Lifting"
    ex_time = "45 Minutes"
else:
    steps = 8000
    ex_type = "Brisk Walking / Yoga"
    ex_time = "30 Minutes"

# --- UI DISPLAY ---
st.title("🛡️ Health Dashboard")

# Top Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("💧 Water Intake", f"{water} L")
c3.metric("🍗 Protein", f"{int(w * 1.6)} g")
c4.metric("👟 Step Goal", f"{steps:,}")

st.divider()

# Exercise Suggestion Feature
st.subheader("🏋️ Personalized Exercise Plan")
e1, e2 = st.columns(2)
with e1:
    st.info(f"**Recommended Activity:**\n\n{ex_type}")
with e2:
    st.success(f"**Target Duration:**\n\n{ex_time} daily")

st.divider()

# --- AI FOOD MENU WITH AUTO-RETRY ---
st.subheader("🍱 Food Menu")
if st.button("✨ Generate My Plan"):
    with st.spinner("AI is thinking..."):
        # The prompt uses your updated user inputs
        prompt = f"Diet plan for {a}yo {g}, {w}kg. Goal: {goal}. Calorie target: {cal}."
        
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # Try the fast model first
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception:
            # If Flash is busy, try the Pro model automatically
            try:
                model_pro = genai.GenerativeModel('gemini-1.5-pro')
                response = model_pro.generate_content(prompt)
                st.markdown(response.text)
            except Exception:
                st.error("🚨 All AI nodes are busy. Check your internet or API key.")

if st.sidebar.button("🔄 Restart Setup"):
    st.switch_page("cura.py")
