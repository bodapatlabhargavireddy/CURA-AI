import streamlit as st
import google.generativeai as genai
import time

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

# --- 2. CALCULATIONS ---
st.title("🛡️ Cura AI: Performance Coach")
intensity = st.select_slider("Select Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"], value="Moderate")

i_map = {
    "Rest": {"mult": 1.2, "prot": 1.2, "steps": 4000},
    "Light": {"mult": 1.375, "prot": 1.5, "steps": 7000},
    "Moderate": {"mult": 1.55, "prot": 1.8, "steps": 10000},
    "Heavy": {"mult": 1.725, "prot": 2.2, "steps": 15000}
}
lvl = i_map[intensity]

protein_target = round(w * lvl["prot"], 1)
step_goal = lvl["steps"]
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["mult"])

if "Loss" in goal: cal -= 500
elif "Gain" in goal or "Muscle" in goal: cal += 400

# --- 3. UI STATUS ---
st.info(f"📋 **Strategy:** {goal} | **Sex:** {g} | **Weight:** {w}kg")

# --- 4. THE AI PLAN GENERATOR (NO FAILSAFE) ---
if "final_ai_plan" not in st.session_state:
    st.session_state.final_ai_plan = None

if st.button("🚀 Generate AI Plan"):
    with st.spinner("Connecting to Gemini AI Engine..."):
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = (
                f"Give me a detailed 1-day {cuisine} meal plan and workout for a {g}, {w}kg, {a}yo. "
                f"Goal: {goal}. Intensity: {intensity}. "
                f"Diet: {diet}. Targets: {cal} kcal and {protein_target}g protein. "
                f"Use a professional, encouraging tone."
            )
            
            response = model.generate_content(prompt)
            # SUCCESS: Store only the real AI response
            st.session_state.final_ai_plan = response.text
            st.balloons()
            
        except Exception as e:
            st.error("🚨 API Limit Hit! Please wait 30 seconds and click the button again to get the AI Plan.")
            # We do NOT save a local plan here, so the user knows they must try again.

# --- 5. DISPLAY ONLY AI PLAN ---
if st.session_state.final_ai_plan:
    st.divider()
    st.markdown(st.session_state.final_ai_plan)
