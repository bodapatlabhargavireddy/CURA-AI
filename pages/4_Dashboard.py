import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# 1. RETRIEVE USER DATA
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# 2. THE CALCULATION ENGINE
# Calculate BMR
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Determine Goals
if "Loss" in u_goal:
    cal_goal = int(bmr * 1.2) - 500
    steps = 10000
    ex_time = "45-60 mins"
    ex_type = "Cardio/HIIT"
elif "Gain" in u_goal:
    cal_goal = int(bmr * 1.2) + 400
    steps = 6000
    ex_time = "45 mins"
    ex_type = "Strength Training"
else:
    cal_goal = int(bmr * 1.2)
    steps = 8000
    ex_time = "30 mins"
    ex_type = "Brisk Walk/Yoga"

water = round(w * 0.035, 1)
protein = int(w * 1.6)

# 3. DISPLAY UI
st.title("🛡️ Cura AI Dashboard")

# Metric Bar
m1, m2, m3, m4 = st.columns(4)
m1.metric("🔥 Daily Calories", f"{cal_goal} kcal")
m2.metric("🍗 Protein Goal", f"{protein} g")
m3.metric("💧 Water Intake", f"{water} L")
m4.metric("👟 Step Goal", f"{steps:,}")

st.divider()

# Exercise Feature
st.subheader("🏋️ Activity Suggestion")
st.info(f"**Activity:** {ex_type} | **Duration:** {ex_time} daily")

st.divider()

# 4. AI MENU (The Proper Connection)
st.subheader(f"🍱 {u_cuisine} Menu")
if st.button("✨ Generate My Menu"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key missing! Add it to your Streamlit Secrets.")
    else:
        with st.spinner("AI is calculating..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # We use a strict prompt to avoid "Busy" errors
                prompt = f"Provide a 1-day {u_cuisine} menu for {w}kg {g}, goal: {u_goal}. Target: {cal_goal} kcal. List Breakfast, Lunch, Dinner."
                
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except:
                st.error("🚨 AI Servers are busy. Please wait 10 seconds and try again.")
