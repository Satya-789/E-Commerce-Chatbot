import streamlit as st
from faq import ingest_faq_data, faq_chain
from sql import sql_chain
from pathlib import Path
from router import get_route

st.set_page_config(page_title="E-commerce Bot", page_icon="🛒")

# ---------- Load FAQ ----------
faqs_path = Path(__file__).parent / "resources/faq_data.csv"

@st.cache_resource
def load_data():
    ingest_faq_data(faqs_path)

load_data()

# ---------- Routing ----------
def ask(query):
    route = get_route(query)

    if route == "faq":
        return faq_chain(query)
    elif route == "sql":
        return sql_chain(query)
    else:
        return "I can help with products, orders, and policies."

# ---------- UI ----------
st.title("🛒 E-commerce AI Assistant")

query = st.chat_input("Ask something...")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Thinking..."):
        response = ask(query)

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)
