import streamlit as st
from google import genai
import PIL.Image
import time

st.title("🍎 Cura AI: Food Scanner")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = PIL.Image.open(uploaded_file)
    st.image(img, caption="Scanning...", use_container_width=True)

    if st.button("🔍 Identify & Analyze"):
        with st.spinner("Switching to available engine..."):
            # List of models with DIFFERENT quota buckets
            # If the first one is exhausted, the code jumps to the next
            emergency_models = [
                "gemini-3.1-flash-preview",  # Different bucket than 'flash-image'
                "gemini-2.5-flash",          # Solid backup
                "gemini-1.5-flash-8b"        # The 'last resort' fast model
            ]
            
            success = False
            for model_id in emergency_models:
                try:
                    response = client.models.generate_content(
                        model=model_id,
                        contents=["Identify this food and estimate calories. Be brief.", img]
                    )
                    st.subheader(f"📋 Analysis (via {model_id})")
                    st.markdown(response.text)
                    st.balloons()
                    success = True
                    break 
                except Exception as e:
                    if "429" in str(e):
                        st.write(f"⚠️ {model_id} bucket full, trying next...")
                        continue
                    else:
                        st.error(f"Error: {e}")
                        break
            
            if not success:
                st.error("All free-tier buckets exhausted. Please create a NEW API Key with a different Google account to continue.")
