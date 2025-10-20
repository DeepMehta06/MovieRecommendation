"""
Recommendation Engine Module
Core recommendation logic
"""

import pandas as pd
from .text_processing import (
    normalize_title, 
    find_close_matches, 
    format_release_date,
    format_rating,
    truncate_text
)
from .omdb_api import get_movie_poster


class RecommendationEngine:
    """Movie recommendation engine"""
    
    def __init__(self, movies_data, similarity_matrix, data_loader=None):
        """
        Initialize recommendation engine
        
        Args:
            movies_data: DataFrame with movie information
            similarity_matrix: Pre-computed similarity matrix
            data_loader: DataLoader instance for actor/director search
        """
        self.movies_data = movies_data.copy()
        self.similarity_matrix = similarity_matrix
        self.data_loader = data_loader
        
        # Add normalized titles for matching
        self.movies_data['title_norm'] = self.movies_data['title'].apply(normalize_title)
    
    def get_recommendations(self, movie_title: str, k: int = 25):
        """
        Get movie recommendations
        
        Args:
            movie_title: Movie title, actor name, or director name to search
            k: Number of recommendations to return
            
        Returns:
            Tuple of (recommendations_list, suggestions_list, search_type)
            - recommendations_list: List of dicts with movie details (or None)
            - suggestions_list: List of suggested titles if no exact match (or None)
            - search_type: 'movie', 'actor', 'director', or 'suggestion'
        """
        try:
            # Normalize query
            query_norm = normalize_title(movie_title)
            
            # 1. Try exact movie match
            matches = self.movies_data[self.movies_data['title_norm'] == query_norm]
            
            if not matches.empty:
                # Found exact movie match
                result = self._get_similar_movies(matches.index[0], k)
                return result + ('movie',)
            
            # 2. Try actor search
            if self.data_loader:
                actor_movies = self.data_loader.find_movies_by_actor(movie_title)
                if actor_movies:
                    return self._get_movies_by_list(actor_movies, k, movie_title, 'actor')
                
                # 3. Try director search
                director_movies = self.data_loader.find_movies_by_director(movie_title)
                if director_movies:
                    return self._get_movies_by_list(director_movies, k, movie_title, 'director')
            
            # 4. No exact match - suggest similar titles
            result = self._get_suggestions(query_norm)
            return result + ('suggestion',)
            
        except Exception as e:
            print(f"Error in get_recommendations: {e}")
            return None, None, 'error'
            return None, []
    
    def _get_suggestions(self, normalized_query: str):
        """
        Get title suggestions for queries with no exact match
        
        Args:
            normalized_query: Normalized query string
            
        Returns:
            Tuple of (None, suggestions_list)
        """
        candidates = self.movies_data['title_norm'].tolist()
        close_matches = find_close_matches(normalized_query, candidates, n=5, cutoff=0.6)
        
        if close_matches:
            suggestions = []
            for match in close_matches:
                title = self.movies_data.loc[
                    self.movies_data['title_norm'] == match, 
                    'title'
                ].iloc[0]
                suggestions.append(title)
            return None, suggestions
        
        return None, []
    
    def _get_similar_movies(self, movie_index: int, k: int):
        """
        Get similar movies based on similarity matrix
        
        Args:
            movie_index: Index of the movie in the dataset
            k: Number of recommendations
            
        Returns:
            Tuple of (recommendations_list, None)
        """
        # Get similarity scores
        similarity_scores = list(enumerate(self.similarity_matrix[movie_index]))
        
        # Sort by similarity (descending) and exclude the movie itself
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:k+1]
        
        # Build recommendations list
        recommendations = []
        for idx, score in sorted_scores:
            movie = self.movies_data.iloc[idx]
            rec_dict = self._format_movie_data(movie)
            recommendations.append(rec_dict)
        
        return recommendations, None
    
    def _format_movie_data(self, movie: pd.Series) -> dict:
        """
        Format movie data into dictionary
        
        Args:
            movie: Pandas Series with movie data
            
        Returns:
            Dictionary with formatted movie information
        """
        # Format release date
        release_date, release_year = format_release_date(movie['release_date'])
        
        # Format rating
        rating = format_rating(movie['vote_average'])
        
        # Get movie poster
        poster_url = get_movie_poster(movie['title'], release_year)
        
        # Get cast as comma-separated string
        cast_str = 'N/A'
        if 'cast_list' in movie and isinstance(movie['cast_list'], list):
            cast_str = ', '.join(movie['cast_list'][:3])  # Top 3 actors
        
        return {
            'title': movie['title'],
            'director': movie.get('director', 'N/A'),
            'release_date': release_date,
            'release_year': release_year,
            'rating': rating,
            'overview': truncate_text(movie.get('overview', 'No overview available.'), 150),
            'poster_url': poster_url,
            'cast': cast_str,
            'google_search': f"https://www.google.com/search?q={movie['title'].replace(' ', '+')}+movie"
        }
    
    def _get_movies_by_list(self, movie_titles: list, k: int, search_query: str, search_type: str):
        """
        Get movies from a list of titles (for actor/director search)
        
        Args:
            movie_titles: List of movie titles
            k: Maximum number to return
            search_query: Original search query
            search_type: 'actor' or 'director'
            
        Returns:
            Tuple of (recommendations_list, None)
        """
        recommendations = []
        
        for title in movie_titles[:k]:
            # Find movie in dataframe
            movie_match = self.movies_data[self.movies_data['title'] == title]
            
            if not movie_match.empty:
                movie = movie_match.iloc[0]
                rec_dict = self._format_movie_data(movie)
                recommendations.append(rec_dict)
        
        return recommendations, None
