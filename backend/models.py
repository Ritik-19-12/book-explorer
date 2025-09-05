# backend/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Integer)  # 1..5
    detail_url = db.Column(db.String(1000))
    thumbnail_url = db.Column(db.String(1000))
    unique_hash = db.Column(db.String(200), unique=True, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "in_stock": self.in_stock,
            "rating": self.rating,
            "detail_url": self.detail_url,
            "thumbnail_url": self.thumbnail_url
        }
