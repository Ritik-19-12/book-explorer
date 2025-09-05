"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

interface Book {
  id: number;
  title: string;
  price: number;
  in_stock: boolean;
  rating: number;
  detail_url: string;
  thumbnail_url: string;
}

export default function BookPage() {
  const { id } = useParams();
  const [book, setBook] = useState<Book | null>(null);

  useEffect(() => {
    if (!id) return;
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/books/${id}`)
      .then((r) => r.json())
      .then(setBook)
      .catch(console.error);
  }, [id]);

  if (!book) return <div className="p-6">Loading...</div>;

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold">{book.title}</h1>
      <img
        src={book.thumbnail_url}
        alt={book.title}
        className="h-72 object-contain my-4"
      />
      <p className="text-lg">Price: £{book.price}</p>
      <p>Status: {book.in_stock ? "✅ In stock" : "❌ Out of stock"}</p>
      <p>Rating: {"⭐".repeat(book.rating || 0)}</p>
      <a
        href={book.detail_url}
        target="_blank"
        rel="noreferrer"
        className="text-blue-600 underline"
      >
        View on BooksToScrape
      </a>
    </div>
  );
}
