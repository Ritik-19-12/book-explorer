"use client";

import { useState, useEffect } from "react";
import BookCard from "./components/BookCard";
import Pagination from "./components/Pagination";

interface Book {
  id: number;
  title: string;
  price: number;
  in_stock: boolean;
  rating: number;
  detail_url: string;
  thumbnail_url: string;
}

export default function HomePage() {
  const [books, setBooks] = useState<Book[]>([]);
  const [page, setPage] = useState(1);
  const [q, setQ] = useState("");
  const [total, setTotal] = useState(0);

  useEffect(() => {
    const per_page = 20;
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/books?page=${page}&per_page=${per_page}&q=${encodeURIComponent(
      q
    )}`;

    fetch(url)
      .then((r) => r.json())
      .then((data) => {
        setBooks(data.books);
        setTotal(data.total);
      })
      .catch(console.error);
  }, [page, q]);

  const refresh = () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/refresh`;
    fetch(url, { method: "POST" })
      .then(() => {
        console.log("Data refresh triggered");
        // Optionally re-fetch books after refresh
        setPage(1);
      })
      .catch((error) => {
        console.error("Error triggering data refresh:", error);
      });
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4">Book Explorer</h1>

      <input
        type="text"
        placeholder="Search by title..."
        value={q}
        onChange={(e) => {
          setQ(e.target.value);
          setPage(1);
        }}
        className="border px-3 py-2 mb-4 w-full max-w-md"
      />

      <button
        onClick={refresh}
        className="mb-4 px-4 py-2 bg-blue-500 text-white rounded"
      >
        Refresh
      </button>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {books.map((b) => (
          <BookCard key={b.id} book={b} />
        ))}
      </div>

      <Pagination total={total} page={page} setPage={setPage} />
    </div>
  );
}
