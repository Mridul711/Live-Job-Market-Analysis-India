## 📈 Project: India Job Market Tracker (Live Scraping)

**Goal:** To analyze the real-time demand for Data Analysts in India and identify the top hiring hubs and companies.

**Technical Approach:**
* **Data Collection:** Built a Python scraper using `requests` and `BeautifulSoup` to bypass LinkedIn's public API limitations, collecting **300+ live job postings** across India.
* **Automation:** Implemented pagination logic with random sleep intervals (2-5s) to mimic human behavior and prevent IP blocking.
* **Analysis:** Used `Pandas` to clean location data (normalizing 'Bengaluru' vs 'Bangalore Urban') and `Seaborn` to visualize hiring trends.

**Key Insights (Nov 2025):**
* **Top Hubs:** Bengaluru and Gurugram account for ~40% of all visible listings.
* **Top Recruiters:** Identified **EXL** and **TELUS Digital** as the top volume hirers this month.
* **Strategy:** Focused job applications on these specific hubs and companies to maximize response rates.

**Visuals:**
![Market Analysis Chart](final_job_market_analysis_v4.png)
