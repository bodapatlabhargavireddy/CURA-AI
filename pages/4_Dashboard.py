import streamlit as st
import google.generativeai as genai

# 1. Setup
st.set_page_config(page_title="Cura AI", layout="wide")

# 2. Get Data
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# 3. Proper Calculations (Calculated locally - won't crash!)
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
protein = int(w * 1.8)
water = round(w * 0.035, 1)

if "Loss" in u_goal:
    cal, steps, ex_time = int(bmr * 1.2) - 500, 10000, "45-60 min"
elif "Gain" in u_goal:
    cal, steps, ex_time = int(bmr * 1.2) + 400, 5000, "45 min"
else:
    cal, steps, ex_time = int(bmr * 1.2), 8000, "30 min"

# 4. Display Features
st.title("📊 Your Health Dashboard")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 Calories", f"{cal} kcal")
col2.metric("🍗 Protein", f"{protein} g")
col3.metric("💧 Water", f"{water} L")
col4.metric("👟 Steps", f"{steps:,}")

st.info(f"🏋️ **Exercise Duration:** {ex_time} daily")

st.divider()

# 5. AI Menu
if st.button("✨ Generate AI Menu"):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"1-day {u_cuisine} menu: {w}kg {g}, goal: {u_goal}. Target: {cal} cal."
        
        with st.spinner("AI is thinking..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
    except:
        st.error("🚨 AI Busy. Wait 10s and try again.")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
