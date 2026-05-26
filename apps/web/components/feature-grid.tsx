import {
  Layers,
  Database,
  Zap,
  GitBranch,
  Shield,
  BookOpen,
} from "lucide-react";

const FEATURES = [
  {
    icon: Layers,
    title: "Multi-provider fallback",
    body: "Configured providers are tried automatically. If one fails or rate-limits, borsa falls through to the next source.",
  },
  {
    icon: Database,
    title: "200+ EGX symbols pre-configured",
    body: "The EGX catalog is bundled with provider-specific ticker mapping handled for you.",
  },
  {
    icon: Zap,
    title: "In-process caching",
    body: "TTL-based cache with configurable size. Responses served in microseconds on cache hit.",
  },
  {
    icon: GitBranch,
    title: "Async parallel fetching",
    body: "Built on FastAPI and httpx. Non-blocking I/O means fast p99 even under concurrent load.",
  },
  {
    icon: Shield,
    title: "Type-safe with Pydantic",
    body: "Every response is a validated Pydantic model. No surprise null fields, no string-typed numbers.",
  },
  {
    icon: BookOpen,
    title: "Open source (MIT)",
    body: "Fork it, extend it, deploy it. No vendor lock-in, no per-seat pricing, no usage telemetry.",
  },
];

export function FeatureGrid() {
  return (
    <section className="py-20 px-4 sm:px-6 border-t border-[var(--border)]">
      <div className="max-w-6xl mx-auto space-y-12">
        <div className="space-y-2">
          <h2 className="text-2xl sm:text-3xl font-bold">Features</h2>
          <p className="text-[var(--muted-foreground)]">
            Everything you need to build on EGX data, nothing you don&apos;t.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {FEATURES.map((f) => {
            const Icon = f.icon;
            return (
              <div
                key={f.title}
                className="p-5 rounded-lg border border-[var(--border)] bg-[var(--card)] hover:border-[var(--accent)]/40 transition-colors group"
              >
                <div className="flex items-start gap-4">
                  <div className="mt-0.5 w-8 h-8 rounded-md bg-[var(--accent)]/10 flex items-center justify-center shrink-0 group-hover:bg-[var(--accent)]/20 transition-colors">
                    <Icon className="w-4 h-4 text-[var(--accent)]" />
                  </div>
                  <div className="space-y-1">
                    <h3 className="text-sm font-semibold">{f.title}</h3>
                    <p className="text-xs text-[var(--muted-foreground)] leading-relaxed">
                      {f.body}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
