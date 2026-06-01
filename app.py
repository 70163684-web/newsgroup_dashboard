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

# Explicit layout declaration for all 20 categories
target_categories = [
    'alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
    'comp.sys.mac.hardware', 'comp.windows.x', 'misc.forsale', 'rec.autos',
    'rec.motorcycles', 'rec.sport.baseball', 'rec.sport.hockey', 'sci.crypt',
    'sci.electronics', 'sci.med', 'sci.space', 'soc.religion.christian',
    'talk.politics.guns', 'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc'
]

# --- 2. ROBUST DATA PROCESSING ENGINE ---
@st.cache_data(ttl=3600)
def compile_dataset_matrix():
    possible_files = ["20news-bydate.tar.gz", "20news-bydate.tar", "20news-bydate.tat.gz"]
    archive_path = None
    for f_name in possible_files:
        if os.path.exists(f_name):
            archive_path = f_name
            break

    records = []
    if archive_path:
        mode = "r:gz" if "gz" in archive_path else "r:"
        try:
            with tarfile.open(archive_path, mode) as tar:
                limit = 0
                for member in tar.getmembers():
                    if member.isfile() and ("train" in member.name or "test" in member.name):
                        if limit > 3500:
                            break
                        parts = member.name.split('/')
                        if len(parts) >= 3:
                            cat
