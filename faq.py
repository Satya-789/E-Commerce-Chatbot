import os
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)

chroma_client = chromadb.Client(
    chromadb.config.Settings(
        persist_directory="./chroma_db"
    )
)

groq_client = Groq()
collection_name_faq = 'faqs'


def ingest_faq_data(path):
    existing = [c.name for c in chroma_client.list_collections()]
    if collection_name_faq not in existing:
        collection = chroma_client.create_collection(
            name=collection_name_faq,
            embedding_function=ef
        )
        df = pd.read_csv(path)

        collection.add(
            documents=df['question'].tolist(),
            metadatas=[{'answer': a} for a in df['answer']],
            ids=[str(i) for i in range(len(df))]
        )
        chroma_client.persist()


def get_relevant_qa(query):
    collection = chroma_client.get_collection(
        name=collection_name_faq,
        embedding_function=ef
    )
    return collection.query(query_texts=[query], n_results=3)


def generate_answer(query, context):
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
        model=os.environ['GROQ_MODEL'],
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content


def faq_chain(query):
    result = get_relevant_qa(query)

    context = "\n\n".join(
        [r.get('answer', '') for r in result['metadatas'][0]]
    )

    if not context.strip():
        return "I don't know"

    return generate_answer(query, context)
