import { GithubIcon } from "./icons";

const GITHUB_URL = "https://github.com/omarelsergany/borsa";

export function Footer() {
  return (
    <footer className="border-t border-[var(--border)] py-12 px-4 sm:px-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg">borsa</span>
              <span className="text-[var(--muted-foreground)] font-mono text-sm">
                بورصة
              </span>
            </div>
            <p className="text-xs text-[var(--muted-foreground)]">
              MIT License · Made in 🇪🇬
            </p>
          </div>

          <nav className="flex flex-wrap items-center gap-4 text-sm text-[var(--muted-foreground)]">
            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1.5 hover:text-[var(--foreground)] transition-colors"
            >
              <GithubIcon className="w-4 h-4" />
              GitHub
            </a>
            <a
              href="#docs"
              className="hover:text-[var(--foreground)] transition-colors"
            >
              Docs
            </a>
            <a
              href={`${GITHUB_URL}/blob/main/DISCLAIMER.md`}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-[var(--foreground)] transition-colors"
            >
              Disclaimer
            </a>
            <a
              href={`${GITHUB_URL}/blob/main/LICENSE`}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-[var(--foreground)] transition-colors"
            >
              License
            </a>
          </nav>
        </div>

        <div className="mt-8 pt-6 border-t border-[var(--border)] text-xs text-[var(--muted-foreground)] space-y-1">
          <p>
            borsa is not a financial advisor. Data accuracy depends on
            third-party providers. See{" "}
            <a
              href={`${GITHUB_URL}/blob/main/DISCLAIMER.md`}
              target="_blank"
              rel="noopener noreferrer"
              className="underline underline-offset-2 hover:text-[var(--foreground)] transition-colors"
            >
              DISCLAIMER.md
            </a>{" "}
            for full terms.
          </p>
          <p>
            © {new Date().getFullYear()} borsa contributors. MIT licensed.
          </p>
        </div>
      </div>
    </footer>
  );
}
