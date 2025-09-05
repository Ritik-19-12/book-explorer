# 📚 Book Explorer

Book Explorer is a **full-stack web app** that scrapes books from [Books to Scrape](https://books.toscrape.com/), stores them in a database, and lets you **search, filter, and explore** them through a modern Next.js frontend.

---

## 🚀 Features
- Scrapes book data (title, price, stock, rating, image, detail link)
- Flask backend with REST API
- Next.js + Tailwind frontend with search and pagination
- SQLite database by default (easy setup)-
- Click any book to see full details
- API supports filters (search, rating, price range, stock)

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Ritik-19-12/book-explorer.git
cd book-explorer

cd scraper
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python scraper.py

cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

python -c "from app import create_app; app=create_app(); from models import db; `
with app.app_context(): db.create_all(); print('DB created')"

python app.py
Open this in your browser:
👉 http://127.0.0.1:5000/api/refresh

It should return:

{"status":"ok","imported":1000}

cd ../frontend
pnpm install
Create .env.local
NEXT_PUBLIC_API_URL=http://127.0.0.1:5000
pnpm dev

---
👨‍💻 Author

Built by Ritik Sotwal ✨
