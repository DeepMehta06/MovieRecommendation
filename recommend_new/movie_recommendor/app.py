import streamlit as slt
import pickle
import pandas as pd
import re
from difflib import get_close_matches

# Load pickled data
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity_list.pkl', 'rb'))

slt.title("Movie Recommender System")

# Create normalized title column for flexible matching
def normalize_title(s: str) -> str:
    """Normalize title: lowercase, remove non-alphanumeric characters"""
    s = str(s).lower()
    s = re.sub(r"[^a-z0-9]+", "", s)  # Keep only alphanumerics
    return s

# Add normalized titles to dataframe
movies_df['title_norm'] = movies_df['title'].apply(normalize_title)

def recommend(title_query: str, k: int = 10):
    """
    Recommend k similar movies based on the input title.
    
    Parameters:
    - title_query: Movie title (case-insensitive, flexible spelling)
    - k: Number of recommendations to return (default: 10)
    
    Returns:
    - List of recommended movie titles
    """
    # Normalize query
    q = normalize_title(title_query)
    
    # Find exact match
    matches = movies_df[movies_df['title_norm'] == q]
    
    if matches.empty:
        # No exact match - suggest similar titles
        candidates = movies_df['title_norm'].tolist()
        close = get_close_matches(q, candidates, n=5, cutoff=0.6)
        
        if close:
            suggestions = []
            for c in close:
                suggestions.append(movies_df.loc[movies_df['title_norm'] == c, 'title'].iloc[0])
            return None, suggestions
        else:
            return None, []
    
    # Get movie index
    movie_index = matches.index[0]
    
    # Find top-k most similar movies (excluding the input movie itself)
    top = sorted(enumerate(similarity[movie_index]), key=lambda x: x[1], reverse=True)[1:k+1]
    
    recommendations = []
    for idx, score in top:
        recommendations.append(movies_df.iloc[idx]['title'])
    
    return recommendations, None

# Streamlit UI
selected_movie_name = slt.selectbox(
    'Select a movie you like:',
    movies_df['title'].values
)

if slt.button('Recommend'):
    recommendations, suggestions = recommend(selected_movie_name, k=10)
    
    if recommendations:
        slt.subheader(f"Movies similar to '{selected_movie_name}':")
        for i, movie in enumerate(recommendations, 1):
            slt.write(f"{i}. {movie}")
    elif suggestions:
        slt.warning(f"Title not found: '{selected_movie_name}'. Did you mean:")
        for movie in suggestions:
            slt.write(f"• {movie}")
    else:
        slt.error(f"No matches found for '{selected_movie_name}'. Try another title.")