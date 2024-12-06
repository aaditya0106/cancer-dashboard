import streamlit as st
from streamlit_lottie import st_lottie
import json

def load_lottie_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def homepage():
    lottie_cancer_animation = load_lottie_file("lottie.json")
    
    with st.container():
        col1, col2 = st.columns([2, 3])

        with col1:
            st.title("Breast Cancer Insights")
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            st.markdown(
                """
                Explore key insights, trends, and analytics in the breast cancer research. 
                Dive into the data and uncover meaningful insights to make informed decisions.
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div style='margin-top: 150px;'></div>", unsafe_allow_html=True)
            if st.button("Go to Dashboard"):
                st.session_state.page = 'Dashboard'
                st.experimental_rerun()

        with col2:
            if lottie_cancer_animation:
                st_lottie(lottie_cancer_animation, height=500)
            else:
                st.error("Error loading animation. Please check the file.")
