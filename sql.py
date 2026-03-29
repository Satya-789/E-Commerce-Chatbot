from groq import Groq
import os, re, sqlite3
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

client = Groq()
db_path = Path(__file__).parent / "db.sqlite"

def is_safe_query(q):
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP"]
    return q.strip().upper().startswith("SELECT") and not any(x in q.upper() for x in forbidden)

def generate_sql(question):
    prompt = f"""
Generate SQL for this question:
{question}

Table: product
Columns: title, brand, price, discount, avg_rating, total_ratings, product_link

Use LIKE for brand.
Always LIMIT 5.

Return inside <SQL></SQL>
"""
    res = client.chat.completions.create(
        model=os.environ['GROQ_MODEL'],
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content

def run_query(q):
    if not is_safe_query(q):
        return None
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(q, conn)

def format_products(df):
    output = []
    for i, r in df.iterrows():
        output.append(
            f"{i+1}. {r['title']} - Rs.{r['price']} "
            f"({int(r['discount']*100)}% off), ⭐ {r['avg_rating']}\n{r['product_link']}"
        )
    return "\n\n".join(output)

def sql_chain(question):
    raw = generate_sql(question)

    match = re.findall("<SQL>(.*?)</SQL>", raw, re.DOTALL)
    sql = match[0] if match else raw

    if "LIMIT" not in sql.upper():
        sql += " LIMIT 5"

    df = run_query(sql)

    if df is None:
        return "Invalid query."
    if df.empty:
        return "No products found."

    return format_products(df)
