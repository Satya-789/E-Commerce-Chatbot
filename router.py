def get_route(query: str):
    query = query.lower()

    # FAQ type queries
    faq_keywords = [
        "return", "refund", "policy", "track",
        "payment", "cancel", "delivery"
    ]

    # Product / SQL queries
    sql_keywords = [
        "buy", "price", "shoes", "under",
        "discount", "brand", "sale", "rating"
    ]

    if any(word in query for word in faq_keywords):
        return "faq"

    if any(word in query for word in sql_keywords):
        return "sql"

    # Default fallback
    return "faq"
