"""
Utility modules for the recommender app
"""

from .data_loader import get_data_loader, DataLoader
from .text_processing import normalize_title, find_close_matches
from .recommender_engine import RecommendationEngine

__all__ = [
    'get_data_loader',
    'DataLoader',
    'normalize_title',
    'find_close_matches',
    'RecommendationEngine',
]
