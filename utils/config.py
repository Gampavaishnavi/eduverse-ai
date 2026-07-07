import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class Config:
    try:
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
    except Exception:
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    APP_TITLE = "Eduverse AI – Student Decision Intelligence Platform"
    PAGE_ICON = "🎓"
    
    # Thresholds
    ATTENDANCE_THRESHOLD = 75.0
    RISK_HIGH_THRESHOLD = 70.0
    RISK_MEDIUM_THRESHOLD = 40.0
