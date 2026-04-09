import streamlit as st
import google.generativeai as genai

# --- 1. DATA RECOVERY (The "Sync" Layer) ---
# Pulling every detail from the previous 3 pages
w = st.session_state.get("user_weight", 70.0)
h = st.session_state.get("user_height", 170.0)
a = st.session_state.get("user_age", 25)
g = st.session_state.get("user_gender", "Male")
goal = st.session_state.get("user_goal", "Maintenance")
hc = st.session_state.get("final_conditions", ["None"])
diet = st.session_state.get("user_diet", "Vegetarian")
cuisine = st.session_state.get("user_cuisine", "Indian")
dislikes = st.session_state.get("user_dislikes", ["None"])

# --- 2. IMPROVED WATER CALCULATION ---
# Base: 35ml per kg + 500ml for light/mod activity + 1000ml for heavy
intensity = st.select_slider("Select Today's Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

water_boost = {"Rest": 0.0, "Light": 0.5, "Moderate": 0.8, "Heavy": 1.2}
# Higher base for those recovering from health issues
base_multiplier = 0.040 if goal == "Recover from health issues" else 0.035
water = round((w * base_multiplier) + water_boost[intensity], 1)

# --- 3. BIOLOGICAL MATH ---
bmi = round(w / ((h/100)**2), 1)
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Intensity Multipliers
i_map = {"Rest": 1.2, "Light": 1.375, "Moderate": 1.55, "Heavy": 1.725}
cal = int(bmr * i_map[intensity])

# Goal Adjustments
if "Loss" in goal: cal -= 500
elif "Gain" in goal or "Muscle" in goal: cal += 400

st.title("🛡️ Cura AI: Performance Coach")
st.info(f"👤 **Live Profile:** {g} | {w}kg | Goal: {goal}")

# Metrics Display
c1, c2, c3 = st.columns(3)
c1.metric("🔥 Target Calories", f"{cal} kcal")
c2.metric("💧 Daily Water", f"{water} L", delta="Hydration Target")
c3.metric("⚖️ BMI Status", f"{bmi}")

st.divider()

# --- 4. THE SMART AI PROMPT ---
if "final_plan" not in st.session_state:
    st.session_state.final_plan = None

if st.button("🚀 Generate Personalized Plan"):
    with st.spinner("AI is analyzing Bio + Medical + Diet data..."):
        try:
            # DYNAMIC PROMPT: Now uses EVERYTHING the user entered
            prompt = (
                f"As a pro coach, create a 1-day plan for a {g}, {w}kg, {a}yo. "
                f"Goal: {goal}. Medical Conditions: {hc}. "
                f"Diet: {diet} ({cuisine} style). Avoid these: {dislikes}. "
                f"Workout Intensity: {intensity}. "
                f"Strictly include: 1. Meal plan totaling {cal} cal. 2. Specific advice for {hc}."
            )
            
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            st.session_state.final_plan = response.text
            st.balloons()
            
        except Exception as e:
            st.error("AI is currently offline. Showing local calculation.")
            st.session_state.final_plan = f"Plan for {w}kg {g} seeking {goal} with {diet} diet."

# Display the result
if st.session_state.final_plan:
    st.markdown(st.session_state.final_plan)

if st.sidebar.button("🔄 Reset System"):
    st.session_state.clear()
    st.switch_page("cura.py")
