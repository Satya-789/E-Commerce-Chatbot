import os

# Disable telemetry FIRST
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["POSTHOG_DISABLED"] = "1"

import streamlit as st
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from groq import Groq
import pandas as pd
from dotenv import load_dotenv
import logging
import warnings

warnings.filterwarnings("ignore")
logging.getLogger("chromadb").setLevel(logging.CRITICAL)

load_dotenv()

ef = DefaultEmbeddingFunction()

@st.cache_resource
def get_chroma_client():
    return chromadb.Client()

groq_client = Groq()
collection_name_faq = "faqs"

def ingest_faq_data(path):
    client = get_chroma_client()
    existing = [c.name for c in client.list_collections()]

    if collection_name_faq not in existing:
        collection = client.create_collection(name=collection_name_faq)

        df = pd.read_csv(path)

        collection.add(
            documents=df["question"].tolist(),
            metadatas=[{"answer": a} for a in df["answer"]],
            ids=[str(i) for i in range(len(df))]
        )

def get_relevant_qa(query):
    client = get_chroma_client()
    collection = client.get_collection(name=collection_name_faq)

    return collection.query(query_texts=[query], n_results=3)

def generate_answer(query, context):
    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    prompt = f"""
Answer ONLY using the context. If not found say "I don't know".

CONTEXT:
{context}

QUESTION:
{query}
"""

    completion = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content

def faq_chain(query):
    result = get_relevant_qa(query)

    context = "\n\n".join(
        [r.get("answer", "") for r in result["metadatas"][0]]
    )

    if not context:
        return "I don't know"

    return generate_answer(query, context)
