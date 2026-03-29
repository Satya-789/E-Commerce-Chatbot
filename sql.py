from groq import Groq
import os
import re
import sqlite3
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
client = Groq()

db_path = Path(__file__).parent / "db.sqlite"

sql_prompt = """
Generate SQL using this schema:

table: product
columns: product_link, title, brand, price, discount, avg_rating, total_ratings

Rules:
- Always SELECT *
- Use LIKE '%keyword%' for search
- Return SQL inside <SQL></SQL>
"""

def generate_sql_query(question):
    res = client.chat.completions.create(
        messages=[
            {"role": "system", "content": sql_prompt},
            {"role": "user", "content": question}
        ],
        model=GROQ_MODEL
    )
    return res.choices[0].message.content

def run_query(query):
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)

def sql_chain(question):
    sql_text = generate_sql_query(question)

    match = re.findall(r"<SQL>(.*?)</SQL>", sql_text, re.DOTALL)

    if not match:
        return "Could not understand request."

    query = match[0].strip()
    print(query)

    df = run_query(query)

    if df.empty:
        return "No products found."

    result = ""

    for i, row in df.iterrows():
        discount = int(row["discount"] * 100)

        result += f"""
{i+1}. {row['title']}
💰 Rs.{row['price']} ({discount}% off)
⭐ {row['avg_rating']}
👉 <a href="{row['product_link']}" target="_blank">Buy Now</a>

"""

    return result
