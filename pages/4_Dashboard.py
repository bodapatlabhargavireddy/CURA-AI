import streamlit as st
import google.generativeai as genai

# 1. SETUP
st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# 2. RETRIEVE DATA FROM SESSION STATE
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# 3. SCIENTIFIC CALCULATIONS (The "Proper" Features)
# BMR calculation
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Water & Protein (Updates with Weight)
water_target = round(w * 0.035, 1)
protein_target = int(w * 1.8)

# Goal-based logic
if "Loss" in u_goal:
    cal_target = int(bmr * 1.2) - 500
    steps, ex_time, ex_type = 10000, "45-60 min", "Cardio (HIIT)"
elif "Gain" in u_goal:
    cal_target = int(bmr * 1.2) + 400
    steps, ex_time, ex_type = 6000, "45 min", "Strength Training"
else:
    cal_target = int(bmr * 1.2)
    steps, ex_time, ex_type = 8000, "30 min", "Brisk Walk/Yoga"

# 4. DASHBOARD UI (Shows instantly)
st.title("🛡️ Cura AI Dashboard")

# Top Metrics Bar
col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 Calories", f"{cal_target} kcal")
col2.metric("🍗 Protein", f"{protein_target} g")
col3.metric("💧 Water", f"{water_target} L")
col4.metric("👟 Step Goal", f"{steps:,}")

st.success(f"🏋️ **Workout Recommendation:** {ex_type} for **{ex_time}** daily.")
st.divider()

# 5. THE AI MENU GENERATOR (With 'Busy' Protection)
st.subheader(f"🍱 {u_cuisine} Meal Plan")

if st.button("✨ Generate AI Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key in Secrets!")
    else:
        with st.spinner("AI is analyzing..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Concise prompt for faster response
                prompt = f"1-day {u_cuisine} diet for {a}yo {g}, {w}kg. Goal: {u_goal}. Target: {cal_target} kcal."
                
                # Config to avoid 'Busy' errors
                response = model.generate_content(
                    prompt, 
                    generation_config={"max_output_tokens": 350, "temperature": 0.5}
                )
                
                if response.text:
                    st.markdown(response.text)
                    st.balloons()
            except Exception:
                st.error("🚨 AI Servers are busy. Wait 10 seconds and try again!")

# Navigation
if st.sidebar.button("🔄 Restart Setup"):
    st.switch_page("cura.py")
