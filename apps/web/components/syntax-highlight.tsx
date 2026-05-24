"use client";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { useState } from "react";
import { Check, Copy } from "lucide-react";

interface Props {
  code: string;
  language: string;
  showCopy?: boolean;
}

export function SyntaxHighlight({ code, language, showCopy = false }: Props) {
  const [copied, setCopied] = useState(false);

  function copy() {
    navigator.clipboard.writeText(code).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  }

  return (
    <div className="relative group">
      {showCopy && (
        <button
          onClick={copy}
          className="absolute top-3 right-3 z-10 p-1.5 rounded border border-[var(--border)] bg-[var(--muted)] opacity-0 group-hover:opacity-100 transition-opacity text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
          aria-label="Copy code"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
        </button>
      )}
      <SyntaxHighlighter
        language={language}
        style={oneDark}
        customStyle={{
          margin: 0,
          padding: "16px",
          background: "#0a0a0c",
          fontSize: "13px",
          lineHeight: "1.6",
          fontFamily: '"JetBrains Mono", "Fira Code", ui-monospace, monospace',
          borderRadius: 0,
        }}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}
