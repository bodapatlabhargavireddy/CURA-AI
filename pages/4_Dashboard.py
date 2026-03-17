import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Pro", layout="wide")

# 1. RETRIEVE DATA
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Weight Loss")
cuisine = st.session_state.get("cuisine", "Indian")

# 2. LOCAL CALCULATION (For AI Context)
bmi = round(w / ((h/100)**2), 1)
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

st.title("🛡️ Cura AI: Total Coach")
intensity = st.select_slider("Select Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

# Intensity Logic for the AI
i_map = {
    "Rest": 1.2, "Light": 1.375, "Moderate": 1.55, "Heavy": 1.725
}
cal = int(bmr * i_map[intensity])
prot = int(w * 1.8)
fat = int((cal * 0.25) / 9)

# 3. METRICS DISPLAY
c1, c2, c3, c4 = st.columns(4)
c1.metric("⚖️ BMI", f"{bmi}")
c2.metric("🔥 Calories", f"{cal}")
c3.metric("🍗 Protein", f"{prot}g")
c4.metric("🥑 Fat", f"{fat}g")

st.divider()

# 4. THE AI ENGINE (Meal & Exercise Plan)
if st.button("🚀 Generate My AI Meal & Exercise Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Missing API Key!")
    else:
        with st.spinner("AI Coach is drafting your plan..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # STRICT PROMPT: Forces AI to give exactly what you asked for
                prompt = (
                    f"You are a professional fitness coach. Based on these metrics:\n"
                    f"- Profile: {g}, {a} years old, {w}kg\n"
                    f"- BMI: {bmi}\n"
                    f"- Goal: {goal}\n"
                    f"- Today's Intensity: {intensity}\n"
                    f"- Targets: {cal} kcal, {prot}g Protein, {fat}g Fat\n\n"
                    f"Provide:\n"
                    f"1. A specific 45-minute EXERCISE PLAN for this intensity.\n"
                    f"2. A 1-day {cuisine} MEAL PLAN (Breakfast, Lunch, Dinner) fitting the macros.\n"
                    f"Keep it professional and formatted with bullet points."
                )
                
                # Use a specific configuration to speed up response
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=800
                    )
                )
                
                if response.text:
                    st.markdown(response.text)
                    st.balloons()
                else:
                    st.error("AI generated an empty response. Click again.")
                    
            except Exception as e:
                st.error("AI is temporarily unavailable due to high traffic. Please try once more in 5 seconds.")

if st.sidebar.button("🔄 Restart"):
    st.switch_page("cura.py")
