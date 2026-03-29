import re

def normalize(text: str) -> str:
    """Lowercase + remove extra spaces"""
    return re.sub(r"\s+", " ", text.lower().strip())


def contains_any(text: str, keywords: list) -> bool:
    return any(k in text for k in keywords)


def get_route(query: str) -> str:
    """
    Returns one of:
    - 'faq'
    - 'sql'
    - 'fallback'
    """

    q = normalize(query)

    # ---------- FAQ INTENT ----------
    faq_keywords = [
        "return", "refund", "cancel", "policy", "replacement",
        "defective", "damaged", "exchange",
        "payment", "pay", "upi", "credit card", "debit card", "cod",
        "cash on delivery",
        "track", "tracking", "where is my order", "order status",
        "delivery", "shipping", "late delivery",
        "account", "login", "signup"
    ]

    # ---------- PRODUCT / SQL INTENT ----------
    product_keywords = [
        "buy", "show", "find", "search", "looking for",
        "price", "cost", "under", "between",
        "cheap", "best", "top", "discount", "offer",
        "shoes", "sneakers", "heels", "sandals",
        "nike", "puma", "adidas", "reebok",
        "size", "color", "black", "white",
        "men", "women", "kids",
        "running", "formal", "casual"
    ]

    # ---------- PRIORITY RULES (IMPORTANT) ----------

    # If BOTH present → decide based on stronger signal
    faq_match = contains_any(q, faq_keywords)
    product_match = contains_any(q, product_keywords)

    # Example: "return my nike shoes" → FAQ (override)
    if faq_match and product_match:
        if any(word in q for word in ["return", "refund", "cancel"]):
            return "faq"
        return "sql"

    # ---------- DIRECT MATCH ----------
    if faq_match:
        return "faq"

    if product_match:
        return "sql"

    # ---------- PATTERN-BASED DETECTION ----------

    # Price patterns
    if re.search(r"\bunder\s+\d+", q) or re.search(r"\bbetween\s+\d+", q):
        return "sql"

    # Brand pattern
    if re.search(r"\b(nike|puma|adidas|reebok)\b", q):
        return "sql"

    # ---------- DEFAULT ----------
    return "fallback"


# ---------- TESTING ----------
if __name__ == "__main__":
    tests = [
        "What is your return policy?",
        "I want nike shoes under 3000",
        "Where is my order?",
        "Show me cheap running shoes",
        "Refund my product",
        "hello",
        "best puma shoes for men",
        "cancel my order",
        "track my delivery",
        "formal shoes size 9"
    ]

    for t in tests:
        print(f"{t} → {get_route(t)}")
