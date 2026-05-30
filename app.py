import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import tarfile
import os
from collections import Counter

# --- 1. PAGE SETUP & STRUCTURE CONTROL ---
st.set_page_config(
    page_title="20-Newsgroups Premium Intelligence Engine",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Style Layout Sheet - Ensuring Visibility & Smooth Rendering
st.markdown("""
    <style>
    .main { background-color: #0b0f19 !important; color: #f3f4f6 !important; }
    h1 { color: #ffffff !important; font-weight: 800 !important; font-size: 34px !important; margin-bottom: 5px !important; }
    h2, h3 { color: #f3f4f6 !important; font-weight: 600 !important; padding-top: 10px; }
    
    .stTabs [data-baseweb="tab"] { color: #9ca3af !important; font-weight: bold !important; font-size: 15px; }
    .stTabs [aria-selected="true"] { color: #38bdf8 !important; border-bottom-color: #38bdf8 !important; }
    
    div[data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: 800 !important;
        color: #38bdf8 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 11px !important;
        color: #9ca3af
