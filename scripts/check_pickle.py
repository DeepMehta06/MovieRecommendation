import pickle
import pandas as pd

# Check movies.pkl
print("=" * 50)
print("Checking movies.pkl...")
movies_data = pickle.load(open('static/movies.pkl', 'rb'))
print(f"Type: {type(movies_data)}")
print(f"Shape: {movies_data.shape if hasattr(movies_data, 'shape') else 'N/A'}")

# Check similarity_list.pkl
print("\n" + "=" * 50)
print("Checking similarity_list.pkl...")
similarity = pickle.load(open('static/similarity_list.pkl', 'rb'))
print(f"Type: {type(similarity)}")

if isinstance(similarity, pd.DataFrame):
    print("It's a DataFrame!")
    print(f"Columns: {similarity.columns.tolist()}")
    print(f"Shape: {similarity.shape}")
    print("\nFirst few rows:")
    print(similarity.head())
elif isinstance(similarity, list):
    print(f"It's a list with {len(similarity)} items")
    print(f"First item: {similarity[0]}")
else:
    print(f"Shape: {similarity.shape if hasattr(similarity, 'shape') else 'N/A'}")
