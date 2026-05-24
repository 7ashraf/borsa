import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "borsa — Open-source API for Egyptian Exchange data",
  description:
    "Self-hostable FastAPI service that unifies Alpha Vantage, Finnhub, and Yahoo Finance into one consistent API for EGX market data. Bring your own keys.",
  keywords: ["EGX", "Egyptian Exchange", "stock market API", "Alpha Vantage", "Finnhub", "Yahoo Finance", "open source"],
  openGraph: {
    title: "borsa — Open-source API for Egyptian Exchange data",
    description:
      "Self-hostable. BYOK. One docker command. Unified access to Alpha Vantage, Finnhub, and Yahoo Finance.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={inter.variable} suppressHydrationWarning>
      <head>
        <link
          rel="preconnect"
          href="https://fonts.googleapis.com"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen antialiased">
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
