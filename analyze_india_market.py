import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# 1. LOAD DATA
filename = 'linkedin_india_bulk.csv'
try:
    df = pd.read_csv(filename)
    print(f"Loaded {len(df)} jobs.")
except FileNotFoundError:
    print("Error: Run the scraper first!")
    exit()

df['Location_Clean'] = df['Location'].astype(str).str.strip()
city_map = {
    'Bengaluru': ['Bangalore', 'Bengaluru'],
    'Delhi/NCR': ['Delhi', 'Gurgaon', 'Gurugram', 'Noida', 'New Delhi'],
    'Mumbai': ['Mumbai', 'Thane', 'Navi Mumbai'],
    'Pune': ['Pune'],
    'Hyderabad': ['Hyderabad', 'Secunderabad'],
    'Chennai': ['Chennai']
}
def clean_location(loc):
    for main_city, aliases in city_map.items():
        for alias in aliases:
            if alias.lower() in loc.lower():
                return main_city
    return loc 

df['Location_Clean'] = df['Location_Clean'].apply(clean_location)
df = df[~df['Location_Clean'].isin(['India', 'nan', 'null', 'Remote'])]

found_skills = []

# We define exactly what we want to find. 
# Keys = Search term (lowercase), Values = Nice Display Name
target_skills = {
    'sql': 'SQL',
    'python': 'Python',
    'excel': 'Excel',
    'power bi': 'Power BI',
    'powerbi': 'Power BI', # Catching typo
    'tableau': 'Tableau',
    'r': 'R Language',
    'sas': 'SAS',
    'aws': 'AWS',
    'azure': 'Azure',
    'google cloud': 'GCP',
    'snowflake': 'Snowflake',
    'etl': 'ETL',
    'spark': 'Spark',
    'hadoop': 'Hadoop',
    'machine learning': 'Machine Learning',
    'ai': 'AI',
    'nlp': 'NLP',
    'statistics': 'Statistics',
    'databricks': 'Databricks',
    'pandas': 'Pandas',
    'numpy': 'NumPy',
    'vba': 'VBA',
    'looker': 'Looker',
    'alteryx': 'Alteryx',
    'nosql': 'NoSQL',
    'mongodb': 'MongoDB'
}

for title in df['Role']:
    if pd.isna(title): continue
    
    # Convert title to lowercase for searching
    title_lower = str(title).lower()
    
    # Check for each skill in our list
    for key, display_name in target_skills.items():
        # We put spaces around the key to avoid partial matches 
        # (e.g. prevent finding 'R' inside 'Architect')
        # But for 'power bi' we just check if it exists.
        
        if key in ['r', 'c', 'ai']: # Short words need strict checking
             pattern = r'\b' + re.escape(key) + r'\b'
             if re.search(pattern, title_lower):
                 found_skills.append(display_name)
        else:
            if key in title_lower:
                found_skills.append(display_name)
top_cities = df['Location_Clean'].value_counts().head(8)
top_companies = df['Company'].value_counts().head(10)
top_skills = pd.Series(found_skills).value_counts().head(10)

plt.style.use('seaborn-v0_8-whitegrid')
fig, axes = plt.subplots(3, 1, figsize=(10, 16))

# Chart 1: Top Hiring Hubs
sns.barplot(x=top_cities.values, y=top_cities.index, hue=top_cities.index, palette='viridis', ax=axes[0], legend=False)
axes[0].set_title('Top Cities for Data Analysts', fontsize=14, weight='bold')

# Chart 2: Top Hiring Companies
sns.barplot(x=top_companies.values, y=top_companies.index, hue=top_companies.index, palette='rocket', ax=axes[1], legend=False)
axes[1].set_title('Top Companies Hiring Now', fontsize=14, weight='bold')

# Chart 3: Top Technical Skills (Cleaned)
if len(top_skills) > 0:
    sns.barplot(x=top_skills.values, y=top_skills.index, hue=top_skills.index, palette='coolwarm', ax=axes[2], legend=False)
    axes[2].set_title('Most Demanded Technical Skills (From Job Titles)', fontsize=14, weight='bold')
    axes[2].set_xlabel('Frequency')
else:
    axes[2].text(0.5, 0.5, "No specific skills found in Job Titles.\n(Recruiters likely put skills in the Description, not Title)", 
                 ha='center', va='center', fontsize=12)
    axes[2].set_title('Most Demanded Technical Skills', fontsize=14, weight='bold')

plt.tight_layout()
plt.savefig('final_job_market_analysis_v4.png', dpi=300)
print("SUCCESS! Cleaned analysis saved as 'final_job_market_analysis_v4.png'")
