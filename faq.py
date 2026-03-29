import os
import streamlit as st

from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from groq import Groq
import pandas as pd
from dotenv import load_dotenv


# ---------- Silence warnings (clean logs) ----------
warnings.filterwarnings("ignore")
logging.getLogger("chromadb").setLevel(logging.ERROR)

# ---------- Disable telemetry ----------


# 🔥 HARD DISABLE TELEMETRY (must be before chromadb import)
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["POSTHOG_DISABLED"] = "1"
import logging
import warnings

warnings.filterwarnings("ignore")
logging.getLogger("chromadb").setLevel(logging.CRITICAL)
logging.getLogger("posthog").setLevel(logging.CRITICAL)

# ---------- Load environment ----------
import chromadb
load_dotenv()

# ---------- Embedding (NO sentence-transformers) ----------
ef = DefaultEmbeddingFunction()

# ---------- Cached Chroma Client (FIXED) ----------
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

# ---------- Ingest FAQ Data ----------
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


# ---------- Retrieve Relevant FAQs ----------
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
    prompt = f"""
You are an ecommerce assistant.

Answer ONLY using the context.
If the answer is not found, say "I don't know".

CONTEXT:
{context}

QUESTION:
{query}
"""

    completion = groq_client.chat.completions.create(
        model=os.environ["GROQ_MODEL"],
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return completion.choices[0].message.content


# ---------- FAQ Chain ----------
def faq_chain(query):
    result = get_relevant_qa(query)

    context = "\n\n".join(
        [r.get("answer", "") for r in result["metadatas"][0]]
    )

    if not context.strip():
        return "I don't know"

    return generate_answer(query, context)
