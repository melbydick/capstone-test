import streamlit as st
import pandas as pd
from datetime import date

# ---------- Page setup ----------
st.set_page_config(page_title="DFW Fortune 500 Data Jobs", layout="wide")
st.title("BUSA 521 — Prototype")
st.caption("Demo with mock job listings.")

# ---- Simple theme accents (tweak these!) ----
ACCENT = "#00386C"    #blue
BG_GRAD_A = "#FFC333" #gold
BG_GRAD_B = "#000000" # slate-800

# ---- CSS: gradient header, pills, cards, buttons ----
st.markdown(f"""
<style>
/* Page background */
.stApp {{
  background: linear-gradient(180deg, {BG_GRAD_A} 0%, {BG_GRAD_B} 10%, #0b1220 100%);
  color: #FFC333;
}}
</style>
""", unsafe_allow_html=True)


# ---------- Fake dataset (swap this later) ----------
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


# ---------- Filters ----------
col1, col2, col3, col4 = st.columns([1.2,1.2,1.2,1.6], vertical_alignment="bottom")
with col1:
    company = st.selectbox("Company", ["All"] + sorted(df["company_name"].unique()))
with col2:
    location = st.selectbox("Location", ["All"] + sorted(df["location"].unique()))
with col3:
    work = st.selectbox("Work Type", ["All"] + sorted(df["work_type"].unique()))
with col4:
    q = st.text_input("Keyword in job title", placeholder="e.g., analyst, engineer, viz")

# ---------- Apply filters ----------
filtered = df.copy()
if company != "All":
    filtered = filtered[filtered.company_name == company]
if location != "All":
    filtered = filtered[filtered.location == location]
if work != "All":
    filtered = filtered[filtered.work_type == work]
if q:
    filtered = filtered[filtered.job_title.str.contains(q, case=False, na=False)]

# ---------- KPIs ----------
k1, k2, k3 = st.columns(3)
k1.metric("Total Openings (filtered)", len(filtered))
k2.metric("Companies (filtered)", filtered["company_name"].nunique())
k3.metric("Newest Posting", str(filtered["posted_date"].max()) if not filtered.empty else "—")

st.divider()

# ---------- Results table ----------
st.subheader("Job Listings")
show_cols = ["company_name","job_title","location","work_type","posted_date","job_link"]
st.dataframe(filtered[show_cols], use_container_width=True)

st.divider()


