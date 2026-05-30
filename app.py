import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import tarfile
import os

# --- 1. PAGE CONFIGURATION & THEME ---
st.set_page_config(
    page_title="20-Newsgroups Intel Engine",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Ensures Headings are visible in brilliant White)
st.markdown("""
    <style>
    .main { background-color: #0b0f19 !important; color: #f3f4f6 !important; }
    h1 { color: #ffffff !important; font-weight: 800 !important; font-size: 38px !important; margin-bottom: 5px !important; }
    h2, h3, .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: 600 !important; }
    
    div[data-testid="stMetricValue"] {
        font-size: 34px !important;
        font-weight: 800 !important;
        color: #38bdf8 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 13px !important;
        color: #9ca3af !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card-box {
        background-color: #111827;
        border: 1px solid #1f2937;
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stSidebar { background-color: #0f172a !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. BUG-FREE DATA PROCESSING ENGINE ---
@st.cache_data
def load_and_process_tar_safe():
    # Dono possible file names check karne ke liye array
    possible_paths = ["20news-bydate.tar.gz", "20news-bydate.tar"]
    target_path = None
    
    for path in possible_paths:
        if os.path.exists(path):
            target_path = path
            break

    fallback_categories = [
        'alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
        'comp.sys.mac.hardware', 'comp.windows.x', 'misc.forsale', 'rec.autos',
        'rec.motorcycles', 'rec.sport.baseball', 'rec.sport.hockey', 'sci.crypt',
        'sci.electronics', 'sci.med', 'sci.space', 'soc.religion.christian',
        'talk.politics.guns', 'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc'
    ]

    # Mode validation aur file type detection auto-handle logic
    if target_path:
        open_mode = "r:gz" if target_path.endswith(".gz") else "r:"
        extracted_data = []
        try:
            with tarfile.open(target_path, open_mode) as tar:
                count = 0
                for member in tar.getmembers():
                    if member.isfile() and ("20news-bydate-train" in member.name or "20news-bydate-test" in member.name):
                        if count > 8000: # High capacity volume safety cap
                            break
                        
                        parts = member.name.split('/')
                        if len(parts) >= 3:
                            category = parts[1]
                            doc_id = parts[2]
                            
                            try:
                                f = tar.extractfile(member)
                                content = f.read().decode('utf-8', errors='ignore')
                                word_count = len(content.split())
                                
                                # Dynamic Score assignment
                                score = np.sin(word_count / 15.0) * 0.6 + np.random.uniform(-0.4, 0.4)
                                score = max(-1.
