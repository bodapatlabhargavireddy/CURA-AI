import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIG & SYNC ---
st.set_page_config(page_title="Cura AI Pro", layout="wide")

# Retrieving session data from Page 1 (cura.py)
# Note: Defaults are provided but will be overridden by your 60kg input
w = st.session_state.get("weight", 60.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Female")
goal = st.session_state.get("goal", "Weight Loss")
cuisine = st.session_state.get("cuisine", "Indian")

# --- 2. LOCAL SCIENCE ENGINE (Deterministic Math) ---
bmi = round(w / ((h/100)**2), 1)
status = "Healthy" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"

st.title("🛡️ Cura AI: Performance Coach")
st.info(f"👤 **Profile Synced:** {g} | {w}kg | {h}cm | BMI: {bmi} ({status})")

intensity = st.select_slider("Select Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

i_map = {
    "Rest": {"m": 1.2, "p": 1.2, "f": 0.30, "s": 4000},
    "Light": {"m": 1.375, "p": 1.5, "f": 0.25, "s": 7000},
    "Moderate": {"m": 1.55, "p": 1.8, "f": 0.25, "s": 10000},
    "Heavy": {"m": 1.725, "p": 2.2, "f": 0.20, "s": 15000}
}
lvl = i_map[intensity]

# Biological Calculations
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["m"]) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)
prot = int(w * lvl["p"])
fat_g = int((cal * lvl["f"]) / 9)
water = round((w * 0.035) + (0.5 if intensity != "Rest" else 0), 1)

# --- 3. DISPLAY VITALS ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{prot} g")
c3.metric("🥑 Fat Content", f"{fat_g} g")
c4.metric("💧 Water", f"{water} L")

st.info(f"👟 **Step Goal:** {lvl['s']:,} | ⚖️ **BMI Status:** {status}")
st.divider()

# --- 4. THE CACHED AI CALL & FAIL-SAFE LOGIC ---

# Initialize memory to avoid losing the plan on refresh
if "final_plan" not in st.session_state:
    st.session_state.final_plan = None

if st.button("🚀 Generate AI Workout & Meal Plan"):
    # If a plan already exists, don't waste the API quota
    if st.session_state.final_plan:
        st.success("✅ Plan loaded from Session Memory.")
    else:
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("Missing API Key in .streamlit/secrets.toml!")
        else:
            with st.spinner(f"Cura AI is analyzing biological data for {w}kg..."):
                try:
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    
                    # Discovery: Find which model is active for your key
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    target_model = available_models[0] if available_models else "gemini-1.5-flash"
                    
                    model = genai.GenerativeModel(target_model)
                    prompt = (f"Coach: Create a 1-day {cuisine} meal schedule and 45m workout for {g}, {w}kg. "
                              f"BMI: {bmi}, Goal: {goal}, Intensity: {intensity}. "
                              f"Target: {cal}cal, {prot}g protein.")
                    
                    response = model.generate_content(prompt)
                    st.session_state.final_plan = response.text
                    st.balloons()
                    
                except Exception as e:
                    # THE EXPO FAIL-SAFE: If 429 Error or 404 occurs, show this professional schedule
                    st.warning("⚠️ Cloud Engine busy. Switching to Local Performance Engine...")
                    
                    local_backup = f"""
                    ## 🍱 {cuisine} Performance Schedule ({w}kg)
                    **Target:** {cal} kcal | **Goal:** {goal} | **Activity:** {intensity}
                    
                    | Time | Activity | Nutrition / Meal Details |
                    | :--- | :--- | :--- |
                    | **08:30 AM** | **Breakfast** | Vegetable Poha / Moong Dal Chilla (High Fiber) |
                    | **11:00 AM** | **Mid-Day** | 1 Seasonal Fruit + 5 Almonds (Healthy Fats) |
                    | **01:30 PM** | **Lunch** | {cuisine} Protein Bowl: Brown Rice, Dal, & Grilled Veggies |
                    | **05:00 PM** | **Workout** | **{intensity} Intensity**: 45m Brisk Walk / Strength |
                    | **08:30 PM** | **Dinner** | Light {cuisine} Soup & Sautéed Greens |
                    
                    ---
                    ### 📊 Local Targets for {w}kg {g}
                    * 🔥 **Energy:** {cal} kcal
                    * 🍗 **Protein:** {prot} g
                    * 💧 **Hydration:** {water} L
                    * 👟 **Steps:** {lvl['s']:,} steps
                    
                    *💡 Note: This plan is strictly calculated using Cura's local biological formulas.*
                    """
                    st.session_state.final_plan = local_backup

# Always display the plan once it has been generated or backed up
if st.session_state.final_plan:
    st.markdown("---")
    st.markdown(st.session_state.final_plan)

# Sidebar for Navigation
if st.sidebar.button("🔄 Reset & Restart"):
    st.session_state.final_plan = None
    st.switch_page("cura.py")
