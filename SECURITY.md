# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.x     | :white_check_mark: |

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

To report a security issue, email **security@your-domain.com** with:

1. A description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Any suggested mitigations (optional)

You should receive a response within **48 hours**. If you don't, follow up via email.

We will coordinate disclosure with you and credit you in the release notes (unless you prefer to remain anonymous).

## Security Design Notes

borsa uses a BYOK (bring-your-own-key) architecture. Your third-party API keys are:

- Loaded exclusively from server-side environment variables (`.env`) — never passed in request headers or responses
- Never logged, stored, or included in API error messages
- Scoped to your own self-hosted instance — borsa has no central server that receives your keys

Never commit `.env` files. Use `.env.example` as a template only.
