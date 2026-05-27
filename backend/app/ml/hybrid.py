from .collaborative import get_collaborative_recommendations
from .content_based import get_content_based_recommendations

def get_hybrid_recommendations(user_id, category=None, conn=None, n=20):
    """Combine collaborative + content-based, exclude already-rated items."""

    # Get items the user already rated — never recommend these
    with conn.cursor() as cursor:
        cursor.execute("SELECT item_id FROM ratings WHERE user_id = %s", (user_id,))
        already_rated = {row['item_id'] for row in cursor.fetchall()}

    collab  = get_collaborative_recommendations(user_id, conn, n=n)
    content = get_content_based_recommendations(user_id, conn, n=n)

    # Merge, deduplicate, and exclude already-rated items
    seen   = set()
    merged = []
    for item_id in collab + content:
        if item_id not in seen and item_id not in already_rated:
            seen.add(item_id)
            merged.append(item_id)

    if not merged:
        return []

    with conn.cursor() as cursor:
        placeholders = ','.join(['%s'] * len(merged))
        sql = f"SELECT * FROM items WHERE id IN ({placeholders})"
        params = list(merged)
        if category:
            sql += " AND category = %s"
            params.append(category)
        cursor.execute(sql, params)
        items = cursor.fetchall()

    # Preserve recommendation order
    order = {item_id: i for i, item_id in enumerate(merged)}
    items.sort(key=lambda x: order.get(x['id'], 999))
    return items[:n]
