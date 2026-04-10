import streamlit as st
from google import genai
import PIL.Image
import time
import random

st.title("🍎 Cura AI: Food Scanner")

# Initialize client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

uploaded_file = st.file_uploader("Upload meal photo...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = PIL.Image.open(uploaded_file)
    st.image(img, caption="Scanning...", use_container_width=True)

    if st.button("🔍 Analyze Meal"):
        # APRIL 2026 STABLE MODELS - Using 'Flash-Lite' first as it has the highest availability
        models_to_rotate = [
            "gemini-3.1-flash-lite",   # Workhorse for 503 errors
            "gemini-3.1-flash",        # Latest stable
            "gemini-2.5-flash-lite",   # Extremely fast fallback
            "gemini-2.5-flash"         # Rock solid backup
        ]
        
        success = False
        with st.spinner("Finding an available AI engine..."):
            for m_id in models_to_rotate:
                # Attempt with jittered retry for 503 errors
                for attempt in range(2): 
                    try:
                        response = client.models.generate_content(
                            model=m_id,
                            contents=["Identify this food and estimate calories. Be brief.", img]
                        )
                        st.success(f"Verified via {m_id}")
                        st.markdown(response.text)
                        st.balloons()
                        success = True
                        break 
                    except Exception as e:
                        if "503" in str(e):
                            # Add 'Jitter' - wait a random small amount to beat the crowd
                            wait = random.uniform(1.5, 3.5)
                            time.sleep(wait)
                            continue 
                        elif "429" in str(e) or "404" in str(e):
                            break # Move to next model in 'models_to_rotate'
                
                if success: break

        if not success:
            st.error("🚨 All Google Cloud clusters are currently at 100% capacity.")
            st.info("HACKATHON TIP: Switch to a personal mobile hotspot. Sometimes regional 503s are IP-based.")
