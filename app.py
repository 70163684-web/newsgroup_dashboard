import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Enterprise Text Analytics Panel",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Styling
st.markdown("""
<style>
    .reportview-container { background: #f8fafc; }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border-left: 5px solid #3b82f6;
    }
</style>
""", unsafe_html=True)

# 2. Mock Data Generation (For demonstration)
@st.cache_data
def load_data():
    np.random.seed(42)
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports']
    sentiments = ['Positive', 'Negative', 'Neutral']
    
    data = {
        'Doc_ID': [f"DOC_{i:03d}" for i in range(1, 101)],
        'Category': np.random.choice(categories, 100),
        'Word_Count': np.random.randint(50, 800, 100),
        'Sentiment': np.random.choice(sentiments, 100, p=[0.5, 0.3, 0.2]),
        'Sentiment_Score': np.random.uniform(-1.0, 1.0, 100)
    }
    return pd.DataFrame(data)

df = load_data()

# 3. Sidebar Filters
st.sidebar.title("🔍 Analytics Filters")
st.sidebar.markdown("---")

all_categories = sorted(df['Category'].unique())
selected_categories = st.sidebar.multiselect(
    "Select Categories", 
    options=all_categories, 
    default=all_categories
)

min_words, max_words = int(df['Word_Count'].min()), int(df['Word_Count'].max())
selected_word_range = st.sidebar.slider(
    "Word Count Range",
    min_value=min_words,
    max_value=max_words,
    value=(min_words, max_words)
)

# Filtering Data
filtered_df = df[
    (df['Category'].isin(selected_categories)) & 
    (df['Word_Count'].between(selected_word_range[0], selected_word_range[1]))
]

# 4. Header Section
st.title("📊 Enterprise Text Analytics Dashboard")
st.markdown("Real-time sentiment and document metrics distribution panel.")
st.markdown("---")

# 5. KPI Metrics Row
if not filtered_df.empty:
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    with m_col1:
        st.metric("Total Documents", len(filtered_df))
    with m_col2:
        st.metric("Avg Word Count", f"{int(filtered_df['Word_Count'].mean())} words")
    with m_col3:
        pos_pct = (filtered_df['Sentiment'] == 'Positive').sum() / len(filtered_df) * 100
        st.metric("Positive Sentiment", f"{pos_pct:.1f}%")
    with m_col4:
        avg_score = filtered_df['Sentiment_Score'].mean()
        st.metric("Avg Sentiment Score", f"{avg_score:.2f}")
else:
    st.warning("⚠️ No data available for the selected filters.")

st.markdown("<br>", unsafe_html=True)

# 6. Main Dashboard Tabs
tab1, tab2 = st.tabs(["📊 Overview Analysis", "⚡ Advanced Distribution"])

with tab1:
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        st.subheader("📁 Category Distribution")
        if not filtered_df.empty:
            fig_bar = px.histogram(
                filtered_df, 
                x="Category", 
                color="Sentiment",
                barmode="group",
                color_discrete_map={'Positive': '#0ea5e9', 'Negative': '#ef4444', 'Neutral': '#6b7280'}
            )
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, width='stretch')
        else:
            st.info("No data to display chart.")
            
    with g_col2:
        st.subheader("🎭 Sentiment Breakdown")
        if not filtered_df.empty:
            fig_pie = px.pie(
                filtered_df, 
                names="Sentiment",
                color="Sentiment",
                color_discrete_map={'Positive': '#0ea5e9', 'Negative': '#ef4444', 'Neutral': '#6b7280'}
            )
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, width='stretch')
        else:
            st.info("No data to display chart.")

with tab2:
    st.subheader("⚡ Document Length vs Sentiment Distribution Matrix")
    if not filtered_df.empty:
        # FIX: Dynamic mapping to avoid KeyError if any sentiment group is missing in filtered data
        available_sentiments = filtered_df['Sentiment'].unique()
        full_color_map = {'Positive': '#0ea5e9', 'Negative': '#ef4444', 'Neutral': '#6b7280'}
        current_map = {k: v for k, v in full_color_map.items() if k in available_sentiments}
        
        fig_scatter = px.scatter(
            filtered_df, 
            x='Word_Count', 
            y='Sentiment_Score',
            size='Word_Count', 
            hover_name='Doc_ID',
            color='Sentiment',
            color_discrete_map=current_map
        )
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scatter, width='stretch')
    else:
        st.info("No data available to plot scatter matrix.")

# 7. Data Preview Section
st.markdown("---")
st.subheader("📋 Filtered Dataset Preview")
if not filtered_df.empty:
    st.dataframe(filtered_df, width=1500)
else:
    st.info("Dataset is empty based on your sidebar filters.")

# Footer
st.markdown("<br><hr><center style='color:#4b5563; font-size:13px;'>Secure Enterprise Text Analytics Panel • Powered by Streamlit</center>", unsafe_html=True)
