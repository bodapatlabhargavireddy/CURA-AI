import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# 1. GET DATA
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# 2. LOCAL CALCULATIONS (These show up even if AI is busy)
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Science-based Protein (1.8g/kg) and Water (35ml/kg)
protein_target = int(w * 1.8)
water_target = round(w * 0.035, 1)

# Goal Logic
if "Loss" in u_goal:
    cal_target = int(bmr * 1.2) - 500
    steps, ex_time, ex_type = 10000, "45-60 min", "Cardio (HIIT)"
elif "Gain" in u_goal:
    cal_target = int(bmr * 1.2) + 400
    steps, ex_time, ex_type = 6000, "45 min", "Strength Training"
else:
    cal_target = int(bmr * 1.2)
    steps, ex_time, ex_type = 8000, "30 min", "Brisk Walk/Yoga"

# 3. UI DISPLAY
st.title("🛡️ Cura AI Dashboard")

# Feature Bar: These will NEVER show a "Busy" error
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Daily Calories", f"{cal_target} kcal")
c2.metric("🍗 Protein Goal", f"{protein_target} g")
c3.metric("💧 Water Intake", f"{water_target} L")
c4.metric("👟 Step Goal", f"{steps:,}")

st.success(f"🏋️ **Exercise Recommendation:** {ex_type} for **{ex_time}** daily.")

st.divider()

# 4. AI MENU (The only part that can be 'Busy')
st.subheader(f"🍱 {u_cuisine} Meal Plan")

if st.button("✨ Generate AI Menu"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key in Secrets!")
    else:
        with st.spinner("Requesting AI Menu..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Optimized prompt: Short and direct for faster response
                prompt = f"1-day {u_cuisine} menu for {a}yo {g}, {w}kg. Goal: {u_goal}. Target: {cal_target} kcal."
                
                # Generation Config: Forces the AI to be fast
                response = model.generate_content(
                    prompt,
                    generation_config={"max_output_tokens": 300, "temperature": 0.4}
                )
                st.markdown(response.text)
                st.balloons()
            except Exception:
                st.error("🚨 Google API is busy. **Expo Tip:** Wait 10 seconds and try one last time!")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
