import streamlit as st
import google.generativeai as genai

# --- 1. DATA RECOVERY ---
w = st.session_state.get("user_weight")
h = st.session_state.get("user_height")
a = st.session_state.get("user_age")
g = st.session_state.get("user_gender")
goal = st.session_state.get("user_goal")
health_issues = st.session_state.get("final_conditions", ["None"])
diet_type = st.session_state.get("user_diet", "Vegetarian")
cuisine = st.session_state.get("user_cuisine", "Indian")
dislikes = st.session_state.get("user_dislikes", ["None"])

if any(v is None for v in [w, h, a, g, goal]):
    st.error("⚠️ Profile incomplete. Please restart from the Home page.")
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

s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["mult"])

if "Loss" in goal: cal -= 500
elif "Gain" in goal or "Muscle" in goal: cal += 400

# --- 3. UI DASHBOARD ---
st.info(f"📋 **Strategy:** {goal} | **Sex:** {g} | **Weight:** {w}kg")

col1, col2, col3 = st.columns(3)
col1.metric("🔥 Calories", f"{cal} kcal")
col2.metric("🍗 Protein", f"{protein_target} g")
col3.metric("💧 Water", f"{water_target} L")

st.write("### 👟 Movement Target")
st.metric("Required Steps Today", f"{step_goal:,} steps", delta=f"{intensity} Level")

st.divider()

# --- 4. THE AI GENERATOR ---
if "final_ai_plan" not in st.session_state:
    st.session_state.final_ai_plan = None

if st.button("🚀 Generate Personalized AI Plan"):
    with st.spinner("Connecting to Gemini AI Engine..."):
        try:
            # OPTIMIZED CONFIGURATION
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            
            # Using specific parameters to avoid timeouts
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_output_tokens": 1024,
                }
            )
            
            # THE FORCE PROMPT
            prompt = (
                f"Role: Clinical Nutritionist. Profile: {g}, {w}kg, {a}yo. "
                f"Goal: {goal}. Intensity: {intensity}. Diet: {diet_type} ({cuisine}). "
                f"Medical: {health_issues}. "
                f"Instructions: Create a 1-day plan. Must hit {cal} kcal and {protein_target}g protein. "
                f"MANDATORY: Plan a workout for {step_goal} steps. Use bold headers."
            )
            
            response = model.generate_content(prompt)
            st.session_state.final_ai_plan = response.text
            st.balloons()
            st.success("✅ AI Plan Generated successfully.")
            
        except Exception as e:
            st.error("🚨 API Busy. Please wait exactly 30 seconds (Free Tier Limit).")

# --- 5. DISPLAY AI PLAN ---
if st.session_state.final_ai_plan:
    st.markdown(st.session_state.final_ai_plan)

# --- SIDEBAR TOOLS ---
with st.sidebar:
    st.write("### 🛠️ Developer Tools")
    if st.button("🔄 Clear AI Cache"):
        st.session_state.final_ai_plan = None
        st.rerun()
    if st.button("🚪 Reset All"):
        st.session_state.clear()
        st.switch_page("cura.py")
