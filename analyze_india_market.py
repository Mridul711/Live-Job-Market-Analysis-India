import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the Data
filename = 'linkedin_india_bulk.csv'
try:
    df = pd.read_csv(filename)
    print(f"Loaded {len(df)} jobs.")
except FileNotFoundError:
    print("Error: Run the scraper first!")
    exit()

# --- FIX 1: CLEANING LOCATIONS ---
# Map variations to standard names
location_map = {
    'Bangalore Urban': 'Bengaluru',
    'Bengaluru, Karnataka, India': 'Bengaluru',
    'Greater Bengaluru Area': 'Bengaluru',
    'Bengaluru East, Karnataka, India': 'Bengaluru', # Added this from your chart
    'Mumbai, Maharashtra, India': 'Mumbai',
    'Mumbai Metropolitan Region': 'Mumbai',
    'Greater Delhi Area': 'Delhi/NCR',
    'New Delhi': 'Delhi/NCR',
    'Delhi, India': 'Delhi/NCR',
    'Gurugram': 'Gurugram', # Keeping Gurugram separate or merging into NCR is your choice
    'Gurgaon, Haryana, India': 'Gurugram',
    'Noida, Uttar Pradesh, India': 'Noida',
    'Pune, Maharashtra, India': 'Pune',
    'Hyderabad, Telangana, India': 'Hyderabad',
    'Chennai, Tamil Nadu, India': 'Chennai'
}
df['Location_Clean'] = df['Location'].replace(location_map)

# FILTER: Remove generic "India" location to see only cities
df = df[df['Location_Clean'] != 'India']

# --- FIX 2: CLEANING KEYWORDS ---
all_words = []
for title in df['Role']:
    # Split title, convert to lowercase, remove special chars
    words = title.lower().replace('(', '').replace(')', '').split()
    all_words.extend(words)

# List of boring words to ignore
ignore_words = [
    'data', 'analyst', 'engineer', 'business', 'associate', 'senior', 'sr.', 'jr.', 
    'consultant', 'manager', 'assistant', 'scientist', 'developer', 
    'for', 'and', 'of', 'in', 'the', 'to', 'with', 'at', '&', '-', '||', '/', 'online'
]

# FILTER: Keep word only if it is NOT in ignore list AND it is NOT a number
filtered_words = [w for w in all_words if w not in ignore_words and not w.isdigit()]

# --- GENERATE COUNTS ---
top_cities = df['Location_Clean'].value_counts().head(10)
top_companies = df['Company'].value_counts().head(10)
keyword_counts = pd.Series(filtered_words).value_counts().head(10)

# --- VISUALIZATION ---
fig, axes = plt.subplots(3, 1, figsize=(10, 15)) # Increased height slightly

# Chart 1: Top Locations
sns.barplot(x=top_cities.values, y=top_cities.index, hue=top_cities.index, palette='viridis', ax=axes[0], legend=False)
axes[0].set_title('Top 10 Locations for Data Analysts (Cities Only)', fontsize=14)

# Chart 2: Top Companies
sns.barplot(x=top_companies.values, y=top_companies.index, hue=top_companies.index, palette='rocket', ax=axes[1], legend=False)
axes[1].set_title('Companies Hiring the Most Right Now', fontsize=14)

# Chart 3: Top Skills/Keywords (Cleaned)
sns.barplot(x=keyword_counts.values, y=keyword_counts.index, hue=keyword_counts.index, palette='coolwarm', ax=axes[2], legend=False)
axes[2].set_title('Trending Skills & Domain Keywords', fontsize=14)
axes[2].set_xlabel('Frequency')

plt.tight_layout()
plt.savefig('india_market_analysis_fixed.png', dpi=300)
print("SUCCESS! Cleaned chart saved as 'india_market_analysis_fixed.png'")
