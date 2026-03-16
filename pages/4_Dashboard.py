import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# 1. RETRIEVE DATA
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# 2. SCIENTIFIC CALCULATIONS (The "Proper" way)
# Calorie Math (BMR)
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Protein & Water Math
protein_target = int(w * 1.8) # 1.8g per kg for active expo users
water_target = round(w * 0.035, 1)

# Goal Logic
if "Loss" in u_goal:
    cal_target = int(bmr * 1.2) - 500
    steps, ex_time, ex_type = 10000, "45-60 min", "Cardio"
elif "Gain" in u_goal:
    cal_target = int(bmr * 1.2) + 400
    steps, ex_time, ex_type = 6000, "45 min", "Strength Training"
else:
    cal_target = int(bmr * 1.2)
    steps, ex_time, ex_type = 8000, "30 min", "Brisk Walk"

# 3. DISPLAY UI
st.title("📊 Your Health Dashboard")

# Feature Row
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal_target} kcal")
c2.metric("🍗 Protein", f"{protein_target} g")
c3.metric("💧 Water", f"{water_target} L")
c4.metric("👟 Steps", f"{steps:,}")

st.success(f"🏋️ **Workout Plan:** {ex_type} for {ex_time} daily")

st.divider()

# 4. AI MENU (Optimized for Speed)
st.subheader(f"🍱 {u_cuisine} Diet Menu")

if st.button("✨ Generate AI Menu"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key in Secrets!")
    else:
        with st.spinner("AI is bypassing traffic..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Simplified prompt = Faster AI response
                prompt = f"1-day {u_cuisine} diet for {w}kg {g}, goal: {u_goal}. Targets: {cal_target} cal, {protein_target}g protein."
                
                # Force a shorter response to prevent timeout
                response = model.generate_content(
                    prompt,
                    generation_config={"max_output_tokens": 350, "temperature": 0.5}
                )
                st.markdown(response.text)
                st.balloons()
            except Exception:
                st.error("🚨 Google API is busy. **Action:** Wait 10 seconds and click again.")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
