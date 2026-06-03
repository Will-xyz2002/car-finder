import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Car Finder CA",
  description: "Find the best used car deals in Canada",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 antialiased">{children}</body>
    </html>
  );
}
