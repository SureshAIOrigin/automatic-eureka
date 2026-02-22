#!/usr/bin/env python3
"""
Website Checker Tool
Checks website functionality, performance, and health.
"""

import sys
import time
import ssl
import socket
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
from datetime import datetime


class WebsiteChecker:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        self.results = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }
    
    def check_connectivity(self):
        """Check if the website is reachable via HTTP/HTTPS"""
        print(f"\n[1/5] Checking connectivity to {self.url}...")
        try:
            req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0 (Website Checker)'})
            response = urlopen(req, timeout=10)
            status_code = response.getcode()
            self.results['checks']['connectivity'] = {
                'status': 'PASS',
                'status_code': status_code,
                'message': f'Successfully connected (HTTP {status_code})'
            }
            print(f"  ✓ Status Code: {status_code}")
            return True
        except HTTPError as e:
            self.results['checks']['connectivity'] = {
                'status': 'FAIL',
                'status_code': e.code,
                'message': f'HTTP Error: {e.code} - {e.reason}'
            }
            print(f"  ✗ HTTP Error: {e.code} - {e.reason}")
            return False
        except URLError as e:
            self.results['checks']['connectivity'] = {
                'status': 'FAIL',
                'message': f'Connection failed: {str(e.reason)}'
            }
            print(f"  ✗ Connection failed: {e.reason}")
            return False
        except Exception as e:
            self.results['checks']['connectivity'] = {
                'status': 'FAIL',
                'message': f'Error: {str(e)}'
            }
            print(f"  ✗ Error: {e}")
            return False
    
    def check_response_time(self):
        """Measure website response time"""
        print(f"\n[2/5] Checking response time...")
        try:
            req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0 (Website Checker)'})
            start_time = time.time()
            response = urlopen(req, timeout=10)
            response.read()
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            # Categorize response time
            if response_time < 200:
                performance = 'Excellent'
            elif response_time < 500:
                performance = 'Good'
            elif response_time < 1000:
                performance = 'Fair'
            else:
                performance = 'Slow'
            
            self.results['checks']['response_time'] = {
                'status': 'PASS',
                'response_time_ms': round(response_time, 2),
                'performance': performance
            }
            print(f"  ✓ Response Time: {response_time:.2f}ms ({performance})")
            return True
        except Exception as e:
            self.results['checks']['response_time'] = {
                'status': 'FAIL',
                'message': f'Failed to measure: {str(e)}'
            }
            print(f"  ✗ Failed to measure response time: {e}")
            return False
    
    def check_ssl_certificate(self):
        """Check SSL certificate validity for HTTPS sites"""
        print(f"\n[3/5] Checking SSL certificate...")
        
        if self.parsed_url.scheme != 'https':
            self.results['checks']['ssl'] = {
                'status': 'SKIP',
                'message': 'Not an HTTPS URL'
            }
            print(f"  ⊘ Skipped (not HTTPS)")
            return True
        
        try:
            hostname = self.parsed_url.hostname
            port = self.parsed_url.port or 443
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Check expiration
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (not_after - datetime.utcnow()).days
                    
                    if days_until_expiry < 0:
                        status = 'FAIL'
                        message = f'Certificate expired {abs(days_until_expiry)} days ago'
                        print(f"  ✗ {message}")
                    elif days_until_expiry < 30:
                        status = 'WARN'
                        message = f'Certificate expires in {days_until_expiry} days'
                        print(f"  ⚠ {message}")
                    else:
                        status = 'PASS'
                        message = f'Valid certificate (expires in {days_until_expiry} days)'
                        print(f"  ✓ {message}")
                    
                    self.results['checks']['ssl'] = {
                        'status': status,
                        'days_until_expiry': days_until_expiry,
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'subject': dict(x[0] for x in cert['subject']),
                        'message': message
                    }
                    return status != 'FAIL'
        except Exception as e:
            self.results['checks']['ssl'] = {
                'status': 'FAIL',
                'message': f'SSL check failed: {str(e)}'
            }
            print(f"  ✗ SSL check failed: {e}")
            return False
    
    def check_content(self):
        """Check basic HTML content structure"""
        print(f"\n[4/5] Checking content...")
        try:
            req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0 (Website Checker)'})
            response = urlopen(req, timeout=10)
            content = response.read().decode('utf-8', errors='ignore')
            content_lower = content.lower()
            
            checks = {
                'has_html': '<html' in content_lower,
                'has_head': '<head' in content_lower,
                'has_body': '<body' in content_lower,
                'has_title': '<title' in content_lower,
            }
            
            content_size = len(content)
            
            # All basic HTML elements should be present
            all_passed = all(checks.values())
            
            self.results['checks']['content'] = {
                'status': 'PASS' if all_passed else 'WARN',
                'size_bytes': content_size,
                'has_html_structure': checks['has_html'],
                'has_head_section': checks['has_head'],
                'has_body_section': checks['has_body'],
                'has_title': checks['has_title'],
                'message': 'Content structure looks good' if all_passed else 'Some HTML elements missing'
            }
            
            print(f"  {'✓' if all_passed else '⚠'} Content size: {content_size} bytes")
            print(f"  {'✓' if checks['has_html'] else '✗'} HTML structure: {'Present' if checks['has_html'] else 'Missing'}")
            print(f"  {'✓' if checks['has_title'] else '✗'} Title tag: {'Present' if checks['has_title'] else 'Missing'}")
            
            return True
        except Exception as e:
            self.results['checks']['content'] = {
                'status': 'FAIL',
                'message': f'Content check failed: {str(e)}'
            }
            print(f"  ✗ Content check failed: {e}")
            return False
    
    def check_headers(self):
        """Check HTTP headers for security and best practices"""
        print(f"\n[5/5] Checking HTTP headers...")
        try:
            req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0 (Website Checker)'})
            response = urlopen(req, timeout=10)
            headers = response.headers
            
            security_headers = {
                'X-Content-Type-Options': headers.get('X-Content-Type-Options'),
                'X-Frame-Options': headers.get('X-Frame-Options'),
                'Content-Security-Policy': headers.get('Content-Security-Policy'),
                'Strict-Transport-Security': headers.get('Strict-Transport-Security'),
            }
            
            present_count = sum(1 for v in security_headers.values() if v)
            
            self.results['checks']['headers'] = {
                'status': 'PASS' if present_count >= 2 else 'WARN',
                'content_type': headers.get('Content-Type', 'Not specified'),
                'server': headers.get('Server', 'Not specified'),
                'security_headers': security_headers,
                'security_headers_count': present_count,
                'message': f'{present_count}/4 security headers present'
            }
            
            print(f"  {'✓' if present_count >= 2 else '⚠'} Security headers: {present_count}/4 present")
            print(f"  • Content-Type: {headers.get('Content-Type', 'Not specified')}")
            print(f"  • Server: {headers.get('Server', 'Not specified')}")
            
            return True
        except Exception as e:
            self.results['checks']['headers'] = {
                'status': 'FAIL',
                'message': f'Header check failed: {str(e)}'
            }
            print(f"  ✗ Header check failed: {e}")
            return False
    
    def run_all_checks(self):
        """Run all website checks"""
        print("=" * 60)
        print(f"Website Checker - {self.url}")
        print("=" * 60)
        
        # Run checks
        connectivity_ok = self.check_connectivity()
        
        # Only continue with other checks if connectivity succeeds
        if connectivity_ok:
            self.check_response_time()
            self.check_ssl_certificate()
            self.check_content()
            self.check_headers()
        
        # Print summary
        self.print_summary()
        
        return self.results
    
    def print_summary(self):
        """Print a summary of all checks"""
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        
        total_checks = 0
        passed_checks = 0
        failed_checks = 0
        warnings = 0
        
        for check_name, check_result in self.results['checks'].items():
            status = check_result.get('status', 'UNKNOWN')
            total_checks += 1
            
            if status == 'PASS':
                passed_checks += 1
                symbol = '✓'
            elif status == 'FAIL':
                failed_checks += 1
                symbol = '✗'
            elif status == 'WARN':
                warnings += 1
                symbol = '⚠'
            else:
                symbol = '⊘'
            
            print(f"  {symbol} {check_name.replace('_', ' ').title()}: {status}")
        
        print(f"\nTotal: {total_checks} checks")
        print(f"Passed: {passed_checks} | Failed: {failed_checks} | Warnings: {warnings}")
        
        if failed_checks > 0:
            print("\n❌ OVERALL STATUS: FAILED")
            return False
        elif warnings > 0:
            print("\n⚠ OVERALL STATUS: PASSED WITH WARNINGS")
            return True
        else:
            print("\n✅ OVERALL STATUS: ALL CHECKS PASSED")
            return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python website_checker.py <URL>")
        print("Example: python website_checker.py https://example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Add scheme if not present
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    checker = WebsiteChecker(url)
    results = checker.run_all_checks()
    
    # Exit with appropriate code based on any failures
    failed_checks = sum(1 for check in results['checks'].values() if check.get('status') == 'FAIL')
    if failed_checks > 0:
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
