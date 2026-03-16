import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# ... (Calculations and Metrics stay the same as previous)

if st.button("🥘 Generate AI Meal Plan"):
    # List of models - including the exact 'v1' strings
    model_options = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro"]
    
    # Safety settings can often be the reason for "Blocked" or "Busy" errors
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    prompt = f"Create a {st.session_state.get('cuisine')} meal plan for {tdee} calories. Conditions: {st.session_state.get('meds')}."

    success = False
    with st.spinner("Cura AI is forcing a connection..."):
        for model_name in model_options:
            try:
                # Initialize model with safety settings
                model = genai.GenerativeModel(model_name=model_name)
                response = model.generate_content(
                    prompt,
                    safety_settings=safety_settings,
                    request_options={"timeout": 1000} # Very long timeout
                )
                
                if response:
                    st.markdown(response.text)
                    success = True
                    break
            except Exception as e:
                # Debugging info (remove this before the actual expo)
                # st.write(f"Tried {model_name}: {str(e)}") 
                continue
        
        if not success:
            st.error("🚨 Critical Error: Please check if your GEMINI_API_KEY is active in the Google AI Studio dashboard.")

st.title("🛡️ Your Cura Health Hub")

# --- DATA RETRIEVAL ---
# We use .get() to avoid errors if the user skipped the onboarding
w = st.session_state.get("weight", 70.0)
h = st.session_state.get("height", 170.0)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
cuisine = st.session_state.get("cuisine", "Indian")
meds = st.session_state.get("meds", ["None"])
goal = st.session_state.get("goal", "Maintenance")

# --- LOGIC: CALORIE CALCULATION ---
# Mifflin-St Jeor Equation
s = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s
tdee = int(bmr * 1.3) # Assuming sedentary/light activity

# Adjust based on goal
if goal == "Weight Loss":
    tdee -= 500
elif goal == "Weight Gain":
    tdee += 400

# --- UI: METRICS DISPLAY ---
st.subheader("Your Daily Requirements")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Target Calories", f"{tdee} kcal")
with col2:
    # 1.6g protein per kg is a standard fitness goal
    st.metric("Protein Goal", f"{int(w * 1.6)}g")
with col3:
    # 35ml water per kg
    st.metric("Water Intake", f"{round(w * 0.035, 1)} L")

st.divider()

# --- UI: AI MEAL PLANNER (The Fail-Safe Section) ---
st.subheader(f"🥘 Personalized {cuisine} Menu")
st.write(f"Tailored for {goal} and medical context: {', '.join(meds)}")

if st.button("Generate AI Meal Plan"):
    # Fix: Try multiple model names to avoid the 404 error
    model_options = ["gemini-1.5-flash", "gemini-pro"]
    
    prompt = f"""
    Act as a professional nutritionist. Create a 1-day {cuisine} diet plan for a {g} 
    aged {a}, weighing {w}kg with the goal of {goal}. 
    Medical conditions to consider: {meds}.
    Total target calories: {tdee} kcal.
    Provide Breakfast, Lunch, and Dinner with calorie estimates for each.
    """
    
    success = False
    with st.spinner("Cura AI is searching for a stable model..."):
        for model_name in model_options:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    prompt, 
                    request_options={"timeout": 600}
                )
                if response.text:
                    st.markdown(response.text)
                    success = True
                    break
            except Exception as e:
                # Silently try the next model if one fails
                continue
        
        if not success:
            st.error("🚨 Connection Error: All AI models are currently busy. Please try again in 30 seconds.")
        else:
            st.success("✅ Plan generated successfully!")
            
            # --- UI: FOOD APP SUGGESTION ---
            st.divider()
            st.subheader("🔗 Order Healthy Options")
            st.write("Don't have time to cook? Find matching healthy meals nearby:")
            
            # Create a search query based on cuisine and health
            search_query = f"Healthy {cuisine} food"
            if "Diabetes" in meds:
                search_query = "Sugar free healthy meals"
            
            st.link_button(f"Find on Zomato", f"https://www.zomato.com/search?q={search_query}")

# --- RESET BUTTON ---
st.sidebar.divider()
if st.sidebar.button("🔄 Restart Profile"):
    st.switch_page("cura.py")
