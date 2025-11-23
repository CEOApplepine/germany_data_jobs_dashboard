import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# --------------------------
# 1️⃣ Load CSV safely
# --------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("germany_data_jobs_clean.csv")
    
    # Standardize column names to lowercase and replace spaces with underscores
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    
    # Ensure 'apply_link' exists
    if 'apply_link' not in df.columns:
        df['apply_link'] = ""
    
    # Ensure salary_avg exists
    if 'salary_avg' not in df.columns:
        df['salary_avg'] = 0
    
    return df

df = load_data()

# --------------------------
# 2️⃣ Sidebar Filters
# --------------------------
st.sidebar.header("Filter Jobs")

keyword = st.sidebar.text_input("Search by keyword (title/description)")

company_filter = st.sidebar.multiselect(
    "Company", sorted(df["company"].dropna().unique())
)

city_filter = st.sidebar.multiselect(
    "City", sorted(df["location"].dropna().unique())
)

salary_min = st.sidebar.slider(
    "Minimum salary (€)",
    0,
    int(df["salary_avg"].max() if df["salary_avg"].max() > 0 else 100000),
    0
)

# --------------------------
# 3️⃣ Apply Filters
# --------------------------
filtered = df.copy()

if keyword:
    filtered = filtered[
        filtered["title"].str.contains(keyword, case=False, na=False) |
        filtered["description"].str.contains(keyword, case=False, na=False)
    ]

if company_filter:
    filtered = filtered[filtered["company"].isin(company_filter)]

if city_filter:
    filtered = filtered[filtered["location"].isin(city_filter)]

filtered = filtered[filtered["salary_avg"] >= salary_min]

# --------------------------
# 4️⃣ Main Page
# --------------------------
st.title("🇩🇪 Germany Data Jobs Dashboard")
st.write(f"### Showing {len(filtered)} jobs")
st.write("Click 'Apply Now' to open the job link.")

# Display job listings
for i, row in filtered.iterrows():
    st.subheader(row.get("title", "No Title"))
    st.write(f"**Company:** {row.get('company', 'N/A')}")
    st.write(f"**Location:** {row.get('location', 'N/A')}")
    
    salary_min_val = row.get("salary_min", "")
    salary_max_val = row.get("salary_max", "")
    st.write(f"**Salary:** {salary_min_val} - {salary_max_val} €")
    
    st.write(row.get("description", "")[:300] + "...")
    
    link = row.get("apply_link", "")
    if pd.notna(link) and link != "":
        st.markdown(f"[🔗 Apply Now]({link})", unsafe_allow_html=True)
    else:
        st.write("No apply link available")
    
    st.divider()

# --------------------------
# 5️⃣ Visualizations
# --------------------------
st.header("📊 Job Market Analytics")

# Salary Distribution
fig, ax = plt.subplots(figsize=(8,4))
sns.histplot(df[df["salary_avg"]>0]["salary_avg"], kde=True, bins=30, ax=ax)
ax.set_title("Salary Distribution")
st.pyplot(fig)

# Top Cities
st.subheader("Top Cities")
st.bar_chart(df["location"].value_counts().head(10))

# Top Companies
st.subheader("Top Companies Hiring")
st.bar_chart(df["company"].value_counts().head(10))

# Skill WordCloud
st.subheader("Most Frequent Skills")
text = " ".join(df["description"].dropna())
if text.strip() != "":
    wc = WordCloud(width=600, height=300, background_color="white").generate(text)
    st.image(wc.to_array())
else:
    st.write("No job descriptions to generate word cloud")
