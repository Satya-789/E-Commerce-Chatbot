from groq import Groq
import os
import re
import sqlite3
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# ---------- Load env ----------
load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# ---------- DB Path ----------
db_path = Path(__file__).parent / "db.sqlite"

# ---------- Groq Client ----------
client_sql = Groq()

# ---------- SQL Prompt ----------
sql_prompt = """
You are an expert in SQL.

Generate a SQL query based on the question.

Schema:
table: product

fields:
product_link (string)
title (string)
brand (string)
price (integer)
discount (float)
avg_rating (float)
total_ratings (integer)

Rules:
- Always use SELECT *
- Use LIKE for brand search
- Return only SQL inside <SQL></SQL>

Example:
<SQL>SELECT * FROM product WHERE price < 3000</SQL>
"""

# ---------- Generate SQL ----------
def generate_sql_query(question):
    completion = client_sql.chat.completions.create(
        messages=[
            {"role": "system", "content": sql_prompt},
            {"role": "user", "content": question}
        ],
        model=GROQ_MODEL,
        temperature=0.2
    )

    return completion.choices[0].message.content


# ---------- Run SQL ----------
def run_query(query):
    if query.strip().upper().startswith("SELECT"):
        with sqlite3.connect(db_path) as conn:
            return pd.read_sql_query(query, conn)


# ---------- MAIN CHAIN ----------
def sql_chain(question):
    # Step 1: Generate SQL
    sql_query = generate_sql_query(question)

    # Step 2: Extract SQL
    pattern = "<SQL>(.*?)</SQL>"
    matches = re.findall(pattern, sql_query, re.DOTALL)

    if not matches:
        return "❌ Could not understand your request."

    query = matches[0].strip()
    print("Generated SQL:", query)

    # Step 3: Execute
    df = run_query(query)

    if df is None or df.empty:
        return "No products found."

    # Step 4: Format output (NO LLM → reliable)
    result = ""

    for i, row in df.iterrows():
        discount_percent = int(row["discount"] * 100)

        result += f"""
{i+1}. {row['title']}
💰 Price: Rs.{row['price']} ({discount_percent}% off)
⭐ Rating: {row['avg_rating']}
🔗 <a href="{row['product_link']}" target="_blank">View Product</a>

"""

    return result


# ---------- TEST ----------
if __name__ == "__main__":
    question = "Show top 3 shoes under 3000"
    print(sql_chain(question))
