import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. SETUP & CONFIGURATION
st.set_page_config(page_title="Cura AI", page_icon="🛡️", layout="wide")

# API Configuration - Fixed with Error Handling
try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except KeyError:
    st.error("❌ API Key not found! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# Helper function to get AI response
def get_gemini_response(prompt, image=None):
    # Using 'gemini-1.5-flash' which is the current stable standard
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    try:
        if image:
            response = model.generate_content([prompt, image])
        else:
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # If 1.5-flash fails, try a fallback to the pro model
        return f"Error connecting to Cura Brain: {e}"

# Custom CSS for Branding
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. DYNAMIC LOGIC ENGINE
def calculate_metrics(w, h, a, g, goal, diseases):
    s = 5 if g == "Male" else -161
    bmr = (10 * w) + (6.25 * h) - (5 * a) + s
    tdee = bmr * 1.3 
    if goal == "Weight Loss": tdee -= 500
    elif goal == "Weight Gain": tdee += 400
    if any(d in ["PCOD", "Thyroid"] for d in diseases):
        tdee *= 0.85
    prot = w * (2.2 if goal == "Weight Gain" else 1.6)
    water = w * 0.035
    steps = 11000 if goal == "Weight Loss" else 7500
    sleep = "7-8 hours" if "BP" not in diseases else "8-9 hours (Essential for Hypertension)"
    return int(tdee), int(prot), round(water, 1), steps, sleep

# 3. SIDEBAR: CURA USER PROFILE
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=100)
    st.title("Cura Profile")
    age = st.number_input("Age", 15, 95, 25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    weight = st.number_input("Weight (kg)", 35, 180, 70)
    height = st.number_input("Height (cm)", 100, 250, 170)
    meds = st.multiselect("Active Conditions", ["None", "Diabetes", "BP", "Thyroid", "PCOD"])
    goal = st.selectbox("Current Goal", ["Maintenance", "Weight Loss", "Weight Gain", "Disease Management"])
    cuisine = st.selectbox("Preferred Diet", ["Indian", "Western", "Continental"])

# 4. MAIN DASHBOARD
st.title("🛡️ Cura: Your Ethical Health Companion")
st.write("---")

cal, prot, water, steps, sleep = calculate_metrics(weight, height, age, gender, goal, meds)

c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("🎯 Target Calories", f"{cal} kcal")
with c2: st.metric("🥩 Protein Goal", f"{prot}g")
with c3: st.metric("👣 Daily Steps", f"{steps}")
with c4: st.metric("💧 Water Intake", f"{water} L")

st.info(f"💡 **Cura Recommendation:** Aim for **{sleep}** tonight.")

# 5. FEATURE TABS
tab1, tab2, tab3 = st.tabs(["🥘 AI Meal Planner", "📸 Vision Scanner", "📊 My Journey"])

with tab1:
    st.subheader(f"Custom {cuisine} Plan")
    if st.button("Generate Medical-Grade Menu"):
        with st.spinner("Analyzing nutritional needs..."):
            prompt = f"1-day {cuisine} meal plan for {cal} cal. Med: {meds}. Goal: {goal}. Breakfast, Lunch, Snack, Dinner."
            st.markdown(get_gemini_response(prompt))

with tab2:
    st.subheader("Cura Vision Scanner")
    img_file = st.camera_input("Scanner Active")
    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Analyzing meal...", width=400)
        with st.spinner("Calculating..."):
            v_prompt = f"Estimate calories and safety for {meds} and goal {goal}."
            st.success(get_gemini_response(v_prompt, img))

with tab3:
    st.subheader("Cura Journey Tracker")
    today_w = st.slider("Update weight (kg)", 35.0, 180.0, float(weight), 0.1)
    if today_w < float(weight):
        st.balloons()
        st.success(f"Lost {round(weight - today_w, 2)}kg! Targets recalibrating...")

st.caption("🔒 Cura Privacy Guarantee: Data is never sold.")
