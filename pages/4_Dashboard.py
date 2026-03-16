import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# 2. Retrieve Data (Updates automatically from front page)
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# --- 3. DYNAMIC CALCULATIONS ---
# Mifflin-St Jeor Formula
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Water & Protein
water = round(w * 0.035, 1)
protein = int(w * 1.6)

# Goal-based logic for Steps and Exercise Time
if "Loss" in u_goal:
    cal, steps = int(bmr * 1.2) - 500, 10000
    ex_type, ex_time = "Cardio (Running/HIIT)", "45-60 Minutes"
elif "Gain" in u_goal:
    cal, steps = int(bmr * 1.2) + 400, 5000
    ex_type, ex_time = "Weight Training", "45 Minutes"
else:
    cal, steps = int(bmr * 1.2), 8000
    ex_type, ex_time = "Brisk Walking/Yoga", "30 Minutes"

# --- 4. UI DISPLAY ---
st.title("🛡️ Your Personalized Cura Dashboard")
st.info(f"Analysis for {w}kg {g} | Goal: {u_goal}")

# Metrics Section
col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 Daily Calories", f"{cal} kcal")
col2.metric("💧 Water Intake", f"{water} L")
col3.metric("🍗 Protein Goal", f"{protein} g")
col4.metric("👟 Step Goal", f"{steps:,}")

st.divider()

# Exercise Suggestion Section
st.subheader("🏋️ Exercise & Activity Recommendation")
e_col1, e_col2 = st.columns(2)
with e_col1:
    st.markdown(f"**Recommended Activity:**\n> {ex_type}")
with e_col2:
    st.markdown(f"**Daily Duration:**\n> {ex_time}")

st.divider()

# --- 5. THE AI GENERATOR (Properly Configured) ---
st.subheader(f"🍱 Personalized {u_cuisine} Menu Plan")

if st.button("✨ Generate AI Menu", use_container_width=True):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key! Please set GEMINI_API_KEY in Streamlit Secrets.")
    else:
        with st.spinner("Cura AI is analyzing your profile..."):
            try:
                # Configuration
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Professional Prompt for better results
                prompt = f"""
                As a clinical nutritionist, provide a 1-day {u_cuisine} meal plan.
                User: {g}, {a} years old, {w}kg. Goal: {u_goal}.
                Daily Target: {cal} calories.
                Please list Breakfast, Lunch, Dinner, and a Snack with calorie counts.
                """
                
                # Using generation_config to make the request 'lighter' for the server
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=600
                    )
                )
                
                if response.text:
                    st.success("✅ Your Plan is Ready!")
                    st.markdown(response.text)
                else:
                    st.error("Empty response from AI. Please try again.")
                    
            except Exception as e:
                # Handling the 'Overloaded' error specifically
                st.error("🚨 AI Nodes are busy at the moment.")
                st.info("💡 **Expo Pro-Tip:** The Google API has a 10-second cool-down. Please wait exactly 10 seconds and click 'Generate' again!")

# Sidebar Navigation
if st.sidebar.button("🔄 Restart Assessment"):
    st.switch_page("cura.py")
