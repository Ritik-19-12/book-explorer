"use client";

import Link from "next/link";

interface Book {
  id: number;
  title: string;
  price: number;
  in_stock: boolean;
  rating: number;
  thumbnail_url: string;
}

export default function BookCard({ book }: { book: Book }) {
  return (
    <Link href={`/book/${book.id}`}>
      <div className="border rounded p-3 shadow hover:shadow-lg transition cursor-pointer">
        <img
          src={book.thumbnail_url}
          alt={book.title}
          className="h-40 object-contain mx-auto"
        />
        <h3 className="mt-2 font-semibold truncate">{book.title}</h3>
        <p>£{book.price.toFixed(2)}</p>
        <p>{book.in_stock ? "In stock" : "Out of stock"}</p>
        <p>{"⭐".repeat(book.rating || 0)}</p>
      </div>
    </Link>
  );
}
