from semantic_router import Route, RouteLayer
from semantic_router.encoders import HuggingFaceEncoder

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

faq = Route(
    name='faq',
    utterances=[
        "return policy", "refund", "cancel order",
        "track order", "payment methods"
    ]
)

sql = Route(
    name='sql',
    utterances=[
        "buy shoes", "cheap shoes", "nike shoes",
        "under 3000", "running shoes"
    ]
)

router = RouteLayer(routes=[faq, sql], encoder=encoder, score_threshold=0.3)

def get_route(query):
    return router(query).name
