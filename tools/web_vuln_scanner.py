"""
Web Vulnerability Scanner
Scans websites for common security flaws including SQL injection, XSS, and misconfigurations
"""

import requests
import re
import urllib.parse
from bs4 import BeautifulSoup # type: ignore
from typing import List, Dict, Any
import time


class WebVulnScanner:
    def __init__(self, target_url: str, timeout: int = 10):
        self.target = target_url if target_url.startswith(('http://', 'https://')) else f'https://{target_url}'
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
        })
        self.findings = []
        self.forms = []
        self.links = []
        
    def scan_all(self) -> Dict[str, Any]:
        """Run all vulnerability checks"""
        print(f"[*] Starting scan of {self.target}")
        
        try:
            # Initial reconnaissance
            self._crawl()
            
            # Run vulnerability tests
            self._check_sql_injection()
            self._check_xss()
            self._check_security_headers()
            self._check_information_disclosure()
            self._check_directory_listing()
            self._check_outdated_software()
            
        except Exception as e:
            self.findings.append({
                'type': 'Error',
                'severity': 'Info',
                'description': f'Scan error: {str(e)}'
            })
        
        return {
            'target': self.target,
            'total_findings': len(self.findings),
            'critical': len([f for f in self.findings if f['severity'] == 'Critical']),
            'high': len([f for f in self.findings if f['severity'] == 'High']),
            'medium': len([f for f in self.findings if f['severity'] == 'Medium']),
            'low': len([f for f in self.findings if f['severity'] == 'Low']),
            'findings': self.findings,
            'forms_found': len(self.forms),
            'links_found': len(self.links)
        }
    
    def _crawl(self):
        """Basic crawling to find forms and links"""
        try:
            response = self.session.get(self.target, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all forms
            self.forms = soup.find_all('form')
            
            # Find all links
            for link in soup.find_all('a', href=True):
                full_url = urllib.parse.urljoin(self.target, link['href'])
                if full_url.startswith(self.target):
                    self.links.append(full_url)
                    
            # Limit links to prevent overload
            self.links = list(set(self.links))[:50]
            
        except Exception as e:
            print(f"[!] Crawl error: {e}")
    
    def _check_sql_injection(self):
        """Test for SQL injection vulnerabilities"""
        sql_payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "1' AND 1=1 --",
            "1' AND 1=2 --",
            "' UNION SELECT NULL--",
            "1'; DROP TABLE users--",
            "1' OR '1'='1' /*",
        ]
        
        sql_errors = [
            "sql syntax",
            "mysql_fetch",
            "pg_query",
            "sqlite_query",
            "ORA-",
            "Microsoft SQL Server",
            "ODBC SQL Server Driver",
            "SQLServer JDBC Driver",
            "PostgreSQL query failed",
            "supplied argument is not a valid MySQL result",
        ]
        
        # Test URL parameters
        parsed = urllib.parse.urlparse(self.target)
        if parsed.query:
            base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            params = urllib.parse.parse_qs(parsed.query)
            
            for param_name in params:
                for payload in sql_payloads[:3]:  # Limit payloads
                    test_params = params.copy()
                    test_params[param_name] = payload
                    test_url = f"{base_url}?{urllib.parse.urlencode(test_params, doseq=True)}"
                    
                    try:
                        response = self.session.get(test_url, timeout=self.timeout)
                        
                        # Check for SQL errors in response
                        for error in sql_errors:
                            if error.lower() in response.text.lower():
                                self.findings.append({
                                    'type': 'SQL Injection',
                                    'severity': 'Critical',
                                    'description': f'Possible SQL injection in parameter "{param_name}"',
                                    'url': test_url,
                                    'payload': payload,
                                    'evidence': f'Database error detected: {error}',
                                    'remediation': 'Use parameterized queries and input validation'
                                })
                                return  # Found it, stop testing
                                
                    except Exception:
                        continue
        
        # Test forms
        for form in self.forms:
            action = form.get('action', '')
            method = form.get('method', 'get').lower()
            form_url = urllib.parse.urljoin(self.target, action)
            
            inputs = form.find_all('input')
            for inp in inputs:
                if inp.get('type') in ['text', 'search', 'url', None]:
                    for payload in sql_payloads[:2]:
                        data = {inp.get('name', 'test'): payload}
                        
                        try:
                            if method == 'post':
                                response = self.session.post(form_url, data=data, timeout=self.timeout)
                            else:
                                response = self.session.get(form_url, params=data, timeout=self.timeout)
                            
                            for error in sql_errors:
                                if error.lower() in response.text.lower():
                                    self.findings.append({
                                        'type': 'SQL Injection',
                                        'severity': 'Critical',
                                        'description': f'Possible SQL injection in form field "{inp.get("name")}"',
                                        'url': form_url,
                                        'payload': payload,
                                        'evidence': f'Database error detected: {error}',
                                        'remediation': 'Use parameterized queries and ORM'
                                    })
                                    return
                        except Exception:
                            continue
    
    def _check_xss(self):
        """Test for Cross-Site Scripting vulnerabilities"""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "\"><script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            "<svg onload=alert('XSS')>",
            "\"><img src=x onerror=alert('XSS')>",
        ]
        
        # Test URL parameters
        parsed = urllib.parse.urlparse(self.target)
        if parsed.query:
            base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            params = urllib.parse.parse_qs(parsed.query)
            
            for param_name in params:
                for payload in xss_payloads[:3]:
                    test_params = params.copy()
                    test_params[param_name] = payload
                    test_url = f"{base_url}?{urllib.parse.urlencode(test_params, doseq=True)}"
                    
                    try:
                        response = self.session.get(test_url, timeout=self.timeout)
                        
                        # Check if payload is reflected without encoding
                        if payload in response.text:
                            self.findings.append({
                                'type': 'Cross-Site Scripting (XSS)',
                                'severity': 'High',
                                'description': f'Reflected XSS in parameter "{param_name}"',
                                'url': test_url,
                                'payload': payload[:50],
                                'evidence': 'Payload reflected in response without proper encoding',
                                'remediation': 'Encode all output, use Content-Security-Policy'
                            })
                            return
                            
                    except Exception:
                        continue
        
        # Test forms for stored XSS potential
        for form in self.forms:
            action = form.get('action', '')
            method = form.get('method', 'get').lower()
            form_url = urllib.parse.urljoin(self.target, action)
            
            inputs = form.find_all('input')
            for inp in inputs:
                if inp.get('type') in ['text', 'search', 'url', 'email', None]:
                    for payload in xss_payloads[:2]:
                        data = {inp.get('name', 'test'): payload}
                        
                        try:
                            if method == 'post':
                                response = self.session.post(form_url, data=data, timeout=self.timeout)
                            else:
                                response = self.session.get(form_url, params=data, timeout=self.timeout)
                            
                            if payload in response.text:
                                self.findings.append({
                                    'type': 'Cross-Site Scripting (XSS)',
                                    'severity': 'High',
                                    'description': f'Possible XSS in form field "{inp.get("name")}"',
                                    'url': form_url,
                                    'payload': payload[:50],
                                    'evidence': 'Payload reflected in response',
                                    'remediation': 'Implement input validation and output encoding'
                                })
                                return
                        except Exception:
                            continue
    
    def _check_security_headers(self):
        """Check for missing security headers"""
        try:
            response = self.session.get(self.target, timeout=self.timeout)
            headers = response.headers
            
            security_headers = {
                'Strict-Transport-Security': {
                    'description': 'HSTS not enabled - site vulnerable to SSL stripping',
                    'severity': 'High'
                },
                'Content-Security-Policy': {
                    'description': 'CSP not implemented - increased XSS risk',
                    'severity': 'Medium'
                },
                'X-Frame-Options': {
                    'description': 'Clickjacking protection missing',
                    'severity': 'Medium'
                },
                'X-Content-Type-Options': {
                    'description': 'MIME sniffing protection missing',
                    'severity': 'Low'
                },
                'X-XSS-Protection': {
                    'description': 'Legacy XSS protection header missing',
                    'severity': 'Low'
                },
                'Referrer-Policy': {
                    'description': 'Referrer policy not set',
                    'severity': 'Low'
                }
            }
            
            for header, info in security_headers.items():
                if header not in headers:
                    self.findings.append({
                        'type': 'Missing Security Header',
                        'severity': info['severity'],
                        'description': info['description'],
                        'header': header,
                        'remediation': f'Add {header} header to server responses'
                    })
            
            # Check for information disclosure in headers
            server = headers.get('Server', '')
            powered = headers.get('X-Powered-By', '')
            
            if server and any(x in server.lower() for x in ['apache', 'nginx', 'iis', 'php']):
                if '/' in server:  # Version number exposed
                    self.findings.append({
                        'type': 'Information Disclosure',
                        'severity': 'Low',
                        'description': f'Server version exposed: {server}',
                        'evidence': f'Server header: {server}',
                        'remediation': 'Configure server to hide version information'
                    })
            
            if powered:
                self.findings.append({
                    'type': 'Information Disclosure',
                    'severity': 'Low',
                    'description': f'Technology stack disclosed: {powered}',
                    'evidence': f'X-Powered-By: {powered}',
                    'remediation': 'Remove X-Powered-By header'
                })
                
        except Exception as e:
            print(f"[!] Header check error: {e}")
    
    def _check_information_disclosure(self):
        """Check for sensitive files and information leakage"""
        common_files = [
            '/robots.txt',
            '/.env',
            '/.git/config',
            '/.htaccess',
            '/web.config',
            '/phpinfo.php',
            '/admin/',
            '/backup/',
            '/config/',
            '/api/',
            '/swagger.json',
            '/openapi.json',
            '/.well-known/security.txt'
        ]
        
        for file_path in common_files:
            try:
                url = urllib.parse.urljoin(self.target, file_path)
                response = self.session.get(url, timeout=self.timeout, allow_redirects=False)
                
                if response.status_code == 200:
                    if file_path == '/.env':
                        self.findings.append({
                            'type': 'Sensitive File Exposure',
                            'severity': 'Critical',
                            'description': 'Environment file publicly accessible',
                            'url': url,
                            'evidence': 'HTTP 200 on /.env',
                            'remediation': 'Block access to .env files in web server config'
                        })
                    elif file_path == '/.git/config':
                        self.findings.append({
                            'type': 'Sensitive File Exposure',
                            'severity': 'Critical',
                            'description': 'Git repository exposed',
                            'url': url,
                            'evidence': 'HTTP 200 on /.git/config',
                            'remediation': 'Block access to .git directory'
                        })
                    elif file_path in ['/robots.txt', '/.well-known/security.txt']:
                        # These are supposed to be public
                        pass
                    else:
                        self.findings.append({
                            'type': 'Sensitive Path Accessible',
                            'severity': 'Medium',
                            'description': f'Potentially sensitive path accessible: {file_path}',
                            'url': url,
                            'remediation': 'Review and restrict access if not intended to be public'
                        })
                        
            except Exception:
                continue
    
    def _check_directory_listing(self):
        """Check for directory listing enabled"""
        test_paths = ['/images/', '/css/', '/js/', '/uploads/', '/files/']
        
        for path in test_paths:
            try:
                url = urllib.parse.urljoin(self.target, path)
                response = self.session.get(url, timeout=self.timeout)
                
                if 'Index of' in response.text or 'Directory Listing' in response.text:
                    self.findings.append({
                        'type': 'Directory Listing',
                        'severity': 'Medium',
                        'description': f'Directory listing enabled on {path}',
                        'url': url,
                        'evidence': 'Directory index page detected',
                        'remediation': 'Disable directory listing in web server configuration'
                    })
                    break
                    
            except Exception:
                continue
    
    def _check_outdated_software(self):
        """Detect outdated software versions"""
        try:
            response = self.session.get(self.target, timeout=self.timeout)
            headers = response.headers
            
            # Check for outdated server versions (simplified check)
            server = headers.get('Server', '')
            
            # This is a basic example - real implementation would check against CVE database
            outdated_signatures = {
                'Apache/2.2': 'Apache 2.2.x is outdated and may have vulnerabilities',
                'Apache/2.4.': 'Check Apache version for known vulnerabilities',
                'PHP/5.': 'PHP 5.x is outdated and unsupported',
                'PHP/7.0': 'PHP 7.0 is outdated',
                'PHP/7.1': 'PHP 7.1 is outdated',
                'PHP/7.2': 'PHP 7.2 is outdated',
            }
            
            for sig, message in outdated_signatures.items():
                if sig in server:
                    self.findings.append({
                        'type': 'Outdated Software',
                        'severity': 'High',
                        'description': message,
                        'evidence': f'Server header: {server}',
                        'remediation': 'Update to latest stable version'
                    })
                    break
                    
        except Exception:
            pass


def main():
    """CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Web Vulnerability Scanner')
    parser.add_argument('url', help='Target URL to scan')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout')
    args = parser.parse_args()
    
    scanner = WebVulnScanner(args.url, args.timeout)
    results = scanner.scan_all()
    
    print(f"\n{'='*60}")
    print(f"SCAN RESULTS FOR: {results['target']}")
    print(f"{'='*60}")
    print(f"Total Findings: {results['total_findings']}")
    print(f"Critical: {results['critical']} | High: {results['high']} | Medium: {results['medium']} | Low: {results['low']}")
    print(f"{'='*60}\n")
    
    for finding in results['findings']:
        print(f"[{finding['severity']}] {finding['type']}")
        print(f"  {finding['description']}")
        if 'url' in finding:
            print(f"  URL: {finding['url']}")
        if 'remediation' in finding:
            print(f"  Fix: {finding['remediation']}")
        print()


if __name__ == '__main__':
    main()