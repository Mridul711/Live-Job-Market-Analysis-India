import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# --- CONFIGURATION ---
# We will scrape 10 pages (approx 200-250 jobs)
# Warning: If you go too high (e.g., 1000), LinkedIn will block you for a few hours.
max_pages = 30 
jobs_per_page = 25  # LinkedIn displays 25 jobs per load
# ---------------------

print(f"Step 1: Starting Bulk Scrape for 'Data Analyst' in India...")
print(f"Target: ~{max_pages * jobs_per_page} Jobs")

data = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

for page in range(0, max_pages):
    # calculate the 'start' position (0, 25, 50, 75...)
    start_position = page * jobs_per_page
    
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Analyst&location=India&start={start_position}"
    
    print(f"--> Scraping Page {page + 1} (Jobs {start_position}-{start_position+25})...")
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"   Blocked or Error (Status: {response.status_code}). Stopping.")
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.find_all('li')
        
        if not jobs:
            print("   No more jobs found.")
            break
            
        for job in jobs:
            try:
                title = job.find('h3', class_='base-search-card__title').get_text(strip=True)
                company = job.find('h4', class_='base-search-card__subtitle').get_text(strip=True)
                location = job.find('span', class_='job-search-card__location').get_text(strip=True)
                link = job.find('a', class_='base-card__full-link')['href']
                
                # Check for "posted date"
                date_tag = job.find('time', class_='job-search-card__listdate')
                date_posted = date_tag.get_text(strip=True) if date_tag else "Recent"

                data.append({
                    "Role": title,
                    "Company": company,
                    "Location": location,
                    "Date_Posted": date_posted,
                    "Apply_Link": link
                })
            except AttributeError:
                continue
        
        # IMPORTANT: Sleep to pretend we are human
        sleep_time = random.uniform(2, 5)
        time.sleep(sleep_time)
        
    except Exception as e:
        print(f"Error: {e}")
        break

# --- SAVE DATA ---
print("-" * 30)
if len(data) > 0:
    df = pd.DataFrame(data)
    # Remove duplicates (jobs often repeat on LinkedIn)
    df.drop_duplicates(subset=['Apply_Link'], inplace=True)
    
    filename = 'linkedin_india_bulk.csv'
    df.to_csv(filename, index=False)
    print(f"SUCCESS! Scraped {len(df)} unique jobs to '{filename}'.")
else:
    print("Failed to scrape any jobs.")
