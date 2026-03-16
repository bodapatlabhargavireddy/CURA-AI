import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# 1. Safety Check: Is the API Key actually there?
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ API Key is missing from Streamlit Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- DATA RECOVERY ---
# This ensures that even if you didn't enter data, the app doesn't crash
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
cuisine = st.session_state.get("cuisine", "Indian")
meds = st.session_state.get("meds", ["None"])
goal = st.session_state.get("goal", "Maintenance")

# --- CALCULATION LOGIC ---
s = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s
tdee = int(bmr * 1.3)
if goal == "Weight Loss": tdee -= 500
elif goal == "Weight Gain": tdee += 400

water = round(w * 0.035, 1)
protein = int(w * 1.6)

# --- THE OUTPUT UI ---
st.title("🛡️ Your Cura Health Analysis")
st.markdown(f"**Profile Summary:** {g}, {a} years old | **Goal:** {goal}")

# This is the part that was likely missing before:
st.subheader("🚀 Your Daily Health Targets")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🔥 Calories", f"{tdee} kcal")
with col2:
    st.metric("💧 Water", f"{water} L")
with col3:
    st.metric("🍗 Protein", f"{protein} g")
with col4:
    st.metric("👟 Steps", "10,000" if goal != "Maintenance" else "8,000")

st.divider()

# --- THE AI OUTPUT ---
st.subheader(f"🥘 AI {cuisine} Meal Planner")

if st.button("Generate My Meal Plan"):
    with st.spinner("AI is thinking..."):
        try:
            # We use the 'flash' model because it's the most reliable for free tier
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Create a {cuisine} meal plan for {tdee} calories. 
            User is {g}, {w}kg, with {meds}. 
            List Breakfast, Lunch, and Dinner.
            """
            
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.success("Plan Generated Successfully!")
            else:
                st.warning("The AI returned an empty response. Try clicking the button again.")
                
        except Exception as e:
            st.error("🚨 AI Connection Error")
            st.info(f"Technical Reason: {str(e)}")
            st.write("---")
            st.write("**Quick Recommendation (Offline Mode):**")
            st.write(f"To reach {tdee} calories, eat 3 balanced meals focused on {cuisine} flavors.")

# Sidebar Navigation
if st.sidebar.button("🔄 Start New Profile"):
    st.switch_page("cura.py")
