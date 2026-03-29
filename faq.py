import os

# ---------- 🔥 MUST BE FIRST (disable telemetry) ----------
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["POSTHOG_DISABLED"] = "1"

# ---------- Imports ----------
import streamlit as st
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from groq import Groq
import pandas as pd
from dotenv import load_dotenv
import logging
import warnings

# ---------- Silence logs ----------
warnings.filterwarnings("ignore")
logging.getLogger("chromadb").setLevel(logging.CRITICAL)
logging.getLogger("posthog").setLevel(logging.CRITICAL)

# ---------- Load env ----------
load_dotenv()

# ---------- Embedding ----------
ef = DefaultEmbeddingFunction()

# ---------- Cached Chroma Client ----------
@st.cache_resource
def get_chroma_client():
    return chromadb.Client(
        chromadb.config.Settings(
            persist_directory="./chroma_db",
            anonymized_telemetry=False
        )
    )

# ---------- Groq Client ----------
groq_client = Groq()
collection_name_faq = "faqs"

# ---------- Ingest ----------
def ingest_faq_data(path):
    chroma_client = get_chroma_client()

    existing = [c.name for c in chroma_client.list_collections()]

    if collection_name_faq not in existing:
        collection = chroma_client.create_collection(
            name=collection_name_faq,
            embedding_function=ef
        )

        df = pd.read_csv(path)

        collection.add(
            documents=df["question"].tolist(),
            metadatas=[{"answer": a} for a in df["answer"]],
            ids=[str(i) for i in range(len(df))]
        )

        chroma_client.persist()

# ---------- Retrieve ----------
def get_relevant_qa(query):
    chroma_client = get_chroma_client()

    collection = chroma_client.get_collection(
        name=collection_name_faq,
        embedding_function=ef
    )

    return collection.query(
        query_texts=[query],
        n_results=3
    )

# ---------- Generate Answer ----------
def generate_answer(query, context):
    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    prompt = f"""
You are an ecommerce assistant.

Answer ONLY using the context.
If not found, say "I don't know".

CONTEXT:
{context}

QUESTION:
{query}
"""

    completion = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return completion.choices[0].message.content

# ---------- Chain ----------
def faq_chain(query):
    result = get_relevant_qa(query)

    context = "\n\n".join(
        [r.get("answer", "") for r in result["metadatas"][0]]
    )

    if not context.strip():
        return "I don't know"

    return generate_answer(query, context)
