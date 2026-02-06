import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import io

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Enterprise Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# THEME TOGGLE
# =========================================================
theme = st.sidebar.radio("🎨 Theme", ["Light Mode", "Dark Mode"])

if theme == "Dark Mode":
    bg_color = "#0e1117"
    card_color = "#161b22"
    text_color = "#ffffff"
else:
    bg_color = "#f5f7fb"
    card_color = "#ffffff"
    text_color = "#000000"

# =========================================================
# CUSTOM CSS (MNC LOOK)
# =========================================================
st.markdown(f"""
<style>
body {{
    background-color: {bg_color};
    color: {text_color};
}}

.metric-card {{
    background-color: {card_color};
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    text-align: center;
    transition: transform 0.2s ease-in-out;
}}

.metric-card:hover {{
    transform: scale(1.05);
}}

.metric-title {{
    font-size: 15px;
    color: gray;
}}

.metric-value {{
    font-size: 32px;
    font-weight: bold;
    color: #1f77b4;
}}

.section-title {{
    font-size: 26px;
    font-weight: 600;
    margin-top: 20px;
}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    return pd.read_csv("dataset_cleaned_full.csv")

df = load_data()

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

# =========================================================
# HEADER
# =========================================================
st.markdown("## 🏢 Enterprise Data Analytics Platform")
st.markdown(
    "##### Advanced insights • Executive dashboards • Data-driven decisions"
)

# =========================================================
# KPI DASHBOARD
# =========================================================
st.markdown("### 📌 Executive KPIs")

k1, k2, k3, k4 = st.columns(4)

kpis = [
    ("Total Records", f"{df.shape[0]:,}"),
    ("Numeric Features", len(numeric_cols)),
    ("Categorical Features", len(categorical_cols)),
    ("Missing Values", int(df.isnull().sum().sum()))
]

for col, (title, value) in zip([k1, k2, k3, k4], kpis):
    col.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# =========================================================
# NAVIGATION
# =========================================================
st.sidebar.title("📂 Dashboard Sections")
section = st.sidebar.selectbox(
    "Navigate",
    [
        "Overview",
        "Distributions",
        "Correlation Analysis",
        "Category Comparison",
        "Relationships",
        "Data Download"
    ]
)

# =========================================================
# OVERVIEW
# =========================================================
if section == "Overview":
    st.markdown('<div class="section-title">Dataset Overview</div>', unsafe_allow_html=True)
    st.dataframe(df.head(15), use_container_width=True)

# =========================================================
# DISTRIBUTIONS
# =========================================================
elif section == "Distributions":
    st.markdown('<div class="section-title">Distribution & Outlier Analysis</div>', unsafe_allow_html=True)

    col = st.selectbox("Select Numeric Feature", numeric_cols)

    fig1, ax1 = plt.subplots()
    sns.histplot(df[col], kde=True, bins=30, ax=ax1)
    ax1.set_title(f"Distribution of {col}")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    sns.boxplot(x=df[col], ax=ax2)
    ax2.set_title(f"Outliers in {col}")
    st.pyplot(fig2)

# =========================================================
# CORRELATION
# =========================================================
elif section == "Correlation Analysis":
    st.markdown('<div class="section-title">Correlation Intelligence</div>', unsafe_allow_html=True)

    corr = df[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(corr, cmap="coolwarm", linewidths=0.4, ax=ax)
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)

# =========================================================
# CATEGORY COMPARISON
# =========================================================
elif section == "Category Comparison":
    st.markdown('<div class="section-title">Category-Based Insights</div>', unsafe_allow_html=True)

    cat = st.selectbox("Category", categorical_cols)
    num = st.selectbox("Metric", numeric_cols)

    fig, ax = plt.subplots()
    sns.boxplot(x=df[cat], y=df[num], palette="Set2", ax=ax)
    ax.set_title(f"{num} by {cat}")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# =========================================================
# RELATIONSHIPS
# =========================================================
elif section == "Relationships":
    st.markdown('<div class="section-title">Variable Relationships</div>', unsafe_allow_html=True)

    x = st.selectbox("X Axis", numeric_cols)
    y = st.selectbox("Y Axis", numeric_cols, index=1)

    fig, ax = plt.subplots()
    sns.scatterplot(x=df[x], y=df[y], alpha=0.7, ax=ax)
    ax.set_title(f"{x} vs {y}")
    st.pyplot(fig)

# =========================================================
# DOWNLOADS
# =========================================================
elif section == "Data Download":
    st.markdown('<div class="section-title">Download Center</div>', unsafe_allow_html=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Cleaned Dataset",
        data=csv,
        file_name="dataset_cleaned_full.csv",
        mime="text/csv"
    )

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown(
    "<center>© 2025 Enterprise Analytics Platform | Powered by Streamlit</center>",
    unsafe_allow_html=True
)
