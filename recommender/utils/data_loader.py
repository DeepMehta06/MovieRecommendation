"""
Data Loader Module
Handles loading of datasets and pre-trained models
"""

import pandas as pd
import pickle
import json
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
DATASETS_DIR = DATA_DIR / 'datasets'
MODELS_DIR = DATA_DIR / 'models'


class DataLoader:
    """Centralized data loading class"""
    
    def __init__(self):
        self.movies_data = None
        self.credits_data = None
        self.similarity_matrix = None
        self.titles_list = None
        self.actor_to_movies = {}  # Actor name -> list of movies
        self.director_to_movies = {}  # Director name -> list of movies
        
    def load_all(self):
        """Load all required data"""
        self.load_movies()
        self.load_credits()
        self.merge_data()
        self.load_similarity_matrix()
        self.create_titles_list()
        self.create_actor_director_indexes()
        
    def load_movies(self):
        """Load TMDB movies dataset"""
        movies_path = DATASETS_DIR / 'tmdb_5000_movies.csv'
        self.movies_data = pd.read_csv(movies_path)
        return self.movies_data
    
    def load_credits(self):
        """Load TMDB credits dataset"""
        credits_path = DATASETS_DIR / 'tmdb_5000_credits.csv'
        self.credits_data = pd.read_csv(credits_path)
        return self.credits_data
    
    def load_similarity_matrix(self):
        """Load pre-computed similarity matrix"""
        similarity_path = MODELS_DIR / 'similarity_list.pkl'
        with open(similarity_path, 'rb') as f:
            self.similarity_matrix = pickle.load(f)
        return self.similarity_matrix
    
    @staticmethod
    def extract_director(crew_json):
        """Extract director name from crew JSON string"""
        try:
            crew_list = json.loads(crew_json)
            directors = [person['name'] for person in crew_list if person['job'] == 'Director']
            return directors[0] if directors else 'N/A'
        except:
            return 'N/A'
    
    @staticmethod
    def extract_cast(cast_json, limit=5):
        """Extract top cast members from cast JSON string"""
        try:
            cast_list = json.loads(cast_json)
            # Get top N actors
            actors = [person['name'] for person in cast_list[:limit]]
            return actors if actors else []
        except:
            return []
    
    def merge_data(self):
        """Merge movies with credits to get director information"""
        if self.credits_data is not None:
            # Add director column
            self.credits_data['director'] = self.credits_data['crew'].apply(self.extract_director)
            
            # Add cast column (list of actors)
            self.credits_data['cast_list'] = self.credits_data['cast'].apply(self.extract_cast)
            
            # Merge movies with credits
            self.movies_data = self.movies_data.merge(
                self.credits_data[['title', 'director', 'cast_list']], 
                on='title', 
                how='left'
            )
            
            # Fill missing directors
            self.movies_data['director'] = self.movies_data['director'].fillna('N/A')
            # Fill missing cast
            self.movies_data['cast_list'] = self.movies_data['cast_list'].apply(
                lambda x: x if isinstance(x, list) else []
            )
    
    def create_titles_list(self):
        """Create list of movie titles"""
        if self.movies_data is not None:
            self.titles_list = self.movies_data['title'].to_list()
        return self.titles_list
    
    def create_actor_director_indexes(self):
        """Create reverse lookup indexes for actors and directors"""
        if self.movies_data is None:
            return
        
        # Build actor index
        for idx, row in self.movies_data.iterrows():
            title = row['title']
            
            # Index by director
            director = row.get('director', 'N/A')
            if director and director != 'N/A':
                if director not in self.director_to_movies:
                    self.director_to_movies[director] = []
                self.director_to_movies[director].append(title)
            
            # Index by actors
            cast_list = row.get('cast_list', [])
            if isinstance(cast_list, list):
                for actor in cast_list:
                    if actor:
                        if actor not in self.actor_to_movies:
                            self.actor_to_movies[actor] = []
                        self.actor_to_movies[actor].append(title)
    
    def find_movies_by_actor(self, actor_name):
        """Find all movies featuring a specific actor"""
        # Case-insensitive partial match
        actor_lower = actor_name.lower()
        matching_movies = []
        
        for actor, movies in self.actor_to_movies.items():
            if actor_lower in actor.lower():
                matching_movies.extend(movies)
        
        # Remove duplicates while preserving order
        seen = set()
        result = []
        for movie in matching_movies:
            if movie not in seen:
                seen.add(movie)
                result.append(movie)
        
        return result
    
    def find_movies_by_director(self, director_name):
        """Find all movies by a specific director"""
        # Case-insensitive partial match
        director_lower = director_name.lower()
        matching_movies = []
        
        for director, movies in self.director_to_movies.items():
            if director_lower in director.lower():
                matching_movies.extend(movies)
        
        # Remove duplicates while preserving order
        seen = set()
        result = []
        for movie in matching_movies:
            if movie not in seen:
                seen.add(movie)
                result.append(movie)
        
        return result
    
    def get_movies_data(self):
        """Get movies dataframe"""
        return self.movies_data
    
    def get_similarity_matrix(self):
        """Get similarity matrix"""
        return self.similarity_matrix
    
    def get_titles_list(self):
        """Get list of all movie titles"""
        return self.titles_list


# Global instance
_data_loader = None

def get_data_loader():
    """Get or create singleton data loader instance"""
    global _data_loader
    if _data_loader is None:
        _data_loader = DataLoader()
        _data_loader.load_all()
    return _data_loader
