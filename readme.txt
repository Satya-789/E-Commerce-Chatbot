# 🛒 E-Commerce Chatbot (AI Powered)

## 📌 Overview

This project is an AI-powered E-commerce chatbot built using **Streamlit, Groq LLM, ChromaDB, and SQLite**.
It can answer FAQs and help users search for products using natural language.

---

## 🚀 Features

* 🤖 AI chatbot interface (Streamlit)
* 📦 Product search using natural language → converted to SQL
* 📚 FAQ answering using vector database (ChromaDB)
* 🔗 Clickable product links
* ⚡ Fast and lightweight (no heavy ML models required)

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
└── README.txt
```

---

## ⚙️ Installation

### 1. Clone the repository

```
git clone https://github.com/your-username/ecommerce-chatbot.git
cd ecommerce-chatbot
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

---

## 🗄️ Database Setup

Run this once to create and insert sample data:

```
python setup_db.py
```

OR manually ensure:

* Table name: `product`
* Columns:

  * product_link
  * title
  * brand
  * price
  * discount
  * avg_rating
  * total_ratings

---

## ▶️ Run the App

```
streamlit run main.py
```

---
---

## 💡 Example Queries

### FAQ

* What is return policy?
* Do you accept cash on delivery?
* How can I track my order?

### Product Search

* Show shoes under 2000
* Nike shoes with discount
* Best rated running shoes

---

---

## 🛠️ Tech Stack

* Streamlit
* Groq LLM
* ChromaDB
* SQLite
* Pandas

---
Link - https://e-commerce-chatbot-n.streamlit.app/


