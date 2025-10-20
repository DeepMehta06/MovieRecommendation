"""
Text Processing Module
Handles text normalization and fuzzy matching
"""

import re
from difflib import get_close_matches


def normalize_title(title: str) -> str:
    """
    Normalize movie title for flexible matching
    
    Args:
        title: Movie title string
        
    Returns:
        Normalized title (lowercase, alphanumeric only)
    """
    title = str(title).lower()
    title = re.sub(r"[^a-z0-9]+", "", title)  # Keep only alphanumerics
    return title


def find_close_matches(query: str, candidates: list, n: int = 5, cutoff: float = 0.6) -> list:
    """
    Find close matches using fuzzy string matching
    
    Args:
        query: Search query
        candidates: List of candidate strings
        n: Maximum number of matches to return
        cutoff: Minimum similarity score (0-1)
        
    Returns:
        List of close matches
    """
    return get_close_matches(query, candidates, n=n, cutoff=cutoff)


def format_release_date(release_date):
    """
    Format release date and extract year
    
    Args:
        release_date: Release date string or NaN
        
    Returns:
        Tuple of (formatted_date, year)
    """
    import pandas as pd
    
    if pd.notna(release_date) and release_date != '':
        formatted_date = release_date
        year = release_date.split('-')[0] if '-' in release_date else release_date
    else:
        formatted_date = 'N/A'
        year = 'N/A'
    
    return formatted_date, year


def format_rating(rating):
    """
    Format movie rating
    
    Args:
        rating: Rating value or NaN
        
    Returns:
        Formatted rating string
    """
    import pandas as pd
    
    if pd.notna(rating):
        return f"{rating:.1f}/10"
    return 'N/A'


def truncate_text(text, max_length: int = 150) -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis
    """
    import pandas as pd
    
    if pd.notna(text):
        text_str = str(text)
        if len(text_str) > max_length:
            return text_str[:max_length] + '...'
        return text_str
    return 'No overview available'
