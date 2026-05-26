"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";

const FAQS = [
  {
    q: "Is this free?",
    a: "Yes — MIT licensed and self-hosted. You run borsa on your own infrastructure. The code costs nothing. The only costs are whatever you pay for server hosting (a $5/mo VPS is plenty) and any provider API tiers you choose.",
  },
  {
    q: "Why BYOK (bring your own keys)?",
    a: "Provider ToS often prohibit reselling or proxying API access. Each user registers accounts directly with the providers they enable, keeping data usage tied to their own provider agreements. Yahoo Finance requires no key.",
  },
  {
    q: "Can I use it commercially?",
    a: "The borsa source code is MIT licensed — use it commercially, fork it, build products on top of it. Whether your use of the underlying provider data is commercially permissible depends on your own provider agreements, not borsa.",
  },
  {
    q: "How do I add a new EGX symbol?",
    a: "Most of the EGX catalog is already bundled. For a missing symbol, edit the symbol dictionary and add the provider-specific tickers. See CONTRIBUTING.md on GitHub for the step-by-step guide.",
  },
  {
    q: "Why not just use yfinance directly?",
    a: "yfinance partially works for EGX, but EGX symbol formats differ per provider (.CA suffix on Yahoo, no suffix on Finnhub, different codes on Alpha Vantage). borsa handles the reconciliation and adds automatic fallback when Yahoo has gaps or rate-limits you.",
  },
];

export function Faq() {
  const [open, setOpen] = useState<number | null>(null);

  return (
    <section className="py-20 px-4 sm:px-6 border-t border-[var(--border)]">
      <div className="max-w-3xl mx-auto space-y-10">
        <div className="space-y-2">
          <h2 className="text-2xl sm:text-3xl font-bold">FAQ</h2>
        </div>

        <div className="space-y-2">
          {FAQS.map((faq, i) => (
            <div
              key={i}
              className="border border-[var(--border)] rounded-lg overflow-hidden"
            >
              <button
                className="w-full flex items-center justify-between px-5 py-4 text-left hover:bg-[var(--muted)] transition-colors"
                onClick={() => setOpen(open === i ? null : i)}
              >
                <span className="font-medium text-sm sm:text-base">{faq.q}</span>
                <ChevronDown
                  className={`w-4 h-4 text-[var(--muted-foreground)] shrink-0 transition-transform duration-200 ${
                    open === i ? "rotate-180" : ""
                  }`}
                />
              </button>
              {open === i && (
                <div className="px-5 pb-5">
                  <p className="text-sm text-[var(--muted-foreground)] leading-relaxed">
                    {faq.a}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
