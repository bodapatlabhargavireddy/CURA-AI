import streamlit as st
import google.generativeai as genai

# --- CONFIG ---
st.set_page_config(page_title="Cura AI Pro", layout="wide")

# --- 1. DATA RETRIEVAL (Sync from Step 1) ---
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Weight Loss")
cuisine = st.session_state.get("cuisine", "Indian")

# --- 2. LOCAL SCIENCE ENGINE ---
bmi = round(w / ((h/100)**2), 1)
status = "Healthy" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"

st.title("🛡️ Cura AI: Performance Coach")
st.info(f"👤 **Profile Synced:** {g} | {w}kg | {h}cm | BMI: {bmi}")

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

st.info(f"👟 **Step Goal:** {lvl['s']:,} | ⚖️ **BMI:** {bmi} ({status})")
st.divider()

# --- 4. THE CACHED AI CALL ---
if "ai_plan_cache" not in st.session_state:
    st.session_state.ai_plan_cache = None

if st.button("🚀 Generate AI Workout & Meal Plan"):
    if st.session_state.ai_plan_cache:
        st.success("✅ Plan loaded from Session Memory.")
    else:
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("Missing API Key in Secrets!")
        else:
            with st.spinner(f"Cura AI is analyzing stats for {w}kg..."):
                try:
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = (f"Coach: 1-day {cuisine} menu and 45m workout for {g}, {w}kg. "
                              f"BMI: {bmi}, Goal: {goal}, Intensity: {intensity}. "
                              f"Target: {cal}cal, {prot}g protein.")
                    
                    response = model.generate_content(prompt)
                    st.session_state.ai_plan_cache = response.text
                    st.balloons()
                    
                except Exception as e:
                    if "429" in str(e):
                        st.warning("⚠️ API Quota Reached. Using 'Cura Offline Engine'...")
                        # Backup Plan using SYNCED variables
                        st.session_state.ai_plan_cache = f"""
                        ### 🍱 Offline Expert {cuisine} Plan for {w}kg {g}
                        **Nutrition Summary:**
                        * **Breakfast:** Vegetable Poha or Sprouts
                        * **Lunch:** Brown Rice with {cuisine} Dal & Protein
                        * **Dinner:** Clear Soup & Grilled Veggies
                        * **Target:** {cal} kcal | {prot}g Protein
                        
                        **Workout Strategy ({intensity}):**
                        * **Main Activity:** 30-45 mins Brisk Activity
                        * **Daily Goal:** {lvl['s']} Steps
                        
                        *💡 Note: Calculated using local bio-metrics because AI is currently busy.*
                        """
                    else:
                        st.error(f"Error: {str(e)}")

# Display result from memory
if st.session_state.ai_plan_cache:
    st.markdown("---")
    st.markdown(st.session_state.ai_plan_cache)

# Sidebar
if st.sidebar.button("🔄 Reset & Restart"):
    st.session_state.ai_plan_cache = None
    st.switch_page("cura.py")
