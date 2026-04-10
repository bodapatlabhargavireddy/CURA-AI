import streamlit as st
from google import genai
from google.genai import types
import PIL.Image

# --- 1. SETUP ---
st.title("🍎 Cura AI: Food Scanner")

# Use the new SDK client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

uploaded_file = st.file_uploader("Upload an image of your meal...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = PIL.Image.open(uploaded_file)
    st.image(img, caption="Scanning your meal...", use_container_width=True)

    if st.button("🔍 Identify & Analyze"):
        with st.spinner("Cura AI is analyzing the image..."):
            try:
                # Use Gemini 3.1 Flash Image - the 2026 standard for vision
                response = client.models.generate_content(
                    model="gemini-3.1-flash-image-preview",
                    contents=["Identify this food and estimate calories, protein, and health impact.", img]
                )
                
                st.subheader("📋 Nutritional Analysis")
                st.markdown(response.text)
                st.balloons()
                
            except Exception as e:
                if "404" in str(e):
                    st.error("Model not found. We are attempting a fallback to Gemini 3.1 Flash.")
                    # Fallback for hackathon stability
                    response = client.models.generate_content(
                        model="gemini-3.1-flash-preview",
                        contents=["Identify this food and estimate calories.", img]
                    )
                    st.markdown(response.text)
                else:
                    st.error(f"Scanner Error: {e}")
