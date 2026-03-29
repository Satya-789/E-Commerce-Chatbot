def get_route(query: str) -> str:
    query = query.lower()

    faq_keywords = [
        "return", "refund", "policy", "payment", "track", "order"
    ]

    sql_keywords = [
        "buy", "price", "shoes", "discount", "under", "rs"
    ]

    if any(word in query for word in faq_keywords):
        return "faq"

    if any(word in query for word in sql_keywords):
        return "sql"

    return "faq"
