import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura Dashboard", layout="wide")

# 1. API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ API Key Missing!")

st.title("🛡️ Your Cura Health Hub")

# --- DATA RETRIEVAL ---
# These must match the 'key' names from your first page
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Maintenance")

# --- LOGIC ---
# Calories (TDEE)
s = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s
tdee = int(bmr * 1.3)
if goal == "Weight Loss": tdee -= 500
elif goal == "Weight Gain": tdee += 400

# Water (35ml per kg)
water_target = round(w * 0.035, 1)

# Protein (1.6g per kg)
protein_target = int(w * 1.6)

# --- DISPLAYING THE 4 KEY METRICS ---
st.subheader("🚀 Your Daily Health Targets")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🔥 Daily Calories", f"{tdee} kcal")

with col2:
    st.metric("💧 Water Intake", f"{water_target} L")

with col3:
    st.metric("🍗 Protein Goal", f"{protein_target} g")

with col4:
    # We set a standard step goal for the dashboard
    st.metric("👟 Step Goal", "8,000 steps")

st.divider()

# --- MONITORING SECTION (STEPS & WEIGHT) ---
st.subheader("📈 Real-time Monitoring")
m_col1, m_col2 = st.columns(2)

with m_col1:
    st.write("**Weight Tracker**")
    current_weight = st.number_input("Update Today's Weight (kg)", value=float(w))
    weight_diff = round(current_weight - w, 2)
    if weight_diff < 0:
        st.success(f"Down {abs(weight_diff)}kg! Great progress.")
    elif weight_diff > 0:
        st.warning(f"Up {weight_diff}kg. Watch your salt intake!")

with m_col2:
    st.write("**Activity Tracker**")
    steps_walked = st.number_input("Enter Steps Walked Today", 0, 30000, 5000)
    if steps_walked >= 8000:
        st.balloons()
        st.success("Daily Step Goal Reached! ✅")
    else:
        st.info(f"Walk {8000 - steps_walked} more steps to reach your goal.")

# --- AI PLANNER SECTION ---
st.divider()
if st.button("🥘 Generate AI Meal Plan"):
    with st.spinner("AI analyzing..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Diet for {tdee} cal. Weight: {w}kg. Protein: {protein_target}g. Style: {st.session_state.get('cuisine', 'Indian')}."
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error("AI is busy, but your targets are displayed above!")
