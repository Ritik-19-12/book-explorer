# backend/scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import hashlib
from models import db, Book

BASE = "https://books.toscrape.com/"

def rating_str_to_int(cls_list):
    # class like ['star-rating', 'Three']
    mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    for c in cls_list:
        if c in mapping:
            return mapping[c]
    return None

def scrape_page(url, session):
    r = session.get(url, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    books = []
    articles = soup.select("article.product_pod")

    for a in articles:
        title = a.h3.a["title"].strip()
        detail_rel = a.h3.a["href"]
        detail_url = urljoin(url, detail_rel)

        # ---- FIXED PRICE CLEANING ----
        price_text = a.select_one(".price_color").text.strip()
        clean_price = (
            price_text
            .replace("£", "")
            .replace("Â", "")
            .replace("$", "")
            .strip()
        )
        price = float(clean_price)

        availability = a.select_one(".availability").text.strip()
        in_stock = "In stock" in availability
        rating = rating_str_to_int(a.p.get("class", []))
        thumb_rel = a.select_one("img")["src"]
        thumbnail_url = urljoin(url, thumb_rel)

        unique_hash = hashlib.sha1(detail_url.encode("utf-8")).hexdigest()

        books.append({
            "title": title,
            "price": price,
            "in_stock": in_stock,
            "rating": rating,
            "detail_url": detail_url,
            "thumbnail_url": thumbnail_url,
            "unique_hash": unique_hash
        })

    return books

def scrape_all_books(app):
    session = requests.Session()
    page_url = BASE
    imported = 0

    with app.app_context():
        while True:
            books = scrape_page(page_url, session)
            # upsert into DB
            for b in books:
                existing = Book.query.filter_by(unique_hash=b["unique_hash"]).first()
                if existing:
                    existing.title = b["title"]
                    existing.price = b["price"]
                    existing.in_stock = b["in_stock"]
                    existing.rating = b["rating"]
                    existing.detail_url = b["detail_url"]
                    existing.thumbnail_url = b["thumbnail_url"]
                else:
                    nb = Book(
                        title=b["title"],
                        price=b["price"],
                        in_stock=b["in_stock"],
                        rating=b["rating"],
                        detail_url=b["detail_url"],
                        thumbnail_url=b["thumbnail_url"],
                        unique_hash=b["unique_hash"]
                    )
                    db.session.add(nb)
                    imported += 1
            db.session.commit()

            # go to next page if exists
            resp = session.get(page_url)
            soup = BeautifulSoup(resp.text, "lxml")
            next_link = soup.select_one("li.next > a")
            if next_link:
                next_rel = next_link["href"]
                page_url = urljoin(page_url, next_rel)
            else:
                break

    return imported
