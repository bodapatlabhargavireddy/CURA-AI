import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG & DATA SYNC ---
st.set_page_config(page_title="Cura AI Pro", layout="wide")

# Sync data from Step 1 (Ensures 60kg carries over)
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Weight Loss")
cuisine = st.session_state.get("cuisine", "Indian")

# --- 2. LOCAL SCIENCE ENGINE (Always Works Offline) ---
bmi = round(w / ((h/100)**2), 1)
status = "Healthy" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"

st.title("🛡️ Cura AI: Performance Coach")
intensity = st.select_slider("Select Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

i_map = {
    "Rest": {"m": 1.2, "p": 1.2, "f": 0.30, "s": 4000},
    "Light": {"m": 1.375, "p": 1.5, "f": 0.25, "s": 7000},
    "Moderate": {"m": 1.55, "p": 1.8, "f": 0.25, "s": 10000},
    "Heavy": {"m": 1.725, "p": 2.2, "f": 0.20, "s": 15000}
}
lvl = i_map[intensity]

s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["m"]) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)
prot = int(w * lvl["p"])
fat_g = int((cal * lvl["f"]) / 9)
water = round((w * 0.035) + (0.5 if intensity != "Rest" else 0), 1)

# Display Vitals (Metrics)
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{prot} g")
c3.metric("🥑 Fat Content", f"{fat_g} g")
c4.metric("💧 Water", f"{water} L")

st.info(f"👟 **Step Goal:** {lvl['s']:,} | ⚖️ **BMI:** {bmi} ({status})")
st.divider()

# --- 3. CACHED AI CALL (Quota Protection) ---
if "ai_plan" not in st.session_state:
    st.session_state.ai_plan = None

if st.button("🚀 Generate AI Workout & Meal Plan"):
    if st.session_state.ai_plan:
        st.success("✅ Loading Plan from Memory...")
    else:
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("Missing API Key!")
        else:
            with st.spinner("Analyzing biological metrics..."):
                try:
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    
                    # Auto-detect the right model for your key
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    target_model = available_models[0] if available_models else "gemini-1.5-flash"
                    
                    model = genai.GenerativeModel(target_model)
                    prompt = (f"Coach: 1-day {cuisine} menu and 45m workout for {g}, {w}kg. "
                              f"BMI: {bmi}, Goal: {goal}, Intensity: {intensity}. "
                              f"Target: {cal}cal, {prot}g protein.")
                    
                    response = model.generate_content(prompt)
                    st.session_state.ai_plan = response.text
                    st.balloons()
                    
                except Exception as e:
                    # LOCAL FAILSAFE: If API hits 429 Error, show this professional schedule
                    st.warning("⚠️ Cloud Engine busy. Using Local Expert Engine...")
                    st.session_state.ai_plan = f"""
                    ### 🍱 {cuisine} Menu Schedule for {w}kg {g}
                    * **08:30 AM (Breakfast):** Vegetable Poha or Sprouts salad (Rich in Protein)
                    * **01:30 PM (Lunch):** {cuisine} Thali: Brown Rice, Dal, and Grilled Paneer/Chicken
                    * **05:00 PM (Workout):** **{intensity} Session** (45 mins) + 1 Fruit
                    * **08:30 PM (Dinner):** Light Vegetable Soup & Sautéed Greens
                    
                    **Daily Targets:** {cal} kcal | {prot}g Protein | {water}L Water
                    *💡 Backup mode: Optimized for your {status} BMI status.*
                    """

# Always display the plan once generated (or the backup)
if st.session_state.ai_plan:
    st.markdown("---")
    st.markdown(st.session_state.ai_plan)

if st.sidebar.button("🔄 Restart"):
    st.session_state.ai_plan = None
    st.switch_page("cura.py")
