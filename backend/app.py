import os
from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from flask_cors import CORS
from backend.models import db, Book
from scraper.scraper import scrape_all_books

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "books.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)

    @app.route("/")
    def home():
        return {"message": "Backend is running 🚀. Try /api/books or /api/refresh"}

    @app.route("/api/books")
    def list_books():
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
        q = request.args.get("q", "").strip()
        rating = request.args.get("rating")
        in_stock = request.args.get("in_stock")
        min_price = request.args.get("min_price")
        max_price = request.args.get("max_price")

        query = Book.query
        if q:
            query = query.filter(Book.title.ilike(f"%{q}%"))
        if rating:
            try:
                query = query.filter_by(rating=int(rating))
            except:
                pass
        if in_stock in ("true", "True", "1", "yes"):
            query = query.filter_by(in_stock=True)
        if in_stock in ("false", "False", "0", "no"):
            query = query.filter_by(in_stock=False)
        if min_price:
            try:
                query = query.filter(Book.price >= float(min_price))
            except:
                pass
        if max_price:
            try:
                query = query.filter(Book.price <= float(max_price))
            except:
                pass

        pagination = query.order_by(Book.id).paginate(page=page, per_page=per_page, error_out=False)
        return jsonify({
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "books": [b.to_dict() for b in pagination.items]
        })

    @app.route("/api/books/<int:book_id>")
    def get_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            abort(404, description="Book not found")
        return jsonify(book.to_dict())

    @app.route("/api/refresh", methods=["POST", "GET"])
    def refresh():
        imported = scrape_all_books(app)
        return jsonify({"status": "ok", "imported": imported})

    @app.cli.command("init-db")
    def init_db():
        """Initialize the database."""
        with app.app_context():
            db.create_all()
            print("✅ Database created successfully!")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
