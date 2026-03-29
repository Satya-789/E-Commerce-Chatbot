# 🛒 E-Commerce Chatbot (AI Powered)

## 📌 Overview

An intelligent **AI-powered E-commerce chatbot** built using **Streamlit, Groq LLM, ChromaDB, and SQLite**.
It allows users to interact in natural language to:

* 📚 Get instant answers to FAQs
* 🛍️ खोज and discover products effortlessly

---

## 🚀 Features

✨ **Smart Conversational UI**

> Chat-based interface powered by Streamlit

🔎 **Natural Language Product Search**

> Converts user queries into SQL automatically

📚 **FAQ Intelligence (RAG-based)**

> Uses ChromaDB for semantic search

🔗 **Clickable Product Links**

> Direct navigation to products

⚡ **Lightweight & Fast**

> No heavy ML models → optimized for cloud deployment

---

## 🏗️ Project Structure

```
ecommerce-chatbot/
│
├── main.py              # Streamlit UI
├── faq.py               # FAQ retrieval (ChromaDB)
├── sql.py               # Product search (SQL + LLM)
├── router.py            # Query routing (FAQ / SQL)
│
├── db.sqlite            # Product database
├── resources/
│   └── faq_data.csv     # FAQ dataset
│
├── requirements.txt
└── README.md
```

---

## 💡 Example Queries

### 📚 FAQ Queries

* What is your return policy?
* Do you accept cash on delivery?
* How can I track my order?

### 🛍️ Product Queries

* Show shoes under 2000
* Nike shoes with discount
* Best rated running shoes

---

## 🛠️ Tech Stack

| Layer      | Technology     |
| ---------- | -------------- |
| Frontend   | Streamlit      |
| LLM        | Groq (LLaMA 3) |
| Vector DB  | ChromaDB       |
| Database   | SQLite         |
| Data Tools | Pandas         |

---

## 🌐 Live Demo

🔗 **Try it here:**
👉 https://e-commerce-chatbot-n.streamlit.app/

---

## 🎯 Key Highlights

* 💬 End-to-end conversational AI system
* ⚡ Fast response using Groq LLM
* 🧠 Hybrid architecture (RAG + SQL)
* ☁️ Fully deployable on Streamlit Cloud

---

