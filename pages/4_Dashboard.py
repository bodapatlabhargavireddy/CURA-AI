import streamlit as st
import google.generativeai as genai

# Setup
st.set_page_config(page_title="Cura AI", layout="wide")

# 1. Get User Data
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Weight Loss")
u_cuisine = st.session_state.get("cuisine", "Indian")

# 2. Calculations (Updated Features)
bmi = round(w / ((h/100)**2), 1)
water = round(w * 0.035, 1)
protein = int(w * 1.6)

if "Loss" in u_goal:
    steps, ex_time, ex_type = 10000, "45-60 min", "Cardio"
elif "Gain" in u_goal:
    steps, ex_time, ex_type = 5000, "45 min", "Weights"
else:
    steps, ex_time, ex_type = 8000, "30 min", "Yoga/Walk"

# 3. UI Display
st.title("📊 Your Health Dashboard")
st.write(f"**Profile:** {w}kg | BMI: {bmi} | Goal: {u_goal}")

col1, col2, col3 = st.columns(3)
col1.metric("💧 Water", f"{water} L")
col2.metric("👟 Steps", f"{steps:,}")
col3.metric("🍗 Protein", f"{protein} g")

st.info(f"🏋️ **Exercise:** {ex_type} for **{ex_time}** daily")

st.divider()

# 4. AI Menu Generator
st.subheader(f"🍱 {u_cuisine} Food Menu")
if st.button("✨ Generate My Menu"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key missing in Streamlit Secrets!")
    else:
        with st.spinner("AI is generating..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # We use a very short prompt to make the AI respond faster
                prompt = f"Give a 1-day {u_cuisine} menu: {w}kg, {g}, {u_goal}. Breakfast, Lunch, Dinner."
                
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.balloons()
            except:
                st.error("🚨 AI Servers are busy. Please wait 10 seconds and click again.")

if st.sidebar.button("🔄 Back"):
    st.switch_page("cura.py")
