import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# 1. Load the Data
filename = 'linkedin_india_bulk.csv'
try:
    df = pd.read_csv(filename)
    print(f"Loaded {len(df)} jobs from '{filename}'.")
except FileNotFoundError:
    print("Error: Run the scraper first!")
    exit()

# 2. DATA CLEANING
# Fix common location names so "Bangalore Urban" and "Bengaluru" count as the same city
location_map = {
    'Bangalore Urban': 'Bengaluru',
    'Bengaluru, Karnataka, India': 'Bengaluru',
    'Greater Bengaluru Area': 'Bengaluru',
    'Mumbai, Maharashtra, India': 'Mumbai',
    'Mumbai Metropolitan Region': 'Mumbai',
    'Greater Delhi Area': 'Delhi/NCR',
    'New Delhi': 'Delhi/NCR',
    'Delhi, India': 'Delhi/NCR',
    'Gurugram': 'Delhi/NCR',
    'Noida': 'Delhi/NCR',
    'Pune, Maharashtra, India': 'Pune',
    'Hyderabad, Telangana, India': 'Hyderabad',
    'Chennai, Tamil Nadu, India': 'Chennai'
}
df['Location_Clean'] = df['Location'].replace(location_map)

# 3. ANALYSIS

# A. Top 10 Locations
top_cities = df['Location_Clean'].value_counts().head(10)

# B. Top 10 Companies
top_companies = df['Company'].value_counts().head(10)

# C. Keyword Analysis in Job Titles
# We split every title into words to see what terms appear most (e.g., "Senior", "Intern")
all_words = []
for title in df['Role']:
    words = title.lower().split()
    all_words.extend(words)

# Remove boring words like "data", "analyst", "associate" to find the interesting qualifiers
ignore_words = ['data', 'analyst', 'engineer', 'business', 'associate', '-', 'for', 'and', 'of', 'in', 'the', 'sr', 'sr.', 'ii', 'iii']
filtered_words = [w for w in all_words if w not in ignore_words]
keyword_counts = pd.Series(filtered_words).value_counts().head(10)

# 4. VISUALIZATION (Dashboard)
fig, axes = plt.subplots(3, 1, figsize=(10, 18))

# Chart 1: Top Locations
sns.barplot(x=top_cities.values, y=top_cities.index, hue=top_cities.index, palette='viridis', ax=axes[0], legend=False)
axes[0].set_title(f'Top Locations for Data Analysts (Based on {len(df)} Jobs)', fontsize=14)
axes[0].set_xlabel('Number of Jobs')

# Chart 2: Top Companies
sns.barplot(x=top_companies.values, y=top_companies.index, hue=top_companies.index, palette='rocket', ax=axes[1], legend=False)
axes[1].set_title('Companies Hiring the Most Right Now', fontsize=14)
axes[1].set_xlabel('Number of Jobs')

# Chart 3: Most Common Title Keywords
sns.barplot(x=keyword_counts.values, y=keyword_counts.index, hue=keyword_counts.index, palette='coolwarm', ax=axes[2], legend=False)
axes[2].set_title('Common Keywords in Job Titles (Experience Level)', fontsize=14)
axes[2].set_xlabel('Frequency')
axes[2].set_ylabel('Job Title')
plt.tight_layout()
plt.savefig('india_market_analysis.png', dpi=300)
print("SUCCESS! Analysis chart saved as 'india_market_analysis.png'")
