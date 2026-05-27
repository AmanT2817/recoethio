import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def get_collaborative_recommendations(user_id, conn, n=10):
    """User-based collaborative filtering."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT user_id, item_id, score FROM ratings")
        rows = cursor.fetchall()

    if not rows:
        return []

    df = pd.DataFrame(rows)
    matrix = df.pivot_table(index='user_id', columns='item_id', values='score').fillna(0)

    if user_id not in matrix.index:
        return []

    similarity = cosine_similarity(matrix)
    sim_df = pd.DataFrame(similarity, index=matrix.index, columns=matrix.index)

    similar_users = sim_df[user_id].drop(user_id).nlargest(10).index.tolist()
    user_rated = set(df[df['user_id'] == user_id]['item_id'].tolist())

    candidates = df[
        (df['user_id'].isin(similar_users)) & (~df['item_id'].isin(user_rated))
    ]
    top_items = candidates.groupby('item_id')['score'].mean().nlargest(n).index.tolist()
    return top_items
