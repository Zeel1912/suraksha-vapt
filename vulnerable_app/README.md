# SURAKSHA Vulnerable Test Environment

This directory contains a deliberately vulnerable web application designed for educational purposes in the SURAKSHA VAPT platform.

## ⚠️ WARNING

**This application contains intentional security vulnerabilities and should NEVER be exposed to the internet or used in production environments.**

## Purpose

This vulnerable environment provides safe, controlled targets for testing various security vulnerabilities and demonstrating professional pentesting techniques.

## Vulnerabilities Included

- **SQL Injection**: Login forms and search functionality
- **Cross-Site Scripting (XSS)**: Comment system and search forms
- **Cross-Site Request Forgery (CSRF)**: Money transfer forms
- **Directory Traversal**: File viewer functionality
- **Broken Authentication**: Weak session management
- **Insecure Cookies**: Missing security flags
- **Security Misconfiguration**: Exposed sensitive information
- **Outdated Components**: PHP info disclosure

## Setup

1. Ensure PHP and MySQL are installed
2. The application will automatically create the necessary database and tables
3. Start the server: `python3 server.py`
4. Access at: http://localhost:8080

## Test Credentials

- **Username**: admin, **Password**: admin123
- **Username**: user, **Password**: password

## Usage

Use this environment with the SURAKSHA VAPT platform to:
- Test vulnerability scanning modules
- Practice penetration testing techniques
- Learn attack mitigation strategies
- Understand real-world security concepts

## Security Notice

- Only run this on localhost
- Never expose port 8080 to the internet
- Use only for educational cybersecurity training
- Delete this environment when not in use