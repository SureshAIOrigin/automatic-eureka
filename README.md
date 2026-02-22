# automatic-eureka
SSSAIO-SAO-SSO-Auto-Eur

## Website Checker Tool

A comprehensive tool to check website functionality, performance, and health.

### Features

- ✅ **Connectivity Check**: Verifies HTTP/HTTPS connectivity and status codes
- ⏱️ **Performance Measurement**: Measures website response times
- 🔒 **SSL Certificate Validation**: Checks certificate validity and expiration
- 📄 **Content Validation**: Validates basic HTML structure
- 🛡️ **Security Headers**: Checks for common security headers

### Usage

```bash
python website_checker.py <URL>
```

### Examples

Check a website with HTTPS:
```bash
python website_checker.py https://example.com
```

Check a website (HTTPS will be added automatically if no scheme is provided):
```bash
python website_checker.py example.com
```

### What It Checks

1. **Connectivity**: Can the website be reached? Returns HTTP status code.
2. **Response Time**: How fast does the website respond? Measures total time including content download (Excellent: <200ms, Good: <500ms, Fair: <1000ms, Slow: ≥1000ms)
3. **SSL Certificate**: For HTTPS sites, validates the SSL certificate and checks expiration date.
4. **Content Structure**: Validates presence of basic HTML elements (html, head, body, title tags).
5. **HTTP Headers**: Checks for security headers like X-Content-Type-Options, X-Frame-Options, Content-Security-Policy, and Strict-Transport-Security.

### Requirements

- Python 3.x (uses only standard library modules)

### Exit Codes

- `0`: Website is reachable and checks passed
- `1`: Website is not reachable or connectivity check failed
