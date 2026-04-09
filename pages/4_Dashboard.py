import streamlit as st
import google.generativeai as genai

# --- 1. DATA RECOVERY (From all previous pages) ---
w = st.session_state.get("user_weight")
h = st.session_state.get("user_height")
a = st.session_state.get("user_age")
g = st.session_state.get("user_gender")
goal = st.session_state.get("user_goal")

# Dietary & Medical details from pages 1, 2, and 3
health_issues = st.session_state.get("final_conditions", ["None"])
diet_type = st.session_state.get("user_diet", "Vegetarian")
cuisine = st.session_state.get("user_cuisine", "Indian")
dislikes = st.session_state.get("user_dislikes", ["None"])

if any(v is None for v in [w, h, a, g, goal]):
    st.error("⚠️ Profile data missing. Please go back and complete all steps.")
    st.stop()

# --- 2. CALCULATIONS ---
st.title("🛡️ Cura AI: Performance Coach")

intensity = st.select_slider(
    "Set your exercise intensity for today:",
    options=["Rest", "Light", "Moderate", "Heavy"],
    value="Moderate"
)

i_map = {
    "Rest": {"mult": 1.2, "prot": 1.2, "steps": 4000, "water": 0.0},
    "Light": {"mult": 1.375, "prot": 1.5, "steps": 7000, "water": 0.5},
    "Moderate": {"mult": 1.55, "prot": 1.8, "steps": 10000, "water": 0.8},
    "Heavy": {"mult": 1.725, "prot": 2.2, "steps": 15000, "water": 1.2}
}
lvl = i_map[intensity]

protein_target = round(w * lvl["prot"], 1)
step_goal = lvl["steps"]
water_target = round((w * 0.04) + lvl["water"], 1)

# Calories (Mifflin-St Jeor)
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["mult"])

# Apply Goal Offsets
if "Loss" in goal: cal -= 500
elif "Gain" in goal or "Muscle" in goal: cal += 400

# --- 3. DYNAMIC STATUS BAR ---
st.info(f"📋 **Profile:** {w}kg {g} | **Goal:** {goal} | **Diet:** {diet_type} ({cuisine})")

c1, c2, c3 = st.columns(3)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{protein_target} g")
c3.metric("💧 Water", f"{water_target} L")

st.divider()

# --- 4. THE AI GENERATOR (Strict AI Only) ---
if "final_ai_plan" not in st.session_state:
    st.session_state.final_ai_plan = None

if st.button("🚀 Generate AI Workout & Meal Plan"):
    with st.spinner("Cura AI is analyzing your full biological & medical profile..."):
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # THE MASTER PROMPT: Includes every user input
            prompt = (
                f"Role: Expert Fitness Coach & Clinical Nutritionist. "
                f"User Profile: {g}, {w}kg, {h}cm, {a}yo. "
                f"Medical History: {health_issues}. "
                f"Current Goal: {goal}. Today's Intensity: {intensity}. "
                f"Diet Preference: {diet_type} ({cuisine} style). "
                f"Food Dislikes: {dislikes}. "
                f"Requirement: Create a 1-day meal plan for {cal} kcal and {protein_target}g protein. "
                f"Include a workout schedule to reach {step_goal} steps. "
                f"Ensure the plan respects the medical conditions: {health_issues}."
            )
            
            response = model.generate_content(prompt)
            st.session_state.final_ai_plan = response.text
            st.balloons()
            
        except Exception as e:
            st.error("🚨 AI Engine Busy. Please wait 30 seconds and click again to retrieve your plan.")
            # We explicitly do NOT set a local backup here as requested.

# --- 5. DISPLAY AI PLAN ---
if st.session_state.final_ai_plan:
    st.markdown(st.session_state.final_ai_plan)
