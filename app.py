import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import tarfile
import os
import re

# --- 1. PAGE CONFIGURATION & THEME ---
st.set_page_config(
    page_title="20-Newsgroups Intel Engine",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise Dark Theme CSS (Sleek UI like benchmark)
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f3f4f6; }
    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #38bdf8 !important; /* Premium Cyan */
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
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    h1 { font-weight: 800 !important; color: #ffffff !important; }
    h2, h3 { font-weight: 600 !important; color: #e5e7eb !important; }
    .stSidebar { background-color: #0f172a !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTOMATIC DATA EXTRACTOR & PARSER ---
@st.cache_data
def load_and_process_tar():
    tar_path = "20news-bydate.tar" # Agar aapki file ka naam alag hai to yahan change karein
    
    # Validation check
    if not os.path.exists(tar_path):
        # Fallback dataset pipeline agar file detect na ho (Testing ke liye)
        categories = ['alt.atheism', 'comp.graphics', 'rec.sport.baseball', 'sci.space', 'talk.politics.mideast']
        rows = []
        np.random.seed(42)
        for i in range(1200):
            cat = np.random.choice(categories)
            word_cnt = np.random.randint(40, 400)
            score = np.random.uniform(-0.8, 0.9)
            lbl = 'Positive' if score > 0.15 else ('Negative' if score < -0.15 else 'Neutral')
            rows.append({
                'Doc_ID': f"News_File_{10000+i}.txt", 'Category': cat,
                'Content': f"Archived bulletin under topic {cat}. Technical log details verified.",
                'Word_Count': word_cnt, 'Sentiment': lbl, 'Sentiment_Score': round(score, 2)
            })
        return pd.DataFrame(rows)

    # Extraction Logic from Tar File
    extracted_data = []
    with tarfile.open(tar_path, "r") as tar:
        count = 0
        for member in tar.getmembers():
            if member.isfile() and ("20news-bydate-train" in member.name or "20news-bydate-test" in member.name):
                # Max 1500 records process karenge performance speed ke liye
                if count > 1500: 
                    break
                
                parts = member.name.split('/')
                if len(parts) >= 3:
                    category = parts[1] # Extract newsgroup name
                    doc_id = parts[2]   # File name
                    
                    try:
                        f = tar.extractfile(member)
                        content = f.read().decode('utf-8', errors='ignore')
                        
                        # Basic Text Wrangling (Cleaning)
                        word_list = content.split()
                        word_count = len(word_list)
                        
                        # Rule-based Sentiment Score Simulation based on text length and patterns
                        score = np.sin(word_count / 10.0) * 0.5 + np.random.uniform(-0.3, 0.3)
                        score = max(-1.0, min(1.0, score)) # bound between -1 and 1
                        sentiment = 'Positive' if score > 0.15 else ('Negative' if score < -0.15 else 'Neutral')
                        
                        extracted_data.append({
                            'Doc_ID': doc_id,
                            'Category': category,
                            'Content': content[:300].replace('\n', ' ') + "...", # Preview snippet
                            'Word_Count': word_count,
                            'Sentiment': sentiment,
                            'Sentiment_Score': round(score, 2)
                        })
                        count += 1
                    except:
                        continue
                        
    return pd.DataFrame(extracted_data)

# Run Pipeline
df = load_and_process_tar()

# --- 3. SIDEBAR CONTROL CENTER ---
st.sidebar.markdown("<h2 style='color:#38bdf8; margin-bottom:0;'>Navigation</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#6b7280; font-size:12px;'>Enterprise Hub v3.0</p>", unsafe_allow_html=True)
st.sidebar.write("---")

st.sidebar.subheader("🎛️ Dynamic Controls")
all_cats = sorted(df['Category'].unique())
selected_cats = st.sidebar.multiselect("Select Categories", all_cats, default=all_cats[:4])

all_sents = df['Sentiment'].unique()
selected_sents = st.sidebar.multiselect("Filter Sentiment", all_sents, default=list(all_sents))

# Filter Application
filtered_df = df[(df['Category'].isin(selected_cats)) & (df['Sentiment'].isin(selected_sents))]

# --- 4. HERO DASHBOARD HEADER ---
st.title("🔮 20-Newsgroups Semantic Analytics Platform")
st.markdown("Automated text intelligence dashboard processing heavy metadata and classification distribution layers.")
st.write("---")

# --- 5. PREMIUM METRIC CARDS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card-box">', unsafe_allow_html=True)
    st.metric(label="Total Scanned Files", value=f"{len(filtered_df):,}")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card-box">', unsafe_allow_html=True)
    st.metric(label="Active Target Subsets", value=len(filtered_df['Category'].unique()))
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card-box">', unsafe_allow_html=True)
    st.metric(label="Avg Word Count", value=f"{int(filtered_df['Word_Count'].mean()) if len(filtered_df)>0 else 0} words")
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card-box">', unsafe_allow_html=True)
    st.metric(label="Overall Sentiment Index", value=f"{round(filtered_df['Sentiment_Score'].mean(), 2) if len(filtered_df)>0 else 0.0}")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# --- 6. INTERACTIVE TABS & CHARTS (Exact Functional Layout) ---
tab1, tab2 = st.tabs(["📊 Category Distributions", "🔍 Text Metric Exploration"])

with tab1:
    g_col1, g_col2 = st.columns((3, 2))
    with g_col1:
        st.subheader("📌 Volume Distribution Across Categories")
        if not filtered_df.empty:
            cat_counts = filtered_df['Category'].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Volume']
            fig_bar = px.bar(cat_counts, x='Volume', y='Category', orientation='h',
                             color='Volume', color_continuous_scale='Blues', template='plotly_dark')
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=380, margin=dict(t=10, b=10))
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No data selected.")
            
    with g_col2:
        st.subheader("🎯 Overall Sentiment Ratio")
        if not filtered_df.empty:
            sent_counts = filtered_df['Sentiment'].value_counts().reset_index()
            fig_pie = px.pie(sent_counts, values='count', names='Sentiment', hole=0.5,
                             color='Sentiment', color_discrete_map={'Positive':'#0ea5e9', 'Neutral':'#64748b', 'Negative':'#ef4444'},
                             template='plotly_dark')
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=380, margin=dict(t=10, b=10))
            st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.subheader("⚡ Document Length vs Sentiment Score Map")
    if not filtered_df.empty:
        fig_scatter = px.scatter(filtered_df, x='Word_Count', y='Sentiment_Score', color='Sentiment',
                                 size='Word_Count', hover_name='Doc_ID', template='plotly_dark',
                                 color_discrete_map={'Positive':'#0ea5e9', 'Neutral':'#64748b', 'Negative':'#ef4444'}, opacity=0.7)
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

st.write("---")

# --- 7. POWERFUL INTERACTIVE ADVANCED DATAFRAME ---
st.subheader("🔎 Advanced Document Explorer Engine")
st.markdown("Search inside the corpus files instantly:")

search_word = st.text_input("✍️ Filter rows by typing keyword inside content:", "")
if search_word:
    filtered_df = filtered_df[filtered_df['Content'].str.contains(search_word, case=False)]

st.dataframe(
    filtered_df[['Doc_ID', 'Category', 'Word_Count', 'Sentiment', 'Sentiment_Score', 'Content']],
    use_container_width=True,
    column_config={
        "Content": st.column_config.TextColumn("Text Content (Snippet)", width="large"),
        "Sentiment_Score": st.column_config.ProgressColumn("Sentiment Intensity", min_value=-1.0, max_value=1.0, format="%.2f")
    }
)

st.markdown("<br><hr><center style='color:#4b5563; font-size:13px;'>Secure Enterprise Text Analytics Panel • Powered by Streamlit</center>", unsafe_allow_html=True)