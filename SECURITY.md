# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | Yes                |
| < 1.0   | Best effort        |

## Reporting a Vulnerability

If you discover a potential security vulnerability in this project, please report it by emailing security@example.com or creating a private security advisory on GitHub.

Do NOT report security vulnerabilities through public GitHub issues.

## Analysis Security Guarantees

This platform performs **static analysis** on URL strings. It does not automatically execute, visit, or fetch external HTTP/HTTPS targets submitted to the API, preventing Server-Side Request Forgery (SSRF) and malicious payload execution during inference.
