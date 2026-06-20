import streamlit as st
from google import genai
import time
import random

# --- 1. API CONFIGURATION ---
# Initialize the modern Client (looks for st.secrets["GEMINI_API_KEY"] automatically if left empty, 
# or explicitly passed like this for safety)
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Key missing or invalid! Check your st.secrets.")
    st.stop()

# --- 2. DATA RECOVERY ---
w = st.session_state.get("user_weight")
h = st.session_state.get("user_height")
a = st.session_state.get("user_age")
g = st.session_state.get("user_gender")
goal = st.session_state.get("user_goal")
health = st.session_state.get("final_conditions", ["None"])
diet = st.session_state.get("user_diet", "Vegetarian")
cuisine = st.session_state.get("user_cuisine", "Indian")

if any(v is None for v in [w, h, a, g, goal]):
    st.error("⚠️ Profile incomplete. Please restart.")
    st.stop()

# --- 3. CALCULATIONS ---
st.title("🛡️ Cura AI: Performance Coach")

intensity = st.select_slider("Select Intensity:", options=["Rest", "Light", "Moderate", "Heavy"], value="Moderate")

i_map = {
    "Rest": {"mult": 1.2, "prot": 1.2, "steps": 4000, "water": 0.0},
    "Light": {"mult": 1.375, "prot": 1.5, "steps": 7000, "water": 0.5},
    "Moderate": {"mult": 1.55, "prot": 1.8, "steps": 10000, "water": 0.8},
    "Heavy": {"mult": 1.725, "prot": 2.2, "steps": 15000, "water": 1.2}
}
lvl = i_map[intensity]

# Math Engine (Deterministic)
protein_target = round(w * lvl["prot"], 1)
step_goal = lvl["steps"]
water_target = round((w * 0.04) + lvl["water"], 1)

s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["mult"])

if "Loss" in goal: cal -= 500
elif "Gain" in goal: cal += 400

# --- 4. UI DASHBOARD ---
st.info(f"📋 **Strategy:** {goal} | {w}kg {g}")

c1, c2, c3 = st.columns(3)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{protein_target} g")
c3.metric("💧 Water Intake", f"{water_target} L")

st.write("### 👟 Activity Goal")
st.metric("Steps Required", f"{step_goal:,}", delta=f"{intensity} Level")

st.divider()

# --- 5. THE AI GENERATOR (WITH MODERN MODEL ROTATION & RETRY) ---
if "final_ai_plan" not in st.session_state:
    st.session_state.final_ai_plan = None

if st.button("🚀 Generate AI Plan"):
    with st.spinner("Processing Biological Data..."):
        
        # Consistent model rotation aligned with your Scanner page
        models_to_rotate = [
            "gemini-3.1-flash-lite",   
            "gemini-3.1-flash",        
            "gemini-2.5-flash-lite",   
            "gemini-2.5-flash"         
        ]
        
        prompt = (
            f"User: {g}, {w}kg. Goal: {goal}. Diet: {diet} ({cuisine}). "
            f"Medical: {health}. Targets: {cal}kcal, {protein_target}g protein, {water_target}L water. "
            f"Provide a short 24-hour meal and workout plan. Use bold headers."
        )

        success = False
        
        # Outer loop iterates through fallbacks if a cluster or model is completely unavailable
        for m_id in models_to_rotate:
            for attempt in range(2): # 2 attempts per model with jitter
                try:
                    response = client.models.generate_content(
                        model=m_id,
                        contents=prompt
                    )
                    st.session_state.final_ai_plan = response.text
                    success = True
                    break
                except Exception as e:
                    err_str = str(e)
                    if "503" in err_str:
                        # Wait out high traffic clusters with random jitter
                        wait = random.uniform(1.5, 3.5)
                        time.sleep(wait)
                        continue
                    elif "429" in err_str or "404" in err_str:
                        break # Break inner loop to try the next fallback model instantly
            
            if success:
                st.balloons()
                break

        if not success:
            st.error("🚨 All Google Cloud clusters are currently at 100% capacity.")
            st.info("HACKATHON TIP: Switch to a personal mobile hotspot if regional 503 errors persist.")

if st.session_state.final_ai_plan:
    st.markdown(st.session_state.final_ai_plan)
