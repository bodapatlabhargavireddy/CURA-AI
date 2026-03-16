import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("📸 Vision Scanner")
img_file = st.camera_input("Scan your plate")

if img_file:
    img = Image.open(img_file)
    model = genai.GenerativeModel("gemini-1.5-flash")
    with st.spinner("Cura is analyzing..."):
        response = model.generate_content(["Identify this food and estimate calories.", img])
        st.success(response.text)
