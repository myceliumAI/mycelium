# Security Policy

## Supported Versions

Currently supported versions of Mycelium with security updates:

| Version | Supported          |
| ------- | ------------------ |

*(no version released yet)*


## Reporting a Vulnerability

We take the security of Mycelium seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Reporting Process

1. **DO NOT** create a public GitHub issue for the vulnerability.
2. Send a detailed report to sporolyum@gmail.com including:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fixes (if any)
   - Your contact information for follow-up

### What to Expect

1. **Initial Response**: You will receive an acknowledgment within 48 hours.
2. **Status Updates**: 
   - We will provide status updates every 72 hours
   - A full assessment will be provided within 7 days

### Security Measures

Our project implements several security measures:
- Keycloak authentication/authorization
- Environment variable protection
- PostgreSQL security best practices
- Docker container isolation
- AGPL v3 license compliance requirements

### Scope

The following are in scope for security reports:
- Backend API endpoints (`/backend/api`)
- Authentication system (Keycloak integration)
- Database access and management
- Frontend security concerns (`/mycelium`)
- Docker container configurations

### Out of Scope

- Issues in dependencies (report to their respective projects)
- Issues in development environment
- Issues that require physical access
- Social engineering attacks

### Disclosure Policy

- We follow responsible disclosure principles
- Public disclosure timing will be coordinated with the reporter
- Reporters will be credited (unless they prefer to remain anonymous)
- Fixes will be released as security patches

### Security Updates

Security patches will be released as:
- Immediate patches for critical vulnerabilities
- Regular updates for non-critical issues
- Version updates in the changelog

### Contact

For sensitive security issues:
- Email: sporolyum@gmail.com
- Response Time: Within 48 hours

For general security questions:
- GitHub Issues (non-vulnerability related)
- Project Documentation

---

