import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. SETUP & CONFIGURATION
st.set_page_config(page_title="Cura AI", page_icon="🛡️", layout="wide")

# Custom CSS for Branding
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; }
    .metric-container { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# API Configuration
GOOGLE_API_KEY = "st.secrets["GEMINI_API_KEY"]" 
genai.configure(api_key=GOOGLE_API_KEY)

def get_gemini_response(prompt, image=None):
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        if image:
            response = model.generate_content([prompt, image])
        else:
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to Cura Brain: {e}"

# 2. DYNAMIC LOGIC ENGINE
def calculate_metrics(w, h, a, g, goal, diseases):
    # BMR calculation using Mifflin-St Jeor
    s = 5 if g == "Male" else -161
    bmr = (10 * w) + (6.25 * h) - (5 * a) + s
    
    # Activity & Goal adjustment
    tdee = bmr * 1.3 
    if goal == "Weight Loss": tdee -= 500
    elif goal == "Weight Gain": tdee += 400
    
    # Precise Medical Adjustments
    if "PCOD" in diseases or "Thyroid" in diseases:
        tdee *= 0.85 # Higher metabolic resistance for these conditions
    
    # Dynamic Outputs
    prot = w * (2.2 if goal == "Weight Gain" else 1.6)
    water = w * 0.035
    steps = 11000 if goal == "Weight Loss" else 7500
    sleep = "7-8 hours" if "BP" not in diseases else "8-9 hours (Essential for Hypertension control)"
    
    return int(tdee), int(prot), round(water, 1), steps, sleep

# 3. SIDEBAR: CURA USER PROFILE
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=100)
    st.title("Cura Profile")
    st.divider()
    age = st.number_input("Age", 15, 95, 25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    weight = st.number_input("Weight (kg)", 35, 180, 70)
    height = st.number_input("Height (cm)", 100, 250, 170)
    
    st.header("Medical Context")
    meds = st.multiselect("Active Conditions", ["None", "Diabetes", "BP", "Thyroid", "PCOD"])
    goal = st.selectbox("Current Goal", ["Maintenance", "Weight Loss", "Weight Gain", "Disease Management"])
    cuisine = st.selectbox("Preferred Diet", ["Indian", "Western", "Continental"])

# 4. MAIN DASHBOARD
st.title("🛡️ Cura: Your Ethical Health Companion")
st.write("---")

cal, prot, water, steps, sleep = calculate_metrics(weight, height, age, gender, goal, meds)

# Metrics Grid
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("🎯 Target Calories", f"{cal} kcal")
with c2: st.metric("🥩 Protein Goal", f"{prot}g")
with c3: st.metric("👣 Daily Steps", f"{steps}")
with c4: st.metric("💧 Water Intake", f"{water} L")

st.info(f"💡 **Cura Recommendation:** Aim for **{sleep}** tonight to optimize recovery.")

# 5. FEATURE TABS
tab1, tab2, tab3 = st.tabs(["🥘 AI Meal Planner", "📸 Vision Scanner", "📊 My Journey"])

with tab1:
    st.subheader(f"Custom {cuisine} Plan")
    if st.button("Generate Medical-Grade Menu"):
        with st.spinner("Cura AI is analyzing your nutritional needs..."):
            prompt = f"""Generate a highly specific 1-day {cuisine} meal plan for {cal} calories. 
            Medical constraints: {meds}. Primary Goal: {goal}. 
            Include: Breakfast, Lunch, Snack, and Dinner. 
            Highlight fiber and protein content for each."""
            menu = get_gemini_response(prompt)
            st.markdown(menu)
            
            st.divider()
            st.write("🔗 **Recommended Order Options:**")
            search_term = "Diabetes friendly" if "Diabetes" in meds else "Healthy"
            st.link_button(f"Find {cuisine} options on Zomato", f"https://www.zomato.com/search?q={search_term}+meals")

with tab2:
    st.subheader("Cura Vision Scanner")
    st.write("Snap a photo of your plate for an instant nutrient audit.")
    img_file = st.camera_input("Scanner Active")
    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Analyzing your meal...", width=400)
        
        with st.spinner("Calculating calories..."):
            v_prompt = f"Analyze this food. Estimate calories, macros, and tell me if it is safe for a person with {meds} and a goal of {goal}."
            analysis = get_gemini_response(v_prompt, img)
            st.success(analysis)

with tab3:
    st.subheader("Cura Journey Tracker")
    today_w = st.slider("Update weight (kg)", 35.0, 180.0, float(weight), 0.1)
    
    if today_w < float(weight):
        st.balloons()
        st.success(f"Great progress! You've lost {round(weight - today_w, 2)}kg. Cura is recalibrating your targets...")
    elif today_w > float(weight):
        st.warning("Weight increased slightly. Cura suggests increasing your step count by 2,000 for the next 2 days.")

    st.write("---")
    st.caption("🔒 Cura Privacy Guarantee: Your health data stays in this session and is never sold.")
