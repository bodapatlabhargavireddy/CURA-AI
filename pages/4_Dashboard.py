import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cura Dashboard")

# 1. Direct API Key Check
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("❌ Key not found in Secrets. Go to App Settings > Secrets and add GEMINI_API_KEY")
    st.stop()

st.title("🛡️ Cura Health Hub")

# --- Simplified Logic ---
w = st.session_state.get("weight", 70)
h = st.session_state.get("height", 170)
a = st.session_state.get("age", 25)
tdee = int(((10 * w) + (6.25 * h) - (5 * a) + 5) * 1.3)

st.metric("Daily Calories", f"{tdee} kcal")

st.divider()

if st.button("🥘 Generate AI Meal Plan"):
    with st.spinner("Talking to Gemini..."):
        try:
            # Use the most stable model name
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Simple prompt to test connection
            prompt = f"Give a 1-day meal plan for {tdee} calories."
            
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
            else:
                st.warning("AI responded but the text was empty.")
                
        except Exception as e:
            st.error("🚨 Connection Failed!")
            st.info(f"Technical Error Detail: {e}")
            
            # EXPO BACKUP: This shows if the AI fails so you still have something to show!
            st.subheader("📋 Static Backup Plan (AI Offline)")
            st.write("1. Breakfast: Oats with milk and nuts (400 cal)")
            st.write("2. Lunch: Brown rice with grilled chicken/dal (600 cal)")
            st.write("3. Dinner: Mixed vegetable salad with soup (300 cal)")
