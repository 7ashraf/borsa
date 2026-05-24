"use client";

import { SyntaxHighlight } from "./syntax-highlight";

const ENDPOINTS = [
  {
    method: "GET",
    path: "/health",
    desc: "Service health + provider status",
    response: `{
  "status": "ok",
  "providers": {
    "alpha_vantage": { "enabled": true, "has_key": true },
    "finnhub": { "enabled": true, "has_key": true },
    "yahoo": { "enabled": true, "has_key": false }
  }
}`,
  },
  {
    method: "GET",
    path: "/symbols",
    desc: "List all pre-configured EGX symbols",
    response: `[
  { "symbol": "COMI", "name": "Commercial International Bank", "sector": "Financials" },
  { "symbol": "CIBEA", "name": "CIB Egypt", "sector": "Financials" },
  ...
]`,
  },
  {
    method: "GET",
    path: "/quotes/{symbol}",
    desc: "Real-time quote: price, OHLC, volume, change",
    response: `{
  "symbol": "COMI",
  "name": "Commercial International Bank",
  "price": 45.80,
  "open": 45.20,
  "high": 46.10,
  "low": 45.00,
  "previous_close": 45.50,
  "change": 0.30,
  "change_percent": 0.659,
  "volume": 1234567,
  "currency": "EGP",
  "provider": "yahoo",
  "fetched_at": "2025-05-24T10:30:00"
}`,
  },
  {
    method: "GET",
    path: "/historical/{symbol}",
    desc: "OHLCV history. Query params: interval=daily|weekly|monthly, period=1mo|3mo|6mo|1y",
    response: `[
  { "date": "2025-05-01", "open": 44.5, "high": 45.0, "low": 44.2, "close": 44.8, "volume": 987654 },
  { "date": "2025-05-02", "open": 44.8, "high": 46.2, "low": 44.7, "close": 45.80, "volume": 1234567 }
]`,
  },
  {
    method: "GET",
    path: "/company/{symbol}",
    desc: "Company fundamentals and metadata",
    response: `{
  "symbol": "COMI",
  "name": "Commercial International Bank Egypt",
  "sector": "Financials",
  "industry": "Banks",
  "country": "Egypt",
  "currency": "EGP",
  "market_cap": null,
  "description": "..."
}`,
  },
  {
    method: "DELETE",
    path: "/cache",
    desc: "Flush the in-process cache",
    response: `{ "message": "Cache cleared", "entries_removed": 42 }`,
  },
];

const ENV_VARS = [
  { name: "ALPHA_VANTAGE_API_KEY", default: "_(empty)_", desc: "Alpha Vantage key — provider disabled if empty" },
  { name: "FINNHUB_API_KEY", default: "_(empty)_", desc: "Finnhub key — provider disabled if empty" },
  { name: "ENABLE_ALPHA_VANTAGE", default: "true", desc: "Feature flag to disable Alpha Vantage entirely" },
  { name: "ENABLE_FINNHUB", default: "true", desc: "Feature flag to disable Finnhub entirely" },
  { name: "ENABLE_YAHOO", default: "true", desc: "Yahoo Finance requires no key" },
  { name: "CACHE_TTL_SECONDS", default: "60", desc: "Seconds before a cached response expires" },
  { name: "CACHE_MAX_SIZE", default: "512", desc: "Maximum entries in the in-process cache" },
  { name: "HOST", default: "0.0.0.0", desc: "Bind address" },
  { name: "PORT", default: "8000", desc: "Bind port" },
  { name: "LOG_LEVEL", default: "info", desc: "debug · info · warning · error" },
];

function MethodBadge({ method }: { method: string }) {
  const colors: Record<string, string> = {
    GET: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    DELETE: "bg-red-500/10 text-red-400 border-red-500/20",
    POST: "bg-green-500/10 text-green-400 border-green-500/20",
  };
  return (
    <span
      className={`px-2 py-0.5 rounded border text-xs font-mono font-semibold ${colors[method] ?? ""}`}
    >
      {method}
    </span>
  );
}

