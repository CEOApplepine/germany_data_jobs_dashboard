# Germany Data Jobs Dashboard

This project collects data-related job postings in Germany and visualizes them in an interactive dashboard using **Streamlit**. It uses the **Adzuna Jobs API** to fetch job listings with details like job title, company, location, salary, description, and apply links.

https://germanydatajobsdashboard-nfemcixshxx4wcdra6sjnc.streamlit.app/


---

## **Features**

- Fetches jobs from **Adzuna API** for Germany with the search term "data".  
- Collects the following details for each job:  
  - Job Title  
  - Company Name  
  - Location  
  - Salary (or "Confidential" if not provided)  
  - Date Posted  
  - Apply Link (direct link to job posting)  
  - Job Description  
- Generates a **clean CSV** (`germany_data_jobs_clean.csv`) for further analysis.  
- Interactive **Streamlit dashboard** to:  
  - Search jobs by **title, company, or location**  
  - Filter jobs by salary visibility (Known/Confidential/All)  
  - Click “Apply Now” to go directly to the job posting  
- Fully free to run on **Google Colab** and **Streamlit Cloud**.  

---

## **Installation & Usage**

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/germany-data-jobs-dashboard.git
cd germany-data-jobs-dashboard

