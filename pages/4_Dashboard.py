import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Pro", layout="wide")

# Configure Gemini
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ---------------------------
# 1. RETRIEVE USER DATA
# ---------------------------
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Weight Loss")
cuisine = st.session_state.get("cuisine", "Indian")

# ---------------------------
# 2. LOCAL HEALTH ENGINE
# ---------------------------
bmi = round(w / ((h/100)**2), 1)

if bmi < 18.5:
    status = "Underweight"
elif bmi < 25:
    status = "Healthy"
elif bmi < 30:
    status = "Overweight"
else:
    status = "Obese"

st.title("🛡️ Cura AI Dashboard")

intensity = st.select_slider(
    "Activity Level:",
    options=["Rest", "Light", "Moderate", "Heavy"]
)

# Activity Map
i_map = {
    "Rest": {"m": 1.2, "w": 0.0, "p": 1.2, "f": 0.30, "s": 4000},
    "Light": {"m": 1.375, "w": 0.5, "p": 1.5, "f": 0.25, "s": 7000},
    "Moderate": {"m": 1.55, "w": 1.0, "p": 1.8, "f": 0.25, "s": 10000},
    "Heavy": {"m": 1.725, "w": 1.5, "p": 2.2, "f": 0.20, "s": 15000}
}

lvl = i_map[intensity]

# ---------------------------
# 3. BODY CALCULATIONS
# ---------------------------
s_val = 5 if g == "Male" else -161

bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

if "Gain" in goal:
    cal = int(bmr * lvl["m"]) + 400
elif "Loss" in goal:
    cal = int(bmr * lvl["m"]) - 500
else:
    cal = int(bmr * lvl["m"])

prot = int(w * lvl["p"])
fat_g = int((cal * lvl["f"]) / 9)
water = round((w * 0.035) + lvl["w"], 1)

# ---------------------------
# 4. DISPLAY METRICS
# ---------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{prot} g")
c3.metric("🥑 Fats", f"{fat_g} g")
c4.metric("💧 Water", f"{water} L")

st.info(f"👟 Step Goal: {lvl['s']:,} | ⚖️ BMI: {bmi} ({status})")

# ---------------------------
# 5. AI COACH
# ---------------------------
st.divider()

if st.button("🚀 Generate AI Workout & Meal Plan"):

    if "GEMINI_API_KEY" not in st.secrets:
        st.error("❌ Gemini API Key missing in Streamlit secrets.")
    else:

        with st.spinner("🤖 AI Coach Thinking..."):

            try:
                model = genai.GenerativeModel("gemini-1.5-flash")

                prompt = f"""
                User Profile:
                Gender: {g}
                Weight: {w} kg
                BMI: {bmi}
                Goal: {goal}
                Activity Level: {intensity}

                Task:
                1. Give a 3 sentence workout plan
                2. Give a {cuisine} diet menu

                Nutrition Targets:
                Calories: {cal}
                Protein: {prot}g
                Fat: {fat_g}g
                """

                response = model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.2,
                        "max_output_tokens": 400
                    }
                )

                # SAFE TEXT EXTRACTION
                if response and hasattr(response, "text") and response.text:
                    ai_text = response.text
                else:
                    ai_text = "⚠️ AI returned empty response. Please try again."

                st.success("✅ AI Coaching Plan Ready")
                st.markdown(ai_text)
                st.balloons()

            except Exception as e:
                st.error("⚠️ AI Temporary Error. Please try again.")
                st.code(str(e))

# ---------------------------
# 6. SIDEBAR RESET
# ---------------------------
if st.sidebar.button("🔄 Restart"):
    st.session_state.clear()
    st.rerun()
