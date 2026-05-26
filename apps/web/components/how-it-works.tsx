"use client";

import { SyntaxHighlight } from "./syntax-highlight";
import { GITHUB_URL } from "@/lib/links";

const STEPS = [
  {
    number: "01",
    title: "Clone the repo",
    description: "Get the code and copy the environment template.",
    code: `git clone ${GITHUB_URL}.git
cd borsa
cp .env.example .env`,
    lang: "bash",
  },
  {
    number: "02",
    title: "Add your API keys",
    description:
      "Add keys for the providers you want to enable. Yahoo Finance needs no key.",
    code: `# .env
ALPHA_VANTAGE_KEY=your_key_here
FINNHUB_KEY=your_key_here

# Get free keys at:
# → alphavantage.co/support/#api-key
# → finnhub.io/register`,
    lang: "bash",
  },
  {
    number: "03",
    title: "Start the service",
    description:
      "One command. API live at localhost:8000. Interactive docs at /docs.",
    code: `docker compose up

# Or without Docker:
uv sync && uv run uvicorn borsa.main:app --reload

# Query it:
curl http://localhost:8000/v1/quote/COMI`,
    lang: "bash",
  },
];

export function HowItWorks() {
  return (
    <section className="py-20 px-4 sm:px-6 border-t border-[var(--border)]">
      <div className="max-w-6xl mx-auto space-y-12">
        <div className="space-y-2">
          <h2 className="text-2xl sm:text-3xl font-bold">How it works</h2>
          <p className="text-[var(--muted-foreground)]">
            From zero to a running EGX API in under 60 seconds.
          </p>
        </div>

        <div className="space-y-8">
          {STEPS.map((step, i) => (
            <div key={i} className="grid lg:grid-cols-2 gap-6 items-start">
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <span className="text-4xl font-bold font-mono text-[var(--accent)]/30">
                    {step.number}
                  </span>
                  <h3 className="text-lg font-semibold">{step.title}</h3>
                </div>
                <p className="text-[var(--muted-foreground)] pl-14 leading-relaxed">
                  {step.description}
                </p>
              </div>
              <div className="rounded-lg border border-[var(--border)] overflow-hidden">
                <SyntaxHighlight
                  code={step.code}
                  language={step.lang}
                  showCopy
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