export function DocsContent() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-16">
      <div className="flex gap-8">
        {/* Sidebar TOC */}
        <aside className="hidden lg:block w-48 shrink-0">
          <nav className="sticky top-20 space-y-1 text-sm">
            {[
              ["#quickstart", "Quickstart"],
              ["#endpoints", "Endpoints"],
              ["#env-vars", "Environment"],
              ["#architecture", "Architecture"],
              ["#symbols", "EGX Symbols"],
            ].map(([href, label]) => (
              <a
                key={href}
                href={href}
                className="block text-[var(--muted-foreground)] hover:text-[var(--foreground)] py-1 transition-colors"
              >
                {label}
              </a>
            ))}
          </nav>
        </aside>

        {/* Content */}
        <div className="flex-1 space-y-16 min-w-0">
          <div className="space-y-3">
            <h1 className="text-3xl sm:text-4xl font-bold">Documentation</h1>
            <p className="text-[var(--muted-foreground)] text-lg">
              borsa — self-hostable REST API for Egyptian Exchange market data.
            </p>
          </div>

          {/* Quickstart */}
          <section id="quickstart" className="space-y-4">
            <h2 className="text-xl font-bold border-b border-[var(--border)] pb-2">
              Quickstart
            </h2>
            <div className="rounded-lg border border-[var(--border)] overflow-hidden">
              <SyntaxHighlight
                showCopy
                language="bash"
                code={`git clone https://github.com/omarelsergany/borsa.git
cd borsa
cp .env.example .env
# Add at least one provider key to .env
docker compose up`}
              />
            </div>
            <p className="text-[var(--muted-foreground)] text-sm">
              API available at{" "}
              <code className="font-mono text-[var(--foreground)] bg-[var(--muted)] px-1.5 py-0.5 rounded text-xs">
                http://localhost:8000
              </code>
              . Interactive Swagger docs at{" "}
              <code className="font-mono text-[var(--foreground)] bg-[var(--muted)] px-1.5 py-0.5 rounded text-xs">
                /docs
              </code>
              .
            </p>
          </section>

          {/* Endpoints */}
          <section id="endpoints" className="space-y-6">
            <h2 className="text-xl font-bold border-b border-[var(--border)] pb-2">
              Endpoints
            </h2>
            {ENDPOINTS.map((ep) => (
              <div
                key={ep.path}
                className="border border-[var(--border)] rounded-lg overflow-hidden"
              >
                <div className="flex items-center gap-3 px-4 py-3 bg-[var(--muted)] border-b border-[var(--border)]">
                  <MethodBadge method={ep.method} />
                  <code className="font-mono text-sm text-[var(--foreground)]">
                    {ep.path}
                  </code>
                </div>
                <div className="px-4 py-3 text-sm text-[var(--muted-foreground)]">
                  {ep.desc}
                </div>
                <div className="border-t border-[var(--border)]">
                  <SyntaxHighlight
                    code={ep.response}
                    language="json"
                    showCopy
                  />
                </div>
              </div>
            ))}
          </section>

          {/* Env vars */}
          <section id="env-vars" className="space-y-4">
            <h2 className="text-xl font-bold border-b border-[var(--border)] pb-2">
              Environment variables
            </h2>
            <div className="rounded-lg border border-[var(--border)] overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-[var(--muted)] border-b border-[var(--border)]">
                    <th className="px-4 py-2.5 text-left font-semibold text-[var(--foreground)]">
                      Variable
                    </th>
                    <th className="px-4 py-2.5 text-left font-semibold text-[var(--foreground)] hidden sm:table-cell">
                      Default
                    </th>
                    <th className="px-4 py-2.5 text-left font-semibold text-[var(--foreground)]">
                      Description
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {ENV_VARS.map((v, i) => (
                    <tr
                      key={v.name}
                      className={i % 2 === 0 ? "" : "bg-[var(--muted)]/30"}
                    >
                      <td className="px-4 py-2.5 font-mono text-xs text-[var(--accent)]">
                        {v.name}
                      </td>
                      <td className="px-4 py-2.5 font-mono text-xs text-[var(--muted-foreground)] hidden sm:table-cell">
                        {v.default}
                      </td>
                      <td className="px-4 py-2.5 text-xs text-[var(--muted-foreground)]">
                        {v.desc}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          {/* Architecture */}
          <section id="architecture" className="space-y-4">
            <h2 className="text-xl font-bold border-b border-[var(--border)] pb-2">
              Architecture
            </h2>
            <p className="text-[var(--muted-foreground)] text-sm leading-relaxed">
              borsa is a thin FastAPI service with an in-process TTL cache.
              On a cache miss, the{" "}
              <code className="font-mono text-xs bg-[var(--muted)] px-1.5 py-0.5 rounded">
                StocksService
              </code>{" "}
              tries providers in order: Alpha Vantage → Finnhub → Yahoo Finance.
              A provider is skipped if its key is absent or its feature flag is{" "}
              <code className="font-mono text-xs bg-[var(--muted)] px-1.5 py-0.5 rounded">
                false
              </code>
              . If all fail, the API returns{" "}
              <code className="font-mono text-xs bg-[var(--muted)] px-1.5 py-0.5 rounded">
                503
              </code>{" "}
              with per-provider error details.
            </p>
            <div className="rounded-lg border border-[var(--border)] overflow-hidden">
              <SyntaxHighlight
                language="text"
                code={`Client → FastAPI → TTL Cache (hit → return)
                              ↓ (miss)
                         StocksService
                         ├── Alpha Vantage  (if key set, if enabled)
                         ├── Finnhub        (if key set, if enabled)
                         └── Yahoo Finance  (always enabled)`}
              />
            </div>
          </section>

          {/* Symbols */}
          <section id="symbols" className="space-y-4">
            <h2 className="text-xl font-bold border-b border-[var(--border)] pb-2">
              EGX Symbols
            </h2>
            <p className="text-[var(--muted-foreground)] text-sm">
              15+ EGX symbols pre-configured with provider-specific ticker
              mappings. Use{" "}
              <code className="font-mono text-xs bg-[var(--muted)] px-1.5 py-0.5 rounded">
                GET /symbols
              </code>{" "}
              for the full list at runtime, or see the symbol dictionary in the
              source.
            </p>
            <div className="flex flex-wrap gap-2">
              {[
                "CIBEA","COMI","EAST","EKHO","ETEL",
                "HRHO","JUFO","MFPC","OCDI","ORWE",
                "PHDC","SMSA","SUGR","SWDY","TALM",
              ].map((s) => (
                <span
                  key={s}
                  className="px-2.5 py-1 rounded border border-[var(--border)] bg-[var(--muted)] font-mono text-xs text-[var(--foreground)]"
                >
                  {s}
                </span>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
