"use client";

import { useTheme } from "./theme-provider";
import { Sun, Moon, Star } from "lucide-react";
import { GithubIcon } from "./icons";
import { useState, useEffect } from "react";
import { DOCS_URL, GITHUB_API_URL, GITHUB_URL } from "@/lib/links";

export function Navbar() {
  const { theme, toggle } = useTheme();
  const [stars, setStars] = useState<number | null>(null);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    fetch(GITHUB_API_URL)
      .then((r) => r.json())
      .then((d) => {
        if (typeof d.stargazers_count === "number") {
          setStars(d.stargazers_count);
        }
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 10);
    window.addEventListener("scroll", handler, { passive: true });
    return () => window.removeEventListener("scroll", handler);
  }, []);

  return (
    <header
      className={`fixed top-0 inset-x-0 z-50 transition-all duration-200 ${
        scrolled
          ? "bg-[var(--background)]/90 backdrop-blur border-b border-[var(--border)]"
          : "bg-transparent"
      }`}
    >
      <nav className="max-w-6xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
        <a href="/" className="flex items-center gap-2 group">
          <span className="text-lg font-bold tracking-tight text-[var(--foreground)]">
            borsa
          </span>
          <span className="text-xs text-[var(--muted-foreground)] font-mono hidden sm:inline">
            بورصة
          </span>
        </a>

        <div className="flex items-center gap-1 sm:gap-2">
          <a
            href={DOCS_URL}
            className="px-3 py-1.5 text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors"
          >
            Docs
          </a>

          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-md border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:border-[var(--muted-foreground)] transition-all"
          >
            <GithubIcon className="w-4 h-4" />
            <span className="hidden sm:inline">GitHub</span>
            {stars !== null && (
              <span className="flex items-center gap-0.5 text-xs bg-[var(--muted)] px-1.5 py-0.5 rounded-full">
                <Star className="w-3 h-3 fill-yellow-500 text-yellow-500" />
                {stars >= 1000 ? `${(stars / 1000).toFixed(1)}k` : stars}
              </span>
            )}
          </a>

          <button
            onClick={toggle}
            className="p-2 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--muted)] transition-all"
            aria-label="Toggle theme"
          >
            {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>
        </div>
      </nav>
    </header>
  );
}
