import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PaperPilot — Agentic Research Assistant",
  description:
    "Multi-agent AI research assistant. Generates structured research briefs from ArXiv, HackerNews, Wikipedia, Tavily, and DEV.to.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full">
      <body className="h-full antialiased">{children}</body>
    </html>
  );
}
