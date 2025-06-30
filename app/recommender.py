import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

def recommend_for_user(user_id, n=5):
    try:
        df = pd.read_csv("ratings.csv")
    except FileNotFoundError:
        print("ratings.csv not found.")
        return []

    if df.empty or user_id not in df['userId'].values:
        print(f"No data or unknown user: {user_id}")
        return []

    # Create user-item matrix (pivot)
    user_item_matrix = df.pivot_table(index='userId', columns='menuItemId', values='rating', fill_value=0)

    # Convert to sparse matrix for efficiency
    sparse_matrix = csr_matrix(user_item_matrix.values)

    # Fit KNN model on users
    model = NearestNeighbors(metric='cosine', algorithm='brute')
    model.fit(sparse_matrix)

    # Find the nearest neighbors for the target user
    user_index = user_item_matrix.index.get_loc(user_id)
    distances, indices = model.kneighbors(sparse_matrix[user_index], n_neighbors=3)

    # Get neighbor indices, excluding the user itself (0th index)
    neighbor_indices = indices.flatten()[1:]

    # Aggregate top-rated items from neighbors
    neighbor_ids = user_item_matrix.index[neighbor_indices]
    neighbor_ratings = user_item_matrix.loc[neighbor_ids]

    # Compute average ratings for each item from neighbors
    mean_ratings = neighbor_ratings.mean(axis=0)

    # Exclude items already rated by the user
    user_rated_items = user_item_matrix.loc[user_id]
    unrated_items = mean_ratings[user_rated_items == 0]

    # Recommend top N items based on average neighbor rating
    recommendations = unrated_items.sort_values(ascending=False).head(n).index.tolist()

    print(f"✅ Recommended items for user {user_id}: {recommendations}")

    return recommendations
