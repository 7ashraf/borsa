"use client";

import { useState } from "react";
import { SyntaxHighlight } from "./syntax-highlight";

const TABS = [
  {
    label: "curl",
    language: "bash",
    code: `BASE="https://demo.borsa.ashh.me"

# Check the demo API
curl "$BASE/v1/health"

# Fetch one quote
curl "$BASE/demo/quote/COMI"

# List all EGX symbols
curl "$BASE/v1/stocks"`,
  },
  {
    label: "Python",
    language: "python",
    code: `import requests

BASE = "https://demo.borsa.ashh.me"

# Fetch a quote
resp = requests.get(f"{BASE}/demo/quote/COMI", timeout=10)
resp.raise_for_status()
quote = resp.json()

print(f"{quote['company']}: {quote['price']} {quote['currency']}")
print(f"Source: {quote['source']}")

# List all EGX symbols
symbols = requests.get(f"{BASE}/v1/stocks", timeout=10).json()
print(f"Total symbols: {symbols['count']}")`,
  },
  {
    label: "JavaScript",
    language: "javascript",
    code: `const BASE = "https://demo.borsa.ashh.me";

// Fetch a quote
const res = await fetch(\`\${BASE}/demo/quote/COMI\`);
if (!res.ok) throw new Error(\`HTTP \${res.status}\`);
const quote = await res.json();

console.log(\`\${quote.company}: \${quote.price} \${quote.currency}\`);
console.log(\`Source: \${quote.source}\`);

// List all EGX symbols
const symbols = await fetch(\`\${BASE}/v1/stocks\`).then(r => r.json());
console.log(\`Total symbols: \${symbols.count}\`);`,
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
