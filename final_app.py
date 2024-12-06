from final_app_homepage import homepage
from final_app_survival import survival_dashboard
import streamlit as st
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="Breast Cancer Insights", page_icon="🔬", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Home"

if st.session_state.page == 'Home':
    homepage()
elif st.session_state.page == 'Dashboard':
    survival_dashboard()