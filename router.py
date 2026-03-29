def get_route(query: str):
    query = query.lower()

    faq_keywords = ["return", "refund", "policy", "track", "payment"]
    sql_keywords = ["buy", "price", "shoes", "under", "discount"]

    if any(word in query for word in faq_keywords):
        return "faq"

    if any(word in query for word in sql_keywords):
        return "sql"

    return "faq"
