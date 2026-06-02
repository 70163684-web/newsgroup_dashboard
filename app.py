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
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .glow-text {
        text-shadow: 0 0 10px rgba(0,242,254,0.6);
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

target_categories = [
    'alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
    'comp.sys.mac.hardware', 'comp.windows.x', 'misc.forsale', 'rec.autos',
    'rec.motorcycles', 'rec.sport.baseball', 'rec.sport.hockey', 'sci.crypt',
    'sci.electronics', 'sci.med', 'sci.space', 'soc.religion.christian',
    'talk.politics.guns', 'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc'
]

# --- 2. CACHED ENGINE DATA GENERATOR ---
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
            'Doc_ID': "Intel_Node_" + str(95000+i) + ".txt", 
            'Category': cat,
            'Content': "Ingestion record reference node code " + str(cat) + ". " + str(sample_logs[i % 4]),
            'Word_Count': w_count, 
            'Sentiment': sentiment, 
            'Sentiment_Score': round(score, 2),
            'Pipeline_Year': int(np.random.choice([2022, 2023, 2024, 2025, 2026])),
            'Processing_Delay_ms': int(np.random.uniform(100, 1200)),
            'Linguistic_Complexity': round(np.random.uniform(10.5, 95.8), 2)
        })
        
    return pd.DataFrame(records)

df = compile_dataset_matrix()

# --- 3. PREMIUM FLOATING NAVIGATION SIDEBAR ---
st.sidebar.markdown("""
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
""", unsafe_allow_html=True)

st.sidebar.write("---")

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
st.sidebar.subheader("🕹️ Control Matrix Filters")

selected_categories = st.sidebar.multiselect("Target Newsgroup Categories", options=target_categories, default=target_categories)
available_sents = ['Positive', 'Neutral', 'Negative']
selected_sentiments = st.sidebar.multiselect("Filter Sentiment Classes", available_sents, default=available_sents)

max_word_found = int(df['Word_Count'].max()) if not df.empty else 50000
chosen_word_range = st.sidebar.slider("Document Word Count Range", 0, max_word_found, (0, max_word_found))

# Ingest Filtering Parameters
if not df.empty:
    working_df = df[
        (df['Category'].isin(selected_categories)) & 
        (df['Sentiment'].isin(selected_sentiments)) & 
        (df['Word_Count'] >= chosen_word_range[0]) & 
        (df['Word_Count'] <= chosen_word_range[1])
    ]
else:
    working_df = pd.DataFrame()

# --- 4. CONDITIONAL SWITCH ROUTER PANEL ---

if selected_page == "01 Executive Overview":
    st.markdown("""
        <div class='premium-card'>
            <span style='color: #00f2fe; font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 1.5px;'>EXECUTIVE OVERVIEW</span>
            <h1 class='glow-text' style='margin-top: 5px; margin-bottom: 10px; font-size: 38px;'>Global Text & Category Intelligence</h1>
            <p style='color: #94a3b8; max-width: 750px; font-size: 14px; margin-bottom: 0;'>
                A futuristic AI-powered command center for NLP text analytics, semantic cluster density patterns, 
                and context distribution across disparate newsgroup tracking modules.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        v1 = "{:,}".format(len(working_df))
        st.markdown("<div class='metric-container'><div style='float: right; color: #00f2fe; font-size: 11px;'>Live Scan</div><div class='metric-label'>Total Documents</div><div class='metric-val'>" + v1 + "</div></div>", unsafe_allow_html=True)
        
        v2 = str(int(working_df['Word_Count'].mean())) if not working_df.empty else "0"
        st.markdown("<div class='metric-container'><div style='float: right; color: #38bdf8; font-size: 11px;'>+1.0% YoY</div><div class='metric-label'>Avg Word Length</div><div class='metric-val'>" + v2 + "</div></div>", unsafe_allow_html=True)
        
    with col2:
        v3 = str(working_df['Category'].nunique() if not working_df.empty else 0)
        st.
