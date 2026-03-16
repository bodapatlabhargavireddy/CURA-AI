import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura AI Dashboard", layout="wide")

# --- 1. DATA RETRIEVAL (Ensures inputs are updated) ---
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
u_goal = st.session_state.get("goal", "Maintenance")
u_cuisine = st.session_state.get("cuisine", "Indian")

# --- 2. DYNAMIC CALCULATIONS ---
s_val = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s_val

# Water & Protein
water = round(w * 0.035, 1)
protein = int(w * 1.6)

# Goal-based logic
if "Loss" in u_goal:
    cal, steps = int(bmr * 1.2) - 500, 10000
    ex_type, ex_time = "Cardio (Running/Cycling)", "45-60 Mins"
elif "Gain" in u_goal:
    cal, steps = int(bmr * 1.2) + 400, 5000
    ex_type, ex_time = "Strength Training", "45 Mins"
else:
    cal, steps = int(bmr * 1.2), 8000
    ex_type, ex_time = "Brisk Walk/Yoga", "30 Mins"

# --- 3. UI DISPLAY ---
st.title("🛡️ Cura AI: Your Personal Hub")

# Metrics row
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 Daily Calories", f"{cal} kcal")
c2.metric("💧 Water Intake", f"{water} L")
c3.metric("🍗 Protein Goal", f"{protein} g")
c4.metric("👟 Step Goal", f"{steps:,}")

st.divider()

# Exercise Section
st.subheader("🏋️ Activity Suggestion")
e1, e2 = st.columns(2)
e1.info(f"**Recommended Exercise:** {ex_type}")
e2.success(f"**Required Duration:** {ex_time} Daily")

st.divider()

# --- 4. THE PROPER AI GENERATOR ---
st.subheader(f"🍱 Personalized {u_cuisine} Menu")

if st.button("✨ Generate My Custom Menu"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key missing! Please add it to Streamlit Secrets.")
    else:
        with st.spinner("AI is calculating your diet plan..."):
            try:
                # Proper Configuration
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                
                # Using 1.5-Flash for speed
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # A "Proper" Prompt that AI understands easily
                prompt = f"""
                You are a professional nutritionist. Provide a 1-day {u_cuisine} meal plan.
                User Details: {g}, {a} years old, {w}kg weight.
                Health Goal: {u_goal}.
                Daily Calorie Target: {cal} kcal.
                Activity Level: {ex_time} of {ex_type}.
                Format the output with Breakfast, Lunch, Dinner, and a Snack. 
                Include approximate calories for each meal.
                """
                
                # Safety settings to prevent blocking
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=800,
                    )
                )
                
                if response.text:
                    st.markdown(response.text)
                    st.balloons()
                else:
                    st.error("AI returned an empty response. Try clicking again.")
                    
            except Exception as e:
                # Handle the specific 'Busy' error with a retry message
                st.error("🚨 The AI server is currently overloaded.")
                st.info("💡 **Expo Tip:** This happens when many people use the same API key. Wait 10 seconds and try one more time!")

# Sidebar navigation
if st.sidebar.button("🔄 Restart Setup"):
    st.switch_page("cura.py")
