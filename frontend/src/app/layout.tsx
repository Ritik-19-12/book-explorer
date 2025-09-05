import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Book Explorer",
  description: "Explore books scraped from BooksToScrape",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900">{children}</body>
    </html>
  );
}
