import streamlit as st
from google import genai
import PIL.Image
import time

st.title("🍎 Cura AI: Food Scanner")

# Initialize client with the NEW API KEY from secrets
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Invalid API Key in Secrets!")

uploaded_file = st.file_uploader("Upload meal photo...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = PIL.Image.open(uploaded_file)
    st.image(img, caption="Scanning...", use_container_width=True)

    if st.button("🔍 Analyze Meal"):
        with st.spinner("Rotating AI engines to find availability..."):
            # 2026 Stable Model List
            models = ["gemini-3.1-flash", "gemini-3.1-flash-lite", "gemini-2.5-flash"]
            
            success = False
            for m_id in models:
                try:
                    # The 2026 SDK doesn't always need the 'models/' prefix
                    response = client.models.generate_content(
                        model=m_id,
                        contents=["Identify this food and estimate calories. Be brief.", img]
                    )
                    st.success(f"Analysis complete via {m_id}")
                    st.markdown(response.text)
                    st.balloons()
                    success = True
                    break 
                except Exception as e:
                    # If 404 (Not Found) or 429 (Busy), try the next model
                    if "404" in str(e) or "429" in str(e):
                        continue
                    else:
                        st.error(f"Error: {e}")
                        break
            
            if not success:
                st.error("All available engines are busy. Please wait 60s or swap your API Key.")
