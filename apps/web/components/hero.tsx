"use client";

import { useEffect, useState } from "react";
import { BookOpen } from "lucide-react";
import { GithubIcon } from "./icons";

const GITHUB_URL = "https://github.com/omarelsergany/borsa";

const TERMINAL_LINES = [
  { delay: 0, text: "$ curl https://demo.borsa.ashh.me/demo/quote/COMI", type: "cmd" },
  { delay: 900, text: "{", type: "json" },
  { delay: 1100, text: '  "symbol": "COMI",', type: "json" },
  { delay: 1200, text: '  "company": "Commercial International Bank Egypt",', type: "json" },
  { delay: 1300, text: '  "price": 136.0,', type: "json" },
  { delay: 1400, text: '  "source": "Yahoo Finance (COMI.CA)",', type: "json" },
  { delay: 1500, text: '  "currency": "EGP",', type: "json" },
  { delay: 1600, text: '  "api_symbol": "COMI.CA"', type: "json" },
  { delay: 1700, text: "}", type: "json" },
];

function Terminal() {
  const [visibleLines, setVisibleLines] = useState<number>(0);

  useEffect(() => {
    const timers = TERMINAL_LINES.map((line, i) =>
      setTimeout(() => setVisibleLines(i + 1), line.delay + 400)
    );
    return () => timers.forEach(clearTimeout);
  }, []);

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[#0a0a0c] overflow-hidden shadow-2xl">
      {/* Title bar */}
      <div className="flex items-center gap-1.5 px-4 py-3 border-b border-[var(--border)] bg-[#111114]">
        <span className="w-3 h-3 rounded-full bg-red-500/80" />
        <span className="w-3 h-3 rounded-full bg-yellow-500/80" />
        <span className="w-3 h-3 rounded-full bg-green-500/80" />
        <span className="ml-3 text-xs text-[var(--muted-foreground)] font-mono">
          terminal
        </span>
      </div>
      {/* Body */}
      <div className="p-4 font-mono text-sm space-y-1 min-h-[220px]">
        {TERMINAL_LINES.slice(0, visibleLines).map((line, i) => (
          <div key={i} className="flex gap-2">
            {line.type === "cmd" ? (
              <span className="text-green-400 whitespace-pre">{line.text}</span>
            ) : (
              <span
                className={
                  line.text.includes('"symbol"') || line.text.includes('"price"') || line.text.includes('"provider"')
                    ? "text-[var(--accent)]"
                    : "text-[var(--muted-foreground)]"
                }
              >
                {line.text}
              </span>
            )}
          </div>
        ))}
        {visibleLines < TERMINAL_LINES.length && (
          <span className="inline-block w-2 h-4 bg-green-400 cursor-blink" />
        )}
      </div>
    </div>
  );
}

export function Hero() {
  return (
    <section className="relative pt-28 pb-20 px-4 sm:px-6 overflow-hidden">
      {/* Background grid */}
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `linear-gradient(var(--foreground) 1px, transparent 1px), linear-gradient(90deg, var(--foreground) 1px, transparent 1px)`,
          backgroundSize: "40px 40px",
        }}
      />
      {/* Radial glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-[var(--accent)]/5 rounded-full blur-3xl pointer-events-none" />

      <div className="relative max-w-6xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left */}
          <div className="space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--border)] bg-[var(--muted)] text-xs text-[var(--muted-foreground)] font-mono">
              <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
              MIT licensed · Self-hostable · BYOK
            </div>

            <h1 className="text-4xl sm:text-5xl font-bold leading-tight tracking-tight">
              The open-source API for{" "}
              <span className="gradient-text">Egyptian Exchange</span> data
            </h1>

            <p className="text-lg text-[var(--muted-foreground)] leading-relaxed max-w-lg">
              Self-hostable. BYOK. One docker command. Unified access to Alpha
              Vantage, Finnhub, and Yahoo Finance — with automatic fallback.
            </p>

            <div className="flex flex-wrap gap-3">
              <a
                href={GITHUB_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-5 py-2.5 rounded-md bg-[var(--accent)] text-white font-medium hover:bg-[var(--accent)]/90 transition-colors glow-accent"
              >
                <GithubIcon className="w-4 h-4" />
                View on GitHub
              </a>
              <a
                href="#docs"
                className="flex items-center gap-2 px-5 py-2.5 rounded-md border border-[var(--border)] text-[var(--foreground)] font-medium hover:bg-[var(--muted)] transition-colors"
              >
                <BookOpen className="w-4 h-4" />
                Read the docs
              </a>
            </div>

            <div className="flex items-center gap-6 pt-2 text-sm text-[var(--muted-foreground)]">
              <span className="font-mono">docker compose up</span>
              <span className="w-px h-4 bg-[var(--border)]" />
              <span>15+ EGX symbols</span>
              <span className="w-px h-4 bg-[var(--border)]" />
              <span>3 providers</span>
            </div>
          </div>

          {/* Right — Terminal */}
          <div className="relative">
            <Terminal />
          </div>
        </div>
      </div>
    </section>
  );
}
