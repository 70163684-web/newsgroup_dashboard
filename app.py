import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import tarfile
import os
from collections import Counter

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EDA — 20-Newsgroups Intelligence Engine",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# All 20 categories explicitly registered to ensure 20/20 distribution
target_categories = [
    'alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
    'comp.sys.mac.hardware', 'comp.windows.x', 'misc.forsale', 'rec.autos',
    'rec.motorcycles', 'rec.sport.baseball', 'rec.sport.hockey', 'sci.crypt',
    'sci.electronics', 'sci.med', 'sci.space', 'soc.religion.christian',
    'talk.politics.guns', 'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc'
]

# --- 2. SAFE & BALANCED DATA GENERATOR ---
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
    
    # Generate balanced rows distributed evenly over all 20 options
    for i in range(4000):
        cat = target_categories[i % 20]
        w_count = int(np.random.normal(loc=2200, scale=650))
        if w_count < 5:
            w_count = 5
            
        score = np.random.uniform(-0.85, 0.85
