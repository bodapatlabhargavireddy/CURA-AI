import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Cura AI Dashboard", layout="wide", initial_sidebar_state="expanded")

# 1. API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ API Key not found! Add it to Streamlit Secrets.")
    st.stop()

st.title("🛡️ Your Cura Health Analysis")

# --- DATA RETRIEVAL ---
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
cuisine = st.session_state.get("cuisine", "Indian")
meds = st.session_state.get("meds", ["None"])
goal = st.session_state.get("goal", "Maintenance")

# --- SMART LOGIC ENGINE ---
# Basic Calorie Calculation (Mifflin-St Jeor)
s = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s
tdee = int(bmr * 1.3)

# Goal-Specific Adjustments
step_goal = 8000
advice_note = "Standard balanced nutrition."

if goal == "Weight Loss":
    tdee -= 500
    step_goal = 10000
elif goal == "Weight Gain":
    tdee += 400
    step_goal = 6000
elif "PCOD" in goal or "Diabetes" in goal:
    tdee -= 200 
    step_goal = 11000
    advice_note = "Focus on Low Glycemic Index (GI) foods."
elif "Thyroid" in goal:
    step_goal = 9000
    advice_note = "Focus on Iodine/Selenium rich foods, avoid raw cruciferous veggies."
elif "BP Control" in goal:
    step_goal = 10000
    advice_note = "DASH Diet: Low Sodium (Salt) and high Potassium."

# Water and Protein
water_target = round(w * 0.035, 1)
protein_target = int(w * 1.4) # Standard 1.4g/kg

# --- DISPLAY OUTPUT: THE 4 KEY METRICS ---
st.subheader(f"🚀 Daily Targets for {goal}")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🔥 Calories", f"{tdee} kcal")
with col2:
    st.metric("💧 Water", f"{water_target} L")
with col3:
    st.metric("🍗 Protein", f"{protein_target} g")
with col4:
    st.metric("👟 Step Goal", f"{step_goal}")

st.info(f"💡 **Expert Tip:** {advice_note}")

st.divider()

# --- AI GENERATOR: THE FOOD MENU ---
st.subheader(f"🍱 AI Generated {cuisine} Menu")
st.write(f"Tailored for: **{goal}**")

if st.button("Generate Medical-Grade Meal Plan"):
    with st.spinner("Cura AI is calculating your macro-nutrients..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Detailed Prompt for the Menu
            prompt = f"""
            Act as a Senior Clinical Dietitian. Create a 1-day {cuisine} food menu.
            User Profile: {g}, {a} years old, {w}kg.
            Primary Goal: {goal}.
            Required Calories: {tdee} kcal.
            
            Format the output as follows:
            1. Breakfast (with calorie count)
            2. Mid-morning Snack
            3. Lunch (with calorie count)
            4. Evening Snack
            5. Dinner (with calorie count)
            
            Ensure the food items are strictly helpful for {goal}.
            """
            
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                
                # Zomato Integration
                st.divider()
                st.success("✅ Menu Prepared! You can find these healthy ingredients/meals below:")
                st.link_button(f"Search {goal} Friendly Food on Zomato", 
                               f"https://www.zomato.com/search?q=healthy+{cuisine}+food")
            
        except Exception as e:
            st.error("AI is currently overloaded. Please try again in 10 seconds.")
            st.info(f"Technical Log: {e}")

# --- SIDEBAR RESTART ---
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset & New Entry"):
    st.session_state.clear()
    st.switch_page("cura.py")
