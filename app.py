import streamlit as st
import pandas as pd
from datetime import date

# ---------- Page setup ----------
st.set_page_config(page_title="DFW Fortune 500 Data Jobs", layout="wide")
# ---------- Improved TAMUC CSS ----------
TAMUC_BLUE = "#00386C"
TAMUC_GOLD = "#FFC333"
LIGHT_BG = "#F5F7FA"
CARD_BORDER = "#E2E8F0"

st.markdown(f"""
<style>

    /* GLOBAL PAGE BACKGROUND */
    .stApp {{
        background-color: {LIGHT_BG};
    }}

    /* TITLE */
    h1 {{
        color: {TAMUC_BLUE} !important;
        font-weight: 700 !important;
        border-left: 10px solid {TAMUC_GOLD};
        padding-left: 15px;
        margin-bottom: 5px;
    }}

    /* CAPTION */
    .stCaption, .stMarkdown {{
        color: #333333 !important;
    }}

    /* FILTER LABELS */
    label {{
        color: {TAMUC_BLUE} !important;
        font-weight: 600 !important;
    }}

    /* KPI METRICS */
    [data-testid="stMetricValue"] {{
        color: {TAMUC_BLUE} !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: #444444 !important;
    }}

    /* JOB CARDS (for later if you switch from dataframe) */
    .job-card {{
        background-color: white;
        border: 1px solid {CARD_BORDER};
        border-radius: 10px;
        padding: 15px 20px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }}
    .job-title {{
        color: {TAMUC_BLUE};
        font-size: 20px;
        font-weight: 700;
    }}
    .company-text {{
        color: #2B2B2B;
        font-size: 16px;
        font-weight: 600;
    }}
    .job-link {{
        color: {TAMUC_GOLD} !important;
        font-weight: 600;
        text-decoration: none;
    }}
    .job-link:hover {{
        text-decoration: underline;
    }}

</style>
""", unsafe_allow_html=True)
