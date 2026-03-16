import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Cura Dashboard", layout="wide")

# 1. API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ API Key Missing in Secrets!")
    st.stop()

st.title("🛡️ Your Cura Health Hub")

# --- DATA RETRIEVAL ---
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
cuisine = st.session_state.get("cuisine", "Indian")
meds = st.session_state.get("meds", ["None"])
goal = st.session_state.get("goal", "Maintenance")

# --- SCIENTIFIC LOGIC ---
# Calories
s = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s
tdee = int(bmr * 1.3)
if goal == "Weight Loss": tdee -= 500
elif goal == "Weight Gain": tdee += 400

# Other Metrics
water_target = round(w * 0.035, 1)
protein_target = int(w * 1.6)
step_goal = "8,000" if goal == "Maintenance" else "10,000"

# --- DISPLAY METRICS ---
st.subheader("🚀 Your Daily Health Targets")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🔥 Daily Calories", f"{tdee} kcal")
with col2:
    st.metric("💧 Water Intake", f"{water_target} L")
with col3:
    st.metric("🍗 Protein Goal", f"{protein_target} g")
with col4:
    st.metric("👟 Step Goal", f"{step_goal}")

st.divider()

# --- AI MEAL PLAN GENERATOR ---
st.subheader(f"🥘 Personalized {cuisine} Meal Plan")
st.info(f"Goal: {goal} | Medical Context: {', '.join(meds)}")

if st.button("Generate Detailed AI Plan"):
    # List of models to prevent the 404 error
    model_options = ["gemini-1.5-flash", "gemini-pro"]
    
    prompt = f"""
    Create a detailed {cuisine} meal plan for {tdee} calories. 
    User details: {g}, {a} years old, {w}kg. 
    Medical conditions: {meds}. 
    Provide Breakfast, Lunch, and Dinner with calorie estimates.
    """
    
    success = False
    with st.spinner("Cura AI is analyzing..."):
        for model_name in model_options:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                if response.text:
                    st.markdown(response.text)
                    
                    # Food App Suggestion
                    st.divider()
                    st.success("✨ Plan Ready! You can find these healthy options on Zomato.")
                    search_q = f"Healthy {cuisine} food"
                    st.link_button(f"Search {cuisine} on Zomato", f"https://www.zomato.com/search?q={search_q}")
                    
                    success = True
                    break
            except Exception:
                continue
        
        if not success:
            st.error("🚨 Connection Busy. Please try again in a few seconds.")

# Sidebar Restart
st.sidebar.divider()
if st.sidebar.button("🔄 Restart Profile"):
    st.switch_page("cura.py")
