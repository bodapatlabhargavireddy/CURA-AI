import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Cura AI Pro", layout="wide")

# 1. DATA RECOVERY
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Weight Loss")
cuisine = st.session_state.get("cuisine", "Indian")

# 2. INSTANT CALCULATIONS
bmi = round(w / ((h/100)**2), 1)
status = "Healthy" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"

st.title("🛡️ Cura AI: Performance Coach")
intensity = st.select_slider("Select Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

# Logic for Step Count and Multipliers
i_map = {
    "Rest": {"m": 1.2, "w": 0.0, "p": 1.2, "s": 4000},
    "Light": {"m": 1.375, "w": 0.5, "p": 1.4, "s": 7000},
    "Moderate": {"m": 1.55, "w": 1.0, "p": 1.8, "s": 10000},
    "Heavy": {"m": 1.725, "w": 1.5, "p": 2.2, "s": 15000}
}
lvl = i_map[intensity]

# Math Engine
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["m"]) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)
prot = int(w * lvl["p"])
wat = round((w * 0.035) + lvl["w"], 1)

# 3. DASHBOARD DISPLAY
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{prot} g")
c3.metric("💧 Water", f"{wat} L")
c4.metric("👟 Step Goal", f"{lvl['s']:,}")

st.info(f"📊 **BMI:** {bmi} ({status}) | **Intensity:** {intensity}")

# 4. EXPO-STABLE AI COACH
st.divider()
if st.button("🚀 Generate AI Coaching Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Add GEMINI_API_KEY to your Streamlit Secrets!")
    else:
        with st.spinner("AI Coach is analyzing your vitals..."):
            success = False
            for attempt in range(3): # It will try 3 times automatically
                try:
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Coach for {g}, {a}y, {w}kg. BMI {bmi}, Goal {goal}, {intensity} activity. Suggest 45m workout and {cuisine} menu for {cal}kcal, {prot}g protein."
                    
                    res = model.generate_content(prompt)
                    st.markdown(res.text)
                    st.balloons()
                    success = True
                    break 
                except Exception:
                    time.sleep(2) # Wait 2 seconds before retrying
            
            if not success:
                st.error("The AI is currently swamped with requests. Since your stats are already calculated above, you can still present your dashboard!")import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Cura AI Pro", layout="wide")

# 1. DATA RECOVERY
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
goal = st.session_state.get("goal", "Weight Loss")
cuisine = st.session_state.get("cuisine", "Indian")

# 2. INSTANT CALCULATIONS
bmi = round(w / ((h/100)**2), 1)
status = "Healthy" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"

st.title("🛡️ Cura AI: Performance Coach")
intensity = st.select_slider("Select Exercise Intensity:", options=["Rest", "Light", "Moderate", "Heavy"])

# Logic for Step Count and Multipliers
i_map = {
    "Rest": {"m": 1.2, "w": 0.0, "p": 1.2, "s": 4000},
    "Light": {"m": 1.375, "w": 0.5, "p": 1.4, "s": 7000},
    "Moderate": {"m": 1.55, "w": 1.0, "p": 1.8, "s": 10000},
    "Heavy": {"m": 1.725, "w": 1.5, "p": 2.2, "s": 15000}
}
lvl = i_map[intensity]

# Math Engine
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val
cal = int(bmr * lvl["m"]) + (400 if "Gain" in goal else -500 if "Loss" in goal else 0)
prot = int(w * lvl["p"])
wat = round((w * 0.035) + lvl["w"], 1)

# 3. DASHBOARD DISPLAY
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Calories", f"{cal} kcal")
c2.metric("🍗 Protein", f"{prot} g")
c3.metric("💧 Water", f"{wat} L")
c4.metric("👟 Step Goal", f"{lvl['s']:,}")

st.info(f"📊 **BMI:** {bmi} ({status}) | **Intensity:** {intensity}")

# 4. EXPO-STABLE AI COACH
st.divider()
if st.button("🚀 Generate AI Coaching Plan"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Add GEMINI_API_KEY to your Streamlit Secrets!")
    else:
        with st.spinner("AI Coach is analyzing your vitals..."):
            success = False
            for attempt in range(3): # It will try 3 times automatically
                try:
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Coach for {g}, {a}y, {w}kg. BMI {bmi}, Goal {goal}, {intensity} activity. Suggest 45m workout and {cuisine} menu for {cal}kcal, {prot}g protein."
                    
                    res = model.generate_content(prompt)
                    st.markdown(res.text)
                    st.balloons()
                    success = True
                    break 
                except Exception:
                    time.sleep(2) # Wait 2 seconds before retrying
            
            if not success:
                st.error("The AI is currently swamped with requests. Since your stats are already calculated above, you can still present your dashboard!")
