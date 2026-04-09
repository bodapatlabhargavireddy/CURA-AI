import streamlit as st
import google.generativeai as genai

# --- 1. DATA RECOVERY ---
w = st.session_state.get("user_weight")
h = st.session_state.get("user_height")
a = st.session_state.get("user_age")
g = st.session_state.get("user_gender")
goal = st.session_state.get("user_goal")
diet = st.session_state.get("user_diet", "Vegetarian")
cuisine = st.session_state.get("user_cuisine", "Indian")
hc = st.session_state.get("health_conditions", ["None"])

if any(v is None for v in [w, h, a, g, goal]):
    st.error("⚠️ Profile incomplete. Please restart.")
    st.stop()

# --- 2. EXERCISE INTENSITY ENGINE ---
st.title("🛡️ Cura AI: Performance Coach")

# This is the slider you were looking for!
st.subheader("🏋️ Today's Activity")
intensity = st.select_slider(
    "Set your exercise intensity for today:",
    options=["Rest", "Light", "Moderate", "Heavy"],
    value="Moderate" # Default starting position
)

# Intensity Mapping Logic
i_map = {
    "Rest": {"mult": 1.2, "prot": 1.2, "steps": 4000, "water": 0.0},
    "Light": {"mult": 1.375, "prot": 1.5, "steps": 7000, "water": 0.5},
    "Moderate": {"mult": 1.55, "prot": 1.8, "steps": 10000, "water": 0.8},
    "Heavy": {"mult": 1.725, "prot": 2.2, "steps": 15000, "water": 1.2}
}
lvl = i_map[intensity]

# --- 3. BIOLOGICAL CALCULATIONS ---
# Protein & Steps
protein_target = round(w * lvl["prot"], 1)
step_goal = lvl["steps"]

# Water (4% of BW + Intensity boost)
water_target = round((w * 0.04) + lvl["water"], 1)

# Calories (Mifflin-St Jeor)
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["mult"])

# Goal Offset
if "Loss" in goal: cal -= 500
elif "Gain" in goal or "Muscle" in goal: cal += 400

# --- 4. DYNAMIC DASHBOARD ---
st.info(f"📋 **Current Strategy:** {goal} | {intensity} Intensity")

# Row 1: Primary Vitals
c1, c2, c3 = st.columns(3)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{protein_target} g")
c3.metric("💧 Water", f"{water_target} L")

# Row 2: Movement
st.write("### 👟 Movement Target")
st.metric("Daily Step Goal", f"{step_goal:,} steps", delta=f"{intensity} Level")

st.divider()

# --- 5. AI GENERATION ---
if st.button("🚀 Generate AI Plan"):
    with st.spinner("Cura AI is analyzing your intensity level..."):
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = (
                f"User: {g}, {w}kg. Goal: {goal}. Intensity: {intensity}. "
                f"Diet: {diet} ({cuisine}). "
                f"Targets: {cal} kcal, {protein_target}g protein, {step_goal} steps. "
                f"Create a 1-day plan with specific {cuisine} meals."
            )
            
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.balloons()
        except:
            st.warning("Using Local Engine. API busy.")
            st.write(f"Today's Target: {cal} kcal and {protein_target}g protein.")
