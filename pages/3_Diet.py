import streamlit as st

st.set_page_config(page_title="Diet Preferences", layout="centered", page_icon="🥗")

# Data Guard
if "user_goal" not in st.session_state:
    st.error("⚠️ Please set your goal first.")
    st.switch_page("pages/2_Goal.py")
    st.stop()

st.title("🥗 Diet & Nutrition Preferences")
st.write("Customize your meal plan logic.")

col1, col2 = st.columns(2)

with col1:
    st.selectbox(
        "Dietary Type:",
        options=["Vegetarian", "Non-Vegetarian", "Vegan", "Eggetarian"],
        key="diet_type_val"
    )

with col2:
    st.selectbox(
        "Cuisine Style:",
        options=["Indian", "Continental", "Mediterranean", "Western"],
        key="cuisine_val"
    )

st.multiselect(
    "Any specific dislikes? (AI will avoid these):",
    options=["Mushroom", "Dairy", "Spicy Food", "Sea Food", "Sweets"],
    key="dislikes_val"
)

st.divider()

if st.button("Finalize & View Dashboard 📊"):
    # Final data lock
    st.session_state["user_diet"] = st.session_state.diet_type_val
    st.session_state["user_cuisine"] = st.session_state.cuisine_val
    st.session_state["user_dislikes"] = st.session_state.dislikes_val
    
    # NOW we go to the Dashboard
    st.switch_page("pages/4_Dashboard.py")
