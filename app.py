import streamlit as st
import pandas as pd
from datetime import date

#page setup
st.set_page_config(page_title="BUSA 521 - Capstone", layout="wide")

#colors
TAMUC_BLUE = "#00386C"
TAMUC_GOLD = "#FFC333"

#CSS header
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

#logo 
logo = st.image("etamulogo.webp", width=150)

#move logo to top left
logo_position_css = """
<style>

section[data-testid="stSidebar"] + div [data-testid="stImage"] img {
    position: absolute;
    top: 10px;
    left: 10px;
    z-index: 9999;
}
</style>
"""
st.markdown(logo_position_css, unsafe_allow_html=True)


#header bar across top
st.markdown(
    "<div class='header-bar'><div class='header-title'>BUSA 521 — Capstone</div></div>",
    unsafe_allow_html=True
)

st.title("DFW Fortune 500 Data Jobs")

st.caption("An interactive dashboard with real job postings.")


#load data
df = pd.read_csv("all_jobs.csv")

#filters
st.markdown(f"<h3 style='color:{TAMUC_BLUE}; margin-bottom:0; font-weight:700;'>Filter Jobs</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.2,1.2,1.6], vertical_alignment="bottom")
with col1:
    company = st.selectbox("Company", ["All"] + sorted(df["Company"].dropna().unique()))
with col2:
    location = st.selectbox("Location", ["All"] + sorted(df["Location"].dropna().unique()))
with col3:
    q = st.text_input("Keyword in job title", placeholder="e.g., analyst, engineer, data")

#filters
filtered = df.copy()
if company != "All":
    filtered = filtered[filtered["Company"] == company]
if location != "All":
    filtered = filtered[filtered["Location"] == location]
if q:
    filtered = filtered[filtered["Title"].str.contains(q, case=False, na=False)]

#kpis
k1, k2, k3 = st.columns(3)
k1.metric("Total Openings", len(filtered))
k2.metric("Companies", filtered["Company"].nunique())
k3.metric("Newest Posting", filtered["Posted On"].iloc[0] if not filtered.empty else "—")

st.divider()

#results
st.subheader("Job Listings")
show_cols = ["Company", "Title", "Location", "Posted On", "Job URL"]

#rename columns
nice_cols = {
    "Company": "Company",
    "Title": "Job Title",
    "Location": "Location",
    "Posted On": "Posted On",
    "Job URL": "Job Link"
}

clean_df = filtered[show_cols].rename(columns=nice_cols)

# format dates
clean_df["Posted Date"] = clean_df["Posted Date"].astype(str)

# Title case job titles
clean_df["Job Title"] = clean_df["Job Title"].str.title()

#show cleaned table
st.data_editor(clean_df, use_container_width=True, hide_index=True, disabled=True)

st.divider()
