import streamlit as st
import google.generativeai as genai

st.set_page_config(initial_sidebar_state="expanded")

# 1. API Initialization with Error Handling
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ API Key Missing")

st.title("🛡️ Cura Dashboard")

# 2. Retrieve session data
w = st.session_state.get("weight", 70)
h = st.session_state.get("height", 170)
a = st.session_state.get("age", 25)
g = st.session_state.get("gender", "Male")
cuisine = st.session_state.get("cuisine", "Indian")
meds = st.session_state.get("meds", ["None"])

# 3. Quick Calculations
s = 5 if g == "Male" else -161
bmr = (10 * w) + (6.25 * h) - (5 * a) + s
tdee = int(bmr * 1.3)

c1, c2, c3 = st.columns(3)
c1.metric("Daily Calories", f"{tdee} kcal")
c2.metric("Protein", f"{int(w * 1.6)}g")
c3.metric("Water", f"{round(w * 0.035, 1)} L")

st.divider()

# 4. ROBUST AI MEAL PLAN GENERATION
if st.button("🥘 Generate AI Meal Plan"):
    # Using 1.5-flash as it is faster and less likely to timeout
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    Create a 1-day {cuisine} meal plan for {tdee} calories. 
    User medical context: {meds}. 
    Provide Breakfast, Lunch, and Dinner with calorie estimates.
    """
    
    with st.spinner("Connecting to Cura Brain..."):
        try:
            # We add a request_options timeout to prevent the 'grpc' error you saw
            response = model.generate_content(
                prompt,
                request_options={"timeout": 600} # Increases wait time to 10 mins
            )
            if response.text:
                st.markdown(response.text)
            
            st.info("🔗 **Order Healthy Options:**")
            st.link_button("Search Healthy Meals on Zomato", f"https://www.zomato.com/search?q=Healthy+food")
            
        except Exception as e:
            st.error(f"⚠️ Connection Error: The AI is taking too long to respond. Please try again in a moment. (Error: {str(e)})")
