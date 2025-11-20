import streamlit as st
import pandas as pd
from datetime import date

# ---------- Page setup ----------
st.set_page_config(page_title="BUSA 521 - Capstone", layout="wide")

# ---- Colors ----
TAMUC_BLUE = "#00386C"
TAMUC_GOLD = "#FFC333"

# ---- CSS for header ----
header_css = """
<style>
.header-bar {{
    background-color: {blue};
    padding: 18px 16px;
    border-bottom: 4px solid {gold};
}}
.header-title {{
    color: white;
    font-size: 28px;
    font-weight: 700;
    margin: 0;
}}
</style>
""".format(blue=TAMUC_BLUE, gold=TAMUC_GOLD)

st.markdown(header_css, unsafe_allow_html=True)

logo_css = """
<style>
.top-logo {
    position: absolute;
    top: 10px;
    left: 10px;
    height: 60px;
    z-index: 9999;
}
</style>
"""
st.markdown(logo_css, unsafe_allow_html=True)

st.markdown(
    "<img src='etamulogo.webp' class='top-logo'>",
    unsafe_allow_html=True
)


#header bar across top
st.markdown(
    "<div class='header-bar'><div class='header-title'>BUSA 521 — Capstone</div></div>",
    unsafe_allow_html=True
)

st.title("DFW Fortune 500 Data Jobs")

st.caption("An interactive dashboard with real job postings.")


#fake data
data = {
    "company_name": ["PepsiCo","AT&T","American Airlines","ExxonMobil","Texas Instruments",
                     "PepsiCo","AT&T","ExxonMobil","Texas Instruments","American Airlines"],
    "job_title": ["Data Analyst","BI Engineer","Data Scientist","Analytics Manager","BI Developer",
                  "Senior Data Analyst","Report Analyst","Data Engineer","Analytics Lead","Data Visualization Analyst"],
    "location": ["Plano, TX","Dallas, TX","Fort Worth, TX","Irving, TX","Dallas, TX",
                 "Plano, TX","Dallas, TX","Houston, TX","Dallas, TX","Fort Worth, TX"],
    "work_type": ["Hybrid","On-site","Remote","Hybrid","Remote",
                  "Hybrid","On-site","Hybrid","Remote","Hybrid"],
    "posted_date": [
        "2025-10-10","2025-10-09","2025-10-08","2025-10-08","2025-10-07",
        "2025-10-06","2025-10-06","2025-10-05","2025-10-05","2025-10-04"
    ],
    "job_link": [
        "https://careers.pepsico.com",
        "https://att.jobs",
        "https://jobs.aa.com",
        "https://jobs.exxonmobil.com",
        "https://careers.ti.com",
        "https://careers.pepsico.com",
        "https://att.jobs",
        "https://jobs.exxonmobil.com",
        "https://careers.ti.com",
        "https://jobs.aa.com"
    ]
}
df = pd.DataFrame(data)
df["posted_date"] = pd.to_datetime(df["posted_date"]).dt.date

st.markdown(f"<h3 style='color:{TAMUC_BLUE}; margin-bottom:0; font-weight:700;'>Filter Jobs</h3>", unsafe_allow_html=True)

#filters
col1, col2, col3, col4 = st.columns([1.2,1.2,1.2,1.6], vertical_alignment="bottom")
with col1:
    company = st.selectbox("Company", ["All"] + sorted(df["company_name"].unique()))
with col2:
    location = st.selectbox("Location", ["All"] + sorted(df["location"].unique()))
with col3:
    work = st.selectbox("Work Type", ["All"] + sorted(df["work_type"].unique()))
with col4:
    q = st.text_input("Keyword in job title", placeholder="e.g., analyst, engineer, viz")

#filters
filtered = df.copy()
if company != "All":
    filtered = filtered[filtered.company_name == company]
if location != "All":
    filtered = filtered[filtered.location == location]
if work != "All":
    filtered = filtered[filtered.work_type == work]
if q:
    filtered = filtered[filtered.job_title.str.contains(q, case=False, na=False)]

#kpis
k1, k2, k3 = st.columns(3)
k1.metric("Total Openings (filtered)", len(filtered))
k2.metric("Companies (filtered)", filtered["company_name"].nunique())
k3.metric("Newest Posting", str(filtered["posted_date"].max()) if not filtered.empty else "—")

st.divider()

#results
st.subheader("Job Listings")
show_cols = ["company_name","job_title","location","work_type","posted_date","job_link"]
st.dataframe(filtered[show_cols], use_container_width=True, hide_index=True)


st.divider()
