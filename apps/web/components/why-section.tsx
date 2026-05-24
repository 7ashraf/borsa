import { Puzzle, Code2, Unlock } from "lucide-react";

const CARDS = [
  {
    icon: Puzzle,
    title: "Fragmented data",
    body: "Different providers cover different EGX symbols with different formats. Alpha Vantage may have COMI but not EAST. Yahoo coverage varies by symbol variant. You end up writing glue code forever.",
  },
  {
    icon: Code2,
    title: "No clean Python interface",
    body: "yfinance partially works, but EGX symbol formats are inconsistent across providers — .CA, .EY, no suffix. You spend hours on reconciliation before writing a single line of real logic.",
  },
  {
    icon: Unlock,
    title: "Open by default",
    body: "MIT licensed, self-hostable, no vendor lock-in. Your API keys stay on your server. The fallback logic, the schema normalization, and the symbol dictionary are all yours to fork.",
  },
];

export function WhySection() {
  return (
    <section className="py-20 px-4 sm:px-6 border-t border-[var(--border)]">
      <div className="max-w-6xl mx-auto space-y-12">
        <div className="space-y-2">
          <h2 className="text-2xl sm:text-3xl font-bold">Why it exists</h2>
          <p className="text-[var(--muted-foreground)] max-w-xl">
            The Egyptian Exchange is one of the oldest in the world — yet it
            remains dramatically underserved by developer tooling.
          </p>
        </div>

        <div className="grid sm:grid-cols-3 gap-6">
          {CARDS.map((card) => {
            const Icon = card.icon;
            return (
              <div
                key={card.title}
                className="p-6 rounded-lg border border-[var(--border)] bg-[var(--card)] space-y-4 hover:border-[var(--accent)]/40 transition-colors group"
              >
                <div className="w-10 h-10 rounded-md bg-[var(--accent)]/10 flex items-center justify-center group-hover:bg-[var(--accent)]/20 transition-colors">
                  <Icon className="w-5 h-5 text-[var(--accent)]" />
                </div>
                <h3 className="font-semibold">{card.title}</h3>
                <p className="text-sm text-[var(--muted-foreground)] leading-relaxed">
                  {card.body}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
