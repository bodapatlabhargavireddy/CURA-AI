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

if any(v is None for v in [w, h, a, g, goal]):
    st.error("⚠️ Profile incomplete. Please restart.")
    st.stop()

# --- 2. EXERCISE INTENSITY ENGINE ---
st.title("🛡️ Cura AI: Performance Coach")

st.subheader("🏋️ Today's Activity")
intensity = st.select_slider(
    "Set your exercise intensity for today:",
    options=["Rest", "Light", "Moderate", "Heavy"],
    value="Moderate"
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
protein_target = round(w * lvl["prot"], 1)
step_goal = lvl["steps"]
water_target = round((w * 0.04) + lvl["water"], 1)

# Calories (Mifflin-St Jeor)
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["mult"])

if "Loss" in goal: cal -= 500
elif "Gain" in goal or "Muscle" in goal: cal += 400

# --- 4. THE UPDATED STATUS BAR ---
# Now explicitly includes Sex and Weight as requested
st.info(f"📋 **Current Strategy:** {goal} | {intensity} Intensity | **Sex:** {g} | **Weight:** {w}kg")

# Row 1: Primary Vitals
c1, c2, c3 = st.columns(3)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{protein_target} g")
c3.metric("💧 Water", f"{water_target} L")

st.write("### 👟 Movement Target")
st.metric("Daily Step Goal", f"{step_goal:,} steps", delta=f"{intensity} Level")

st.divider()

# --- 5. AI GENERATION ---
if st.button("🚀 Generate AI Plan"):
    with st.spinner("Analyzing profile data..."):
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # The prompt now includes all metrics for better AI accuracy
            prompt = (
                f"User Profile: {g}, {w}kg, {a}yo. Goal: {goal}. Intensity: {intensity}. "
                f"Diet: {diet} ({cuisine}). "
                f"Provide a 1-day plan for {cal} kcal, {protein_target}g protein, and {step_goal} steps."
            )
            
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.balloons()
        except:
            st.warning("Using Local Engine. API busy.")
            st.write(f"Target {cal} kcal and {protein_target}g protein today for a {w}kg {g}.")
