import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# 1. FETCH DATA FROM THE MAIN PAGE
# This ensures that whatever the user typed in cura.py shows up here
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# 2. CALCULATIONS (THE FEATURES YOU NEED)
# BMI
bmi = round(w / ((h/100)**2), 1)

# Water (35ml per kg)
water = round(w * 0.035, 1)

# Protein (1.6g per kg)
protein = int(w * 1.6)

# Steps and Exercise Time based on Goal
if "Loss" in u_goal:
    steps = 10000
    ex_time = "45-60 Minutes"
    ex_type = "Cardio / Running"
elif "Gain" in u_goal:
    steps = 6000
    ex_time = "45 Minutes"
    ex_type = "Weight Training"
else:
    steps = 8000
    ex_time = "30 Minutes"
    ex_type = "Brisk Walk / Yoga"

# 3. DISPLAY THE DASHBOARD
st.title("📊 Your Health Report")

# Row 1: Key Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("💧 Water Intake", f"{water} L")
c2.metric("👟 Step Goal", f"{steps:,}")
c3.metric("🍗 Protein", f"{protein} g")
c4.metric("⚖️ BMI", f"{bmi}")

# Row 2: Exercise Plan
st.divider()
st.subheader("🏋️ Exercise Suggestion")
st.info(f"**Recommended Activity:** {ex_type} for **{ex_time}** daily.")

st.divider()

# 4. AI MENU GENERATOR (THE CORE FEATURE)
st.subheader(f"🍱 {u_cuisine} Diet Plan")

if st.button("✨ Generate AI Menu"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key! Please check your Streamlit Secrets.")
    else:
        with st.spinner("AI is building your menu..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # We use a direct prompt to keep the AI fast
                prompt = f"Diet plan for {a}yo {g}, {w}kg. Goal: {u_goal}. Cuisine: {u_cuisine}. List Breakfast, Lunch, and Dinner with calorie counts."
                
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.success("Menu Generated Successfully!")
            except Exception:
                st.error("🚨 AI Servers are busy. Please wait 10 seconds and try again.")

# Sidebar Navigation
if st.sidebar.button("🔄 Back to Setup"):
    st.switch_page("cura.py")
