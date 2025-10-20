"""
OMDB API Integration
Fetch movie posters and additional information from OMDB
"""

import requests
from django.conf import settings


def get_movie_poster(movie_title, year=None):
    """
    Fetch movie poster URL from OMDB API
    
    Args:
        movie_title: Movie title to search
        year: Release year (optional, helps with accuracy)
    
    Returns:
        Poster URL or default placeholder
    """
    api_key = getattr(settings, 'OMDB_API_KEY', None)
    
    if not api_key:
        return get_default_poster()
    
    try:
        # OMDB API endpoint
        url = "http://www.omdbapi.com/"
        params = {
            'apikey': api_key,
            't': movie_title,
            'type': 'movie'
        }
        
        if year:
            params['y'] = year
        
        response = requests.get(url, params=params, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('Response') == 'True':
                poster_url = data.get('Poster', 'N/A')
                
                if poster_url and poster_url != 'N/A':
                    return poster_url
        
        return get_default_poster()
        
    except Exception as e:
        print(f"Error fetching poster for {movie_title}: {str(e)}")
        return get_default_poster()


def get_default_poster():
    """Return default placeholder poster URL"""
    return "https://via.placeholder.com/300x450/1a1a1a/ffffff?text=No+Poster+Available"


def get_movie_details(movie_title, year=None):
    """
    Fetch detailed movie information from OMDB API
    
    Args:
        movie_title: Movie title to search
        year: Release year (optional)
    
    Returns:
        Dictionary with movie details or None
    """
    api_key = getattr(settings, 'OMDB_API_KEY', None)
    
    if not api_key:
        return None
    
    try:
        url = "http://www.omdbapi.com/"
        params = {
            'apikey': api_key,
            't': movie_title,
            'type': 'movie',
            'plot': 'short'
        }
        
        if year:
            params['y'] = year
        
        response = requests.get(url, params=params, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('Response') == 'True':
                return {
                    'poster': data.get('Poster', get_default_poster()),
                    'imdb_rating': data.get('imdbRating', 'N/A'),
                    'genre': data.get('Genre', 'N/A'),
                    'runtime': data.get('Runtime', 'N/A'),
                    'actors': data.get('Actors', 'N/A'),
                    'director': data.get('Director', 'N/A'),
                    'plot': data.get('Plot', 'N/A')
                }
        
        return None
        
    except Exception as e:
        print(f"Error fetching details for {movie_title}: {str(e)}")
        return None
