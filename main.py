import streamlit as st
from faq import ingest_faq_data, faq_chain
from sql import sql_chain
from pathlib import Path
from router import get_route   # ✅ FIXED

# ---------- Load FAQ ----------
faqs_path = Path(__file__).parent / "resources/faq_data.csv"

@st.cache_resource
def load_data():
    ingest_faq_data(faqs_path)

load_data()

# ---------- Routing ----------
def ask(query):
    route = get_route(query)   # ✅ FIXED

    if route == "faq":
        return faq_chain(query)

    elif route == "sql":
        return sql_chain(query)

    else:
        return "I can help with products, orders, and policies."

# ---------- UI ----------
st.set_page_config(page_title="E-commerce Bot", page_icon="🛒")

st.title("🛒 E-commerce AI Assistant")

query = st.chat_input("Write your query")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ---------- Chat history ----------
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'], unsafe_allow_html=True)  # ✅ FIX

# ---------- New message ----------
if query:
    with st.chat_message("user"):
        st.markdown(query)

    st.session_state.messages.append({"role": "user", "content": query})

    with st.spinner("Thinking..."):
        response = ask(query)

    with st.chat_message("assistant"):
        st.markdown(response, unsafe_allow_html=True)  # ✅ FIX

    st.session_state.messages.append({"role": "assistant", "content": response})
