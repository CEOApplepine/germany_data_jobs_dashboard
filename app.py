import streamlit as st
import pandas as pd

# --------------------------
# 1️⃣ Page Config
# --------------------------
st.set_page_config(page_title="Germany Data Jobs", layout="wide")

st.title("🇩🇪 Data Jobs in Germany")
st.markdown("Search and explore recent data-related job postings across Germany. Click 'Apply Now' to visit the job page.")

# --------------------------
# 2️⃣ Load CSV
# --------------------------
try:
    df = pd.read_csv("germany_data_jobs_clean.csv")
except FileNotFoundError:
    st.error("CSV file not found. Please generate germany_data_jobs_clean.csv first.")
    st.stop()

# --------------------------
# 3️⃣ Search Bar
# --------------------------
search_term = st.text_input("🔍 Search jobs by Title, Company, or Location")

filtered_df = df.copy()
if search_term:
    mask = (
        df['title'].str.contains(search_term, case=False, na=False) |
        df['company'].str.contains(search_term, case=False, na=False) |
        df['location'].str.contains(search_term, case=False, na=False)
    )
    filtered_df = df[mask]

# Optional: salary filter
salary_filter = st.selectbox("Show Salary", ["All", "Confidential only", "Known only"])
if salary_filter == "Confidential only":
    filtered_df = filtered_df[filtered_df["salary"] == "Confidential"]
elif salary_filter == "Known only":
    filtered_df = filtered_df[filtered_df["salary"] != "Confidential"]

# --------------------------
# 4️⃣ Display Jobs
# --------------------------
st.subheader(f"Showing {len(filtered_df)} jobs")

for idx, row in filtered_df.iterrows():
    st.markdown(f"### {row['title']}")
    st.write(f"**Company:** {row['company']}")
    st.write(f"**Location:** {row['location']}")
    st.write(f"**Salary:** {row['salary']}")
    st.write(f"**Date Posted:** {row['date_posted']}")
    
    # Apply link as a button
    st.markdown(f"[🔗 Apply Now]({row['apply_link']})", unsafe_allow_html=True)
    st.markdown("---")

# --------------------------
# 5️⃣ Optional: Show Raw Data
# --------------------------
with st.expander("Show raw data"):
    st.dataframe(filtered_df)
