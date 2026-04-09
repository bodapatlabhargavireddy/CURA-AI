import streamlit as st
import google.generativeai as genai

# --- 1. STRICT DATA RECOVERY ---
# Retrieving all variables from previous pages
w = st.session_state.get("user_weight")
h = st.session_state.get("user_height")
a = st.session_state.get("user_age")
g = st.session_state.get("user_gender")
goal = st.session_state.get("user_goal")
diet = st.session_state.get("user_diet", "Vegetarian")
cuisine = st.session_state.get("user_cuisine", "Indian")
dislikes = st.session_state.get("user_dislikes", [])
hc = st.session_state.get("health_conditions", ["None"])

# Guard Rail: If any bio-data is missing, force restart
if any(v is None for v in [w, h, a, g, goal]):
    st.error("⚠️ Incomplete Profile. Please restart the assessment.")
    if st.button("Restart"):
        st.switch_page("cura.py")
    st.stop()

# --- 2. DYNAMIC CALCULATIONS (The Engine) ---
st.title("🛡️ Cura AI: Performance Coach")
intensity = st.select_slider("Select Today's Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

# Protein & Steps Map
prot_map = {"Rest": 1.2, "Light": 1.5, "Moderate": 1.8, "Heavy": 2.2}
step_map = {"Rest": 4000, "Light": 7000, "Moderate": 10000, "Heavy": 15000}

protein_target = round(w * prot_map[intensity], 1)
steps = step_map[intensity]

# Water: 4% of BW + Intensity Boost
water_boost = {"Rest": 0, "Light": 0.5, "Moderate": 0.8, "Heavy": 1.2}
water = round((w * 0.04) + water_boost[intensity], 1)

# Calories: Mifflin-St Jeor Formula
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
activity_mult = {"Rest": 1.2, "Light": 1.375, "Moderate": 1.55, "Heavy": 1.725}
cal = int(bmr * activity_mult[intensity])

# Goal Adjustments
if "Loss" in goal: cal -= 500
elif "Gain" in goal or "Muscle" in goal: cal += 400
elif "Recover" in goal: cal = int(bmr * 1.3) # Maintenance level for recovery

# --- 3. DYNAMIC UI ---
st.subheader(f"Strategy: {goal}")
st.info(f"📊 **System Status:** Analyzing {w}kg {g} | {diet} ({cuisine})")

c1, c2, c3 = st.columns(3)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{protein_target} g")
c3.metric("💧 Water", f"{water} L")

st.write("### 👟 Activity Target")
st.metric("Daily Steps", f"{steps:,} steps")

st.divider()

# --- 4. THE AI GENERATOR ---
if "final_plan" not in st.session_state:
    st.session_state.final_plan = None

if st.button("🚀 Generate AI Analysis"):
    with st.spinner("AI is calculating your custom plan..."):
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # THE EXACT PROMPT: Includes Diet, Cuisine, and Health Conditions
            prompt = (
                f"As a pro health coach, create a 1-day plan for: {g}, {w}kg, {a}yo. "
                f"Goal: {goal}. Health Issues: {hc}. "
                f"Dietary Preference: {diet} ({cuisine} style). "
                f"Avoid these foods: {dislikes}. "
                f"Targets: EXACTLY {cal} calories and {protein_target}g protein. "
                f"Provide a 4-meal schedule and a workout to hit {steps} steps."
            )
            
            response = model.generate_content(prompt)
            st.session_state.final_plan = response.text
            st.balloons()
            
        except Exception as e:
            st.warning("Switching to Local Engine due to API limit.")
            st.session_state.final_plan = (
                f"## 🍱 Local Performance Plan\n"
                f"**Target:** {cal} kcal | **Protein:** {protein_target}g | **Steps:** {steps:,}\n\n"
                f"Since the AI is currently busy, follow these biological targets to reach your goal: **{goal}**."
            )

# Display the Markdown result
if st.session_state.final_plan:
    st.markdown(st.session_state.final_plan)

# Sidebar Reset
if st.sidebar.button("🔄 Reset System"):
    st.session_state.clear()
    st.switch_page("cura.py")
