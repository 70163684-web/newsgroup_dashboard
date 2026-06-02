import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from collections import Counter

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EDA — 20-Newsgroups Intelligence Engine",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# All 20 categories explicitly registered to secure 20/20 data flow
target_categories = [
    'alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
    'comp.sys.mac.hardware', 'comp.windows.x', 'misc.forsale', 'rec.autos',
    'rec.motorcycles', 'rec.sport.baseball', 'rec.sport.hockey', 'sci.crypt',
    'sci.electronics', 'sci.med', 'sci.space', 'soc.religion.christian',
    'talk.politics.guns', 'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc'
]

# --- 2. DYNAMIC WORKSPACE SYNTHESIZER ---
@st.cache_data(ttl=3600)
def compile_dataset_matrix():
    records = []
    np.random.seed(42)
    
    sample_logs = [
        "System diagnostics active. Token classification subsystem cleared.",
        "Encryption module load success. Security keys registered.",
        "Graphics pipeline buffer overflow on hardware allocation module.",
        "Database handshake protocol established successfully."
    ]
    
    # Generate high volume data matrices for balanced distribution
    for i in range(4000):
        cat = target_categories[i % 20]
        w_count = int(np.random.normal(loc=2200, scale=650))
        if w_count < 10: w_count = 10
            
        score = np.random.uniform(-0.85, 0.85)
        
        if score > 0.15:
            sentiment = 'Positive'
        elif score < -0.15:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        records.append({
            'Doc_ID': f"Intel_Node_{95000+i}.txt", 
            'Category': cat,
            'Content': f"Ingestion record reference node code {cat}. {sample_logs[i % 4]}",
            'Word_Count': w_count, 
            'Sentiment': sentiment, 
            'Sentiment_Score': round(score, 2),
            'Timestamp_Year': int(np.random.choice([2022, 2023, 2024, 2025, 2026]))
        })
        
    return pd.DataFrame(records)

df = compile_dataset_matrix()

# --- 3. PREMIUM SIDEBAR NAVIGATION HUB ---
st.sidebar.markdown(
    """
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 5px;">
        <div style="background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); 
                    width: 42px; height: 42px; border-radius: 12px; 
                    display: flex; align-items: center; justify-content: center; 
                    font-weight: bold; color: black; font-size: 16px; box-shadow: 0 4px 15px rgba(0,242,254,0.3);">
            AI
        </div>
        <div>
            <h3 style="margin: 0; padding: 0; font-size: 20px; letter-spacing: 0.5px; color: #ffffff;">20-NEWSGROUPS</h3>
            <p style="margin: 0; padding: 0; font-size: 11px; color: #a1a1aa;">Global Intelligence Engine</p>
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)

st.sidebar.write("---")

# 10 Points exact interface alignment
navigation_options = [
    "01 Executive Overview",
    "02 Global Newsgroup Analytics",
    "03 Sentiment Intelligence",
    "04 Category Comparison Matrix",
    "05 Word & Density Analytics",
    "06 Linguistic Trends Explorer",
    "07 AI Insights Center",
    "08 Predictive Analytics Hub",
    "09 Regional Distribution Matrix",
    "10 Settings & Themes Control"
]

selected_page = st.sidebar.radio(
    "SELECT VIEWING PORTAL",
    options=navigation_options,
    label_visibility="collapsed"
)

st.sidebar.write("---")
st.sidebar.subheader("🕹️ Control Matrix Filters
