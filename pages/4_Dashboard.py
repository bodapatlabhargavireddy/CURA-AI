import streamlit as st
import google.generativeai as genai

# 1. Clear Page Setup
st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# 2. Get the UPDATED data from Step 1
# These variables now update automatically when you change inputs on page 1
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Weight Loss")
u_cuisine = st.session_state.get("cuisine", "Indian")

# 3. Features & Calculations
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Water & Steps Logic
water_target = round(w * 0.035, 1)
protein_target = int(w * 1.6)

if "Loss" in u_goal:
    cal_target = int(bmr * 1.2) - 500
    step_goal = 10000
    ex_type, ex_time = "Cardio (HIIT)", "45-60 mins"
elif "Gain" in u_goal:
    cal_target = int(bmr * 1.2) + 400
    step_goal = 6000
    ex_type, ex_time = "Strength Training", "45 mins"
else:
    cal_target = int(bmr * 1.2)
    step_goal = 8000
    ex_type, ex_time = "Brisk Walk / Yoga", "30 mins"

# 4. Displaying the Dashboard
st.title("🛡️ Cura AI Dashboard")

# Top Metrics Bar
col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 Calories", f"{cal_target} kcal")
col2.metric("💧 Water", f"{water_target} L")
col3.metric("🍗 Protein", f"{protein_target} g")
col4.metric("👟 Step Goal", f"{step_goal:,}")

st.divider()

# Exercise Feature (The "How Much Time" feature you requested)
st.subheader("🏋️ Exercise Suggestion")
e1, e2 = st.columns(2)
with e1:
    st.info(f"**Recommended Type:** {ex_type}")
with e2:
    st.success(f"**Daily Duration:** {ex_time}")

st.divider()

# 5. The AI Menu Generator
st.subheader(f"🍱 Personalized {u_cuisine} Menu")

if st.button("✨ Generate My Menu"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key missing! Add GEMINI_API_KEY to your Secrets.")
    else:
        with st.spinner("AI is thinking..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Optimized prompt for speed
                prompt = f"Create a 1-day {u_cuisine} diet for a {w}kg {g}. Goal: {u_goal}. Calories: {cal_target}. List Breakfast, Lunch, Dinner."
                
                # Request settings to prevent "Busy" errors
                response = model.generate_content(
                    prompt,
                    generation_config={"max_output_tokens": 400, "temperature": 0.7}
                )
                st.markdown(response.text)
                st.balloons()
            except Exception:
                st.error("🚨 AI Servers are busy. Please wait 10 seconds and try again.")

# Navigation
if st.sidebar.button("🔄 Back to Setup"):
    st.switch_page("cura.py")
