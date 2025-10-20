import pandas as pd
import json

# Load data
movies = pd.read_csv('static/tmdb_5000_movies.csv')
credits = pd.read_csv('static/tmdb_5000_credits.csv')

print("Movies columns:", movies.columns.tolist())
print("\nSample movie data:")
print(movies[['title', 'release_date', 'vote_average', 'overview']].head(3))

print("\n" + "="*50)
print("Credits structure:")
# Parse crew JSON to find director
crew_sample = credits['crew'].iloc[0]
crew_list = json.loads(crew_sample)
print(f"Number of crew members: {len(crew_list)}")
print("\nFirst few crew members:")
for person in crew_list[:3]:
    print(f"  Name: {person['name']}, Job: {person['job']}")

# Find director
directors = [p['name'] for p in crew_list if p['job'] == 'Director']
print(f"\nDirector(s): {directors}")
