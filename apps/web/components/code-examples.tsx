"use client";

import { useState } from "react";
import { SyntaxHighlight } from "./syntax-highlight";

const TABS = [
  {
    label: "curl",
    language: "bash",
    code: `# Fetch a quote
curl https://api.borsa.ashh.me/demo/quote/COMI

# Response:
# {
#   "symbol": "COMI",
#   "name": "Commercial International Bank",
#   "price": 45.80,
#   "open": 45.20,
#   "high": 46.10,
#   "low": 45.00,
#   "previous_close": 45.50,
#   "change": 0.30,
#   "change_percent": 0.659,
#   "volume": 1234567,
#   "currency": "EGP",
#   "provider": "yahoo",
#   "fetched_at": "2025-05-24T10:30:00"
# }

# List all EGX symbols
curl http://localhost:8000/symbols

# Historical data (daily, last month)
curl "http://localhost:8000/historical/COMI?interval=daily&period=1mo"`,
  },
  {
    label: "Python",
    language: "python",
    code: `import requests

BASE = "http://localhost:8000"

# Fetch a quote
resp = requests.get(f"{BASE}/quotes/COMI")
resp.raise_for_status()
quote = resp.json()

print(f"{quote['name']}: {quote['price']} {quote['currency']}")
print(f"Change: {quote['change_percent']:+.2f}%")
print(f"Source: {quote['provider']}")

# List all EGX symbols
symbols = requests.get(f"{BASE}/symbols").json()
print(f"Total symbols: {len(symbols)}")

# Historical data
hist = requests.get(
    f"{BASE}/historical/COMI",
    params={"interval": "daily", "period": "1mo"}
).json()
for row in hist[-5:]:  # last 5 days
    print(f"{row['date']}: close={row['close']}")`,
  },
  {
    label: "JavaScript",
    language: "javascript",
    code: `const BASE = "http://localhost:8000";

// Fetch a quote
const res = await fetch(\`\${BASE}/quotes/COMI\`);
if (!res.ok) throw new Error(\`HTTP \${res.status}\`);
const quote = await res.json();

console.log(\`\${quote.name}: \${quote.price} \${quote.currency}\`);
console.log(\`Change: \${quote.change_percent.toFixed(2)}%\`);
console.log(\`Source: \${quote.provider}\`);

// List all EGX symbols
const symbols = await fetch(\`\${BASE}/symbols\`).then(r => r.json());
console.log(\`Total symbols: \${symbols.length}\`);

// Historical data
const params = new URLSearchParams({ interval: "daily", period: "1mo" });
const hist = await fetch(\`\${BASE}/historical/COMI?\${params}\`).then(r => r.json());
hist.slice(-5).forEach(row => {
  console.log(\`\${row.date}: close=\${row.close}\`);
});`,
  },
];

export function CodeExamples() {
  const [active, setActive] = useState(0);

  return (
    <section className="py-20 px-4 sm:px-6 border-t border-[var(--border)]">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="space-y-2">
          <h2 className="text-2xl sm:text-3xl font-bold">Code examples</h2>
          <p className="text-[var(--muted-foreground)]">
            Same REST API, any language. Consistent response schema regardless
            of which provider answered.
          </p>
        </div>

        <div className="rounded-lg border border-[var(--border)] overflow-hidden">
          {/* Tab bar */}
          <div className="flex border-b border-[var(--border)] bg-[var(--muted)]">
            {TABS.map((tab, i) => (
              <button
                key={tab.label}
                onClick={() => setActive(i)}
                className={`px-4 py-2.5 text-sm font-mono transition-colors ${
                  active === i
                    ? "text-[var(--foreground)] border-b-2 border-[var(--accent)] bg-[var(--card)] -mb-px"
                    : "text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
          {/* Code */}
          <SyntaxHighlight
            code={TABS[active].code}
            language={TABS[active].language}
            showCopy
          />
        </div>
      </div>
    </section>
  );
}
