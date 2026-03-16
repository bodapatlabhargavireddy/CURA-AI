import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# --- DATA RETRIEVAL (Fetching your updated inputs) ---
u_weight = st.session_state.get("weight", 70.0)
u_height = st.session_state.get("height", 170.0)
u_age = st.session_state.get("age", 25)
u_gender = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")

# --- DYNAMIC CALCULATIONS ---
# 1. Calories (Mifflin-St Jeor)
s = 5 if u_gender == "Male" else -161
u_cal = int((10 * u_weight) + (6.25 * u_height) - (5 * u_age) + s)

# 2. Water Intake (35ml per kg)
u_water = round(u_weight * 0.035, 1)

# 3. Step Count & Exercise Duration based on Goal
if "Loss" in u_goal:
    u_steps = 10000
    u_ex_time = "45-60 minutes"
    u_ex_type = "Cardio (Brisk Walking/Cycling)"
elif "Gain" in u_goal:
    u_steps = 6000
    u_ex_time = "30-45 minutes"
    u_ex_type = "Strength Training (Weights)"
else:
    u_steps = 8000
    u_ex_time = "30 minutes"
    u_ex_type = "Moderate Activity (Jogging/Yoga)"

# --- UI DISPLAY ---
st.title("🛡️ Your Personalized Health Dashboard")
st.info(f"Summary for {u_weight}kg: Target {u_cal} kcal per day")

# --- METRICS SECTION ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 Calories", f"{u_cal} kcal")
col2.metric("💧 Water", f"{u_water} L")
col3.metric("🍗 Protein", f"{int(u_weight * 1.5)} g")
col4.metric("👟 Steps", f"{u_steps:,}")

st.divider()

# --- NEW FEATURE: EXERCISE SUGGESTION ---
st.subheader("🏋️ Exercise Suggestion")
ex_col1, ex_col2 = st.columns(2)
with ex_col1:
    st.write(f"**Recommended Type:** {u_ex_type}")
with ex_col2:
    st.write(f"**Daily Duration:** {u_ex_time}")

st.divider()

# --- AI FOOD MENU ---
st.subheader("🍱 Food Menu")
if st.button("✨ Generate My Food Menu"):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # We include the exercise info in the prompt so the AI adjusts the food
        prompt = f"""
        Act as a Nutritionist. Create a 1-day food menu for {u_weight}kg, {u_gender}. 
        Goal: {u_goal}. Target {u_cal} kcal. 
        The user does {u_ex_time} of {u_ex_type} daily.
        """
        
        response = model.generate_content(prompt)
        st.markdown(response.text)
    except:
        st.error("AI Node Busy. Please try again.")

if st.sidebar.button("🔄 Back to Setup"):
    st.switch_page("cura.py")
