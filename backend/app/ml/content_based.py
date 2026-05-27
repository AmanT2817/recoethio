import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_content_based_recommendations(user_id, conn, n=10):
    """Content-based filtering using item genre/description TF-IDF."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, title, genre, description, category FROM items")
        items = cursor.fetchall()
        cursor.execute("SELECT item_id, score FROM ratings WHERE user_id = %s", (user_id,))
        user_ratings = cursor.fetchall()

    if not items or not user_ratings:
        return []

    items_df = pd.DataFrame(items)
    items_df['content'] = (
        items_df['genre'].fillna('') + ' ' + items_df['description'].fillna('')
    )

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(items_df['content'])
    sim_matrix = cosine_similarity(tfidf_matrix)

    rated_ids = {r['item_id'] for r in user_ratings}  # exclude ALL rated items
    liked_ids = [r['item_id'] for r in user_ratings if r['score'] >= 4]

    if not liked_ids:
        return []

    id_to_idx = {row['id']: i for i, row in enumerate(items)}
    scores = {}
    for item_id in liked_ids:
        if item_id not in id_to_idx:
            continue
        idx = id_to_idx[item_id]
        for j, score in enumerate(sim_matrix[idx]):
            candidate_id = items[j]['id']
            if candidate_id not in rated_ids:
                scores[candidate_id] = scores.get(candidate_id, 0) + score

    top_items = sorted(scores, key=scores.get, reverse=True)[:n]
    return top_items
