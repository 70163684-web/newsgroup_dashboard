import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from collections import Counter

# --- 1. GLOBAL STYLING & CORE ENVIRONMENT ---
st.set_page_config(
    page_title="20-Newsgroups Intelligence Engine",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Cyberpunk Glassmorphism Styles (Gym Nexus Theme Adaptation)
st.markdown("""
    <style>
    .stApp {
        background-color: #030712;
        color: #f3f4f6;
    }
    .premium-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.6) 0%, rgba(30, 41, 59, 0.4) 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .metric-container {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.03);
        border-left: 4px solid #00f2fe;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 15px;
    }
    .metric-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94a3b8;
        margin-bottom: 4px;
    }
    .metric-val {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        font-family: 'Courier New', monospace;
    }
    .metric-sub {
        font-size: 11px;
        color: #00f2fe;
        margin-top: 2px;
    }
    .status-badge {
        background: rgba(34, 197, 94, 0.1);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.2);
        padding:
