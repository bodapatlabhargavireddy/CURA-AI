import streamlit as st
import google.generativeai as genai
import time

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Cura AI Pro", layout="wide")

st.title("🛡️ Cura AI Health Dashboard")

# -----------------------------
# CONFIGURE GEMINI
# -----------------------------
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.warning("⚠️ Gemini API Key missing in secrets.")

# -----------------------------
# USER INPUTS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)

with col2:
    height = st.number_input("Height (cm)", 120.0, 220.0, 170.0)

with col3:
    age = st.number_input("Age", 10, 100, 25)

gender = st.selectbox("Gender", ["Male", "Female"])

goal = st.selectbox(
    "Fitness Goal",
    ["Weight Loss", "Maintain Weight", "Weight Gain"]
)

cuisine = st.selectbox(
    "Preferred Cuisine",
    ["Indian", "Mediterranean", "High Protein", "Vegetarian"]
)

intensity = st.select_slider(
    "Activity Level",
    options=["Rest", "Light", "Moderate", "Heavy"]
)

# -----------------------------
# ACTIVITY MAP
# -----------------------------
activity_map = {
    "Rest": {"m": 1.2, "water": 0.0, "protein": 1.2, "fat": 0.30, "steps": 4000},
    "Light": {"m": 1.375, "water": 0.5, "protein": 1.5, "fat": 0.25, "steps": 7000},
    "Moderate": {"m": 1.55, "water": 1.0, "protein": 1.8, "fat": 0.25, "steps": 10000},
    "Heavy": {"m": 1.725, "water": 1.5, "protein": 2.2, "fat": 0.20, "steps": 15000},
}

lvl = activity_map[intensity]

# -----------------------------
# HEALTH CALCULATIONS
# -----------------------------
bmi = round(weight / ((height / 100) ** 2), 1)

if bmi < 18.5:
    status = "Underweight"
elif bmi < 25:
    status = "Healthy"
elif bmi < 30:
    status = "Overweight"
else:
    status = "Obese"

s = 5 if gender == "Male" else -161

bmr = (10 * weight) + (6.25 * height) - (5 * age) + s

calories = int(bmr * lvl["m"])

if goal == "Weight Loss":
    calories -= 500
elif goal == "Weight Gain":
    calories += 400

protein = int(weight * lvl["protein"])
fat = int((calories * lvl["fat"]) / 9)
water = round((weight * 0.035) + lvl["water"], 1)

# -----------------------------
# METRICS DISPLAY
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("🔥 Calories", f"{calories} kcal")
c2.metric("🍗 Protein", f"{protein} g")
c3.metric("🥑 Fat", f"{fat} g")
c4.metric("💧 Water", f"{water} L")

st.info(f"👟 Step Goal: {lvl['steps']:,} | ⚖️ BMI: {bmi} ({status})")

# -----------------------------
# AI COACH BUTTON
# -----------------------------
st.divider()

if st.button("🚀 Generate AI Workout & Meal Plan"):

    if "GEMINI_API_KEY" not in st.secrets:
        st.error("❌ Gemini API Key not configured.")
    else:

        with st.spinner("🤖 AI Coach Thinking..."):

            try:
                model = genai.GenerativeModel("gemini-1.5-flash-latest")

                prompt = f"""
                User Profile:
                Age: {age}
                Gender: {gender}
                Weight: {weight} kg
                BMI: {bmi}
                Goal: {goal}
                Activity Level: {intensity}

                Nutrition Targets:
                Calories: {calories}
                Protein: {protein}g
                Fat: {fat}g

                Task:
                1. Write a short 3 sentence workout plan.
                2. Give a 1 day {cuisine} meal plan.
                """

                response = model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.2,
                        "max_output_tokens": 200
                    }
                )

                if response and hasattr(response, "text"):
                    output = response.text
                else:
                    output = "⚠️ AI returned empty response."

                st.success("✅ AI Plan Ready")
                st.markdown(output)
                st.balloons()

            except Exception as e:

                if "429" in str(e):
                    st.warning("⚠️ API limit reached. Retrying in 60 seconds...")
                    time.sleep(60)

                    try:
                        response = model.generate_content(prompt)
                        st.markdown(response.text)
                    except:
                        st.error("AI still busy. Please try later.")

                else:
                    st.error("⚠️ AI Error")
                    st.code(str(e))

# -----------------------------
# SIDEBAR RESET
# -----------------------------
if st.sidebar.button("🔄 Restart App"):
    st.session_state.clear()
    st.rerun()
