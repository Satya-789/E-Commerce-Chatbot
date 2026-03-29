import streamlit as st
from faq import ingest_faq_data, faq_chain
from sql import sql_chain
from pathlib import Path
from router import get_route

# ---------- Load FAQ Data ----------
faqs_path = Path(__file__).parent / "resources/faq_data.csv"

@st.cache_resource
def load_data():
    ingest_faq_data(faqs_path)

load_data()

# ---------- Routing ----------
def ask(query):
    try:
        route = get_route(query)

        if route == 'faq':
            return faq_chain(query)

        elif route == 'sql':
            return sql_chain(query)

        else:
            return "I can help with products, orders, and policies."

    except Exception as e:
        return f"Error: {str(e)}"

# ---------- UI ----------
st.title("🛒 E-commerce AI Assistant")
st.caption("Ask about products, payments, and orders")

query = st.chat_input("Type your question...")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if query:
    with st.chat_message("user"):
        st.markdown(query)

    st.session_state.messages.append({"role": "user", "content": query})

    with st.spinner("Thinking..."):
        response = ask(query)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
