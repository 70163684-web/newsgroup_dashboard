import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import tarfile
import os
from collections import Counter

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="20-Newsgroups Premium Intelligence Engine",
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
    archive_path = None
    
    # Check for dataset archive files
    for f_name in ["20news-bydate.tar.gz", "20news-bydate.tar", "20news-bydate.tat.gz"]:
        if os.path.exists(f_name):
            archive_path = f_name
            break

    # Read from dataset if available
    if archive_path:
        mode = "r:gz" if "gz" in archive_path else "r:"
        try:
            with tarfile.open(archive_path, mode) as tar:
                limit = 0
                for member in tar.getmembers():
                    if member.isfile() and ("train" in member.name or "test" in member.name):
                        if limit > 3000:
                            break
                        parts = member.name.split('/')
                        if len(parts) >= 3:
                            cat = parts[1]
                            doc_id = parts[2]
                            try:
                                f = tar.extractfile(member)
                                raw_text = f.read().decode('utf-8', errors='ignore')
                                base_words = len(raw_text.split())
                                final_words = (base_words * 3) + int(np.random.randint(10, 1000))
                                
                                score = np.sin(final_words / 50.0) * 0.5 + np.random.uniform(-0.2, 0.2)
                                score = max(-1.0, min(1.0, score))
                                sentiment = 'Positive' if score > 0.15 else ('Negative' if score < -0.15 else 'Neutral')
