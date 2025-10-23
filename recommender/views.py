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

    # --- GET Request ---
    # Display the main search page
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
                'input_movie_name': '',
                'error_message': ''  # Added comma here
            }
        )

    # --- POST Request ---
    # Handle the user's search query
    if request.method == 'POST':
        data = request.POST
        movie_name = data.get('movie_name', '').strip()
        search_type_input = data.get('search_type', 'movie').lower()

        # Check if the search term is empty
        if not movie_name:
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
                    'input_movie_name': '',
                    'error_message': 'Please enter a search term'
                }
            )

        try:
            # --- Search by Actor ---
            if search_type_input == 'actor':
                actor_movies = data_loader.find_movies_by_actor(movie_name)
                
                if actor_movies:
                    recommendations = []
                    for title in actor_movies[:25]: # Get top 25 movies for the actor
                        movie_match = movies_data[movies_data['title'] == title]
                        if not movie_match.empty:
                            movie = movie_match.iloc[0]
                            rec_dict = recommender._format_movie_data(movie)
                            recommendations.append(rec_dict)
                    
                    if recommendations:
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
                                'search_type': 'actor',
                                'search_message': f'Movies featuring {movie_name}'
                            }
                        )
                
                # Actor not found or has no movies in the list
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
                        'input_movie_name': movie_name,
                        'error_message': f'Actor "{movie_name}" not found in our database. Please try another actor name.'
                    }
                )

            # --- Search by Director ---
            elif search_type_input == 'director':
                director_movies = data_loader.find_movies_by_director(movie_name)
                
                if director_movies:
                    recommendations = []
                    for title in director_movies[:25]: # Get top 25 movies for the director
                        movie_match = movies_data[movies_data['title'] == title]
                        if not movie_match.empty:
                            movie = movie_match.iloc[0]
                            rec_dict = recommender._format_movie_data(movie)
                            recommendations.append(rec_dict)
                    
                    if recommendations:
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
                                'search_type': 'director',
                                'search_message': f'Movies directed by {movie_name}'
                            }
                        )
                
                # Director not found
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
                        'input_movie_name': movie_name,
                        'error_message': f'Director "{movie_name}" not found in our database. Please try another director name.'
                    }
                )

            # --- Search by Movie Title (Default) ---
            else:
                recommendations, suggestions, search_type = recommender.get_recommendations(movie_name, k=25)
                
                search_message = f'Movies similar to {movie_name}'
                
                # Case 1: Movie found, recommendations generated
                if recommendations:
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
                # Case 2: Movie not found, but suggestions are available
                elif suggestions:
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
                            'input_movie_name': movie_name,
                            'error_message': ''
                        }
                    )
                # Case 3: Movie not found, no suggestions
                else:
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
                            'input_movie_name': movie_name,
                            'error_message': f'Movie "{movie_name}" not found in our database. Please try another title.'
                        }
                    )

        # --- General Error Handling ---
        except Exception as e:
            # Log the error for debugging
            print(f"Error in main view: {e}")
            import traceback
            traceback.print_exc()
            
            # Show a generic error message to the user
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
                    'input_movie_name': movie_name,
                    'error_message': 'An error occurred while searching. Please try again with a different search term.'
                }
            )