import streamlit as st
import google.generativeai as genai

st.title("🥘 AI Meal Planner")
if st.button("Generate Today's Menu"):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Create a {st.session_state.cuisine} meal plan for a {st.session_state.age}yo with {st.session_state.meds}."
    response = model.generate_content(prompt)
    st.markdown(response.text)
