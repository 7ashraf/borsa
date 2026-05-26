"use client";

import { useState } from "react";
import { BORSA_API_BASE_URL } from "@/lib/config";
import { GITHUB_URL } from "@/lib/links";
import { GithubIcon } from "./icons";
import { SyntaxHighlight } from "./syntax-highlight";

const EGX_SYMBOLS = [
  "CIBEA",
  "COMI",
  "EAST",
  "EKHO",
  "ETEL",
  "HRHO",
  "JUFO",
  "MFPC",
  "OCDI",
  "ORWE",
  "PHDC",
  "SMSA",
  "SUGR",
  "SWDY",
  "TALM",
];

export function LiveDemo() {
  const [symbol, setSymbol] = useState("CIBEA");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function fetchQuote() {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${BORSA_API_BASE_URL}/demo/quote/${symbol}`);
      const data = await res.json();
      setResult(JSON.stringify(data, null, 2));
    } catch {
      setError("Failed to reach the demo API. Try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="py-20 px-4 sm:px-6 border-t border-[var(--border)]">
      <div className="max-w-3xl mx-auto space-y-8">
        <div className="space-y-2">
          <h2 className="text-2xl sm:text-3xl font-bold">Try it now</h2>
          <p className="text-[var(--muted-foreground)]">
            Hits a live instance. 50 requests/day shared across all visitors —
            for evaluation only.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <select
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            className="flex-1 px-3 py-2 rounded-md border border-[var(--border)] bg-[var(--muted)] text-[var(--foreground)] font-mono text-sm focus:outline-none focus:ring-2 focus:ring-[var(--ring)]"
          >
            {EGX_SYMBOLS.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>

          <button
            onClick={fetchQuote}
            disabled={loading}
            className="px-5 py-2 rounded-md bg-[var(--accent)] text-white font-medium hover:bg-[var(--accent)]/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors whitespace-nowrap"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                </svg>
                Fetching…
              </span>
            ) : (
              "Fetch quote"
            )}
          </button>
        </div>

        {error && (
          <div className="rounded-md border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400">
            {error}
          </div>
        )}

        {result && (
          <div className="rounded-lg border border-[var(--border)] overflow-hidden">
            <div className="flex items-center justify-between px-4 py-2 bg-[var(--muted)] border-b border-[var(--border)]">
              <span className="text-xs font-mono text-[var(--muted-foreground)]">
                GET /demo/quote/{symbol}
              </span>
              <span className="text-xs text-green-400">200 OK</span>
            </div>
            <SyntaxHighlight code={result} language="json" />
          </div>
        )}

        <p className="text-sm text-[var(--muted-foreground)]">
          Want unlimited?{" "}
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-[var(--foreground)] underline underline-offset-4 hover:text-[var(--accent)] transition-colors"
          >
            <GithubIcon className="w-3.5 h-3.5" />
            Self-host in 60 seconds
          </a>
        </p>
      </div>
    </section>
  );
}
