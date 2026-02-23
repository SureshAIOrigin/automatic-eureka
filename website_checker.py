#!/usr/bin/env python3
"""Website checker tool - validates website connectivity and security."""

import sys
import requests
import socket
from urllib.parse import urlparse


def check_http_connectivity(url):
    """Check if website is accessible via HTTP."""
    print(f"Checking HTTP connectivity for {url}...")
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✓ {url} is accessible (Status: {response.status_code})")
            return True
        else:
            print(f"✗ {url} returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Error connecting to {url}: {e}")
        return False


def check_https_connectivity(url):
    """Check if website is accessible via HTTPS."""
    print(f"Checking HTTPS connectivity for {url}...")
    try:
        response = requests.get(url, timeout=5, verify=True)
        if response.status_code == 200:
            print(f"✓ {url} is accessible via HTTPS (Status: {response.status_code})")
            return True
        else:
            print(f"✗ {url} returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Error connecting to {url} via HTTPS: {e}")
        return False


def check_dns_resolution(hostname):
    """Check if hostname resolves to an IP address."""
    print(f"Checking DNS resolution for {hostname}...")
    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"✓ {hostname} resolves to {ip_address}")
        return True
    except socket.gaierror as e:
        print(f"✗ DNS resolution failed for {hostname}: {e}")
        return False


def check_port_open(hostname, port):
    """Check if a specific port is open on the host."""
    print(f"Checking if port {port} is open on {hostname}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((hostname, port))
        sock.close()
        if result == 0:
            print(f"✓ Port {port} is open on {hostname}")
            return True
        else:
            print(f"✗ Port {port} is closed on {hostname}")
            return False
    except socket.error as e:
        print(f"✗ Error checking port {port} on {hostname}: {e}")
        return False


def main():
    """Main function to run website checks."""
    if len(sys.argv) < 2:
        print("Usage: website_checker.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    parsed_url = urlparse(url)
    hostname = parsed_url.netloc or parsed_url.path
    
    print(f"\n=== Website Checker for {url} ===\n")
    
    results = []
    results.append(check_http_connectivity(url))
    results.append(check_https_connectivity(url))
    results.append(check_dns_resolution(hostname))
    results.append(check_port_open(hostname, 80))
    results.append(check_port_open(hostname, 443))
    
    print(f"\n=== Summary ===")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total} checks")
    
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
