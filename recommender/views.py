"""
Views for the movie recommendation system
Clean and organized using utility modules
"""

from django.shortcuts import render
from .utils import get_data_loader, RecommendationEngine

# Initialize data loader (singleton pattern)
data_loader = get_data_loader()

# Get loaded data
movies_data = data_loader.get_movies_data()
similarity_matrix = data_loader.get_similarity_matrix()
titles_list = data_loader.get_titles_list()

# Initialize recommendation engine
recommender = RecommendationEngine(movies_data, similarity_matrix, data_loader)

def main(request):
    """
    Main view for movie recommendation
    
    Handles both GET (display form) and POST (get recommendations) requests
    """
    global titles_list

    if request.method == 'GET':
        return render(
                request,
                'recommender/index.html',
                {
                    'all_movie_names': titles_list,
                    'input_provided': '',
                    'movie_found': '',
                    'recomendation_found': '',
                    'recommended_movies': [],
                    'suggestions': [],
                    'input_movie_name': ''
                }
            )

    if request.method == 'POST':
        data = request.POST
        movie_name = data.get('movie_name')

        # Get recommendations using the recommendation engine
        recommendations, suggestions, search_type = recommender.get_recommendations(movie_name, k=25)
        
        # Determine search type message
        search_message = ''
        if search_type == 'actor':
            search_message = f'Movies featuring {movie_name}'
        elif search_type == 'director':
            search_message = f'Movies directed by {movie_name}'
        elif search_type == 'movie':
            search_message = f'Movies similar to {movie_name}'
        
        if recommendations:
            # Movie found - show recommendations
            return render(
                request,
                'recommender/result.html',
                {
                    'all_movie_names': titles_list,
                    'input_provided': 'yes',
                    'movie_found': 'yes',
                    'recomendation_found': 'yes',
                    'recommended_movies': recommendations,
                    'suggestions': [],
                    'input_movie_name': movie_name,
                    'search_type': search_type,
                    'search_message': search_message
                }
            )
        elif suggestions:
            # Movie not found but similar suggestions available
            return render(
                request,
                'recommender/index.html',
                {
                    'all_movie_names': titles_list,
                    'input_provided': 'yes',
                    'movie_found': 'no',
                    'recomendation_found': '',
                    'recommended_movies': [],
                    'suggestions': suggestions,
                    'input_movie_name': movie_name
                }
            )
        else:
            # No movie found and no suggestions
            return render(
                request,
                'recommender/index.html',
                {
                    'all_movie_names': titles_list,
                    'input_provided': 'yes',
                    'movie_found': '',
                    'recomendation_found': '',
                    'recommended_movies': [],
                    'suggestions': [],
                    'input_movie_name': movie_name
                }
            )

