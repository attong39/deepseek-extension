# Security Policy

## Reporting a Vulnerability
Please report vulnerabilities privately via GitHub Security Advisories or email: security@zeta-ai.vn.

## Dependencies
- Weekly Dependabot updates are enabled for npm, pip, and actions.
- Weekly security audit workflow runs npm audit and pip-audit (non-blocking).

## Secrets
- Do not commit secrets. Use environment variables or secret managers.
- Consider Vault or AWS Secrets Manager for production.

## Hardening
- Keep CI enforcing lint/tests
- Prefer least privilege and network isolation between services
- Use HTTPS/TLS everywhere; enable logging and audit trails
