import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# 1. FETCH USER DATA
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# 2. LOCAL SCIENTIFIC CALCULATIONS (These never fail!)
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Feature: Protein & Water
protein_target = int(w * 1.8)
water_target = round(w * 0.035, 1)

# Goal Logic for Calories, Steps, and Time
if "Loss" in u_goal:
    cal_target = int(bmr * 1.2) - 500
    steps, ex_time, ex_type = 10000, "45-60 min", "Cardio (HIIT)"
elif "Gain" in u_goal:
    cal_target = int(bmr * 1.2) + 400
    steps, ex_time, ex_type = 6000, "45 min", "Strength Training"
else:
    cal_target = int(bmr * 1.2)
    steps, ex_time, ex_type = 8000, "30 min", "Brisk Walk/Yoga"

# 3. DISPLAY UI
st.title("🛡️ Cura AI Dashboard")

# Feature Bar: Calories, Protein, Water, Steps
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal_target} kcal")
c2.metric("🍗 Protein", f"{protein_target} g")
c3.metric("💧 Water", f"{water_target} L")
c4.metric("👟 Steps", f"{steps:,}")

st.success(f"🏋️ **Workout Plan:** {ex_type} for **{ex_time}** daily.")
st.divider()

# 4. AI MENU WITH AUTOMATIC FALLBACK
st.subheader(f"🍱 {u_cuisine} Meal Plan")

if st.button("✨ Generate Plan"):
    # Pre-written plan in case AI is busy
    fallback_plan = f"""
    ### 🍎 Balanced {u_cuisine} Plan (Standardized)
    * **Breakfast:** Poha or Oats with nuts (approx. 400 kcal)
    * **Lunch:** Dal, Rice/Roti, and Green Salad (approx. 600 kcal)
    * **Dinner:** Grilled Protein (Paneer/Chicken) & Veggies (approx. 500 kcal)
    * **Snack:** Greek Yogurt or Seasonal Fruit.
    * *Note: AI is currently high-traffic. This is your calorie-matched baseline.*
    """
    
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        with st.spinner("AI is thinking..."):
            prompt = f"1-day {u_cuisine} menu for {w}kg {g}, goal: {u_goal}. Target: {cal_target} kcal."
            # Fast settings
            response = model.generate_content(prompt, generation_config={"max_output_tokens": 350})
            st.markdown(response.text)
            st.balloons()
