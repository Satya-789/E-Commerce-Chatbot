import sqlite3
import pandas as pd
import os
from groq import Groq

client = Groq()

db_path = "db.sqlite"

def sql_chain(question):
    conn = sqlite3.connect(db_path)

    query = "SELECT * FROM product LIMIT 5"
    df = pd.read_sql_query(query, conn)

    if df.empty:
        return "No products found."

    result = ""
    for i, row in df.iterrows():
        result += f"{i+1}. {row['title']} - Rs.{row['price']}\n"

    return result
