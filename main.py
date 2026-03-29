import streamlit as st
from faq import ingest_faq_data, faq_chain
from sql import sql_chain
from pathlib import Path
from router import get_route

# ---------- Page Config ----------
st.set_page_config(
    page_title="E-commerce Chatbot",
    page_icon="🛒",
    layout="centered"
)

# ---------- Load FAQ Data ----------
faqs_path = Path(__file__).parent / "resources/faq_data.csv"

@st.cache_resource
def load_data():
    try:
        ingest_faq_data(faqs_path)
    except Exception as e:
        st.error(f"Error loading FAQ data: {e}")

load_data()

# ---------- Routing ----------
def ask(query):
    try:
        route = get_route(query)

        # DEBUG (optional)
        # st.sidebar.write(f"Route: {route}")

        if route == 'faq':
            return faq_chain(query)

        elif route == 'sql':
            return sql_chain(query)

        else:
            return "🤖 I can help with products, orders, and store policies."

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ---------- UI ----------
st.title("🛒 E-commerce AI Assistant")
st.caption("Ask about products, payments, orders, and policies")

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Options")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Try asking:**")
    st.markdown("- Nike shoes under 3000")
    st.markdown("- What is your return policy?")
    st.markdown("- Track my order")

# ---------- Chat Input ----------
query = st.chat_input("Type your question...")

# ---------- Chat Memory ----------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ---------- Display Chat ----------
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# ---------- Handle Query ----------
if query:
    # Show user message
    with st.chat_message("user"):
        st.markdown(query)

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # Generate response
    with st.spinner("Thinking..."):
        response = ask(query)

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
