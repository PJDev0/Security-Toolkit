"""
Security Toolkit API
Wraps existing Python tools with FastAPI endpoints
"""

import os
import sys
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import socket
import concurrent.futures

# Add tools directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))

app = FastAPI(title="Security Toolkit API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ Request Models ============

class TextInput(BaseModel):
    text: str


class PasswordInput(BaseModel):
    password: str


class TargetInput(BaseModel):
    target: str
    ports: str = "1-100"


class URLInput(BaseModel):
    url: str


class RepoInput(BaseModel):
    owner: str
    repo: str


class EncryptInput(BaseModel):
    plaintext: str
    key: str = None


class DecryptInput(BaseModel):
    ciphertext: str
    key: str


# ============ CRYPTOGRAPHY ENDPOINTS ============

@app.post("/api/hash")
async def hash_text(data: TextInput):
    """
    Generate SHA-256 hash of input text
    Uses: tools/hasher.py logic
    """
    import hashlib
    
    result = hashlib.sha256(data.text.encode()).hexdigest()
    
    return {
        "algorithm": "SHA-256",
        "hash": result,
        "length": len(result)
    }


@app.post("/api/aes/encrypt")
async def aes_encrypt(data: EncryptInput):
    """
    Encrypt text with AES-256-GCM
    Uses: tools/symmetric_crypto.py logic
    """
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    import base64
    import os
    
    # Generate key if not provided
    if data.key:
        key = bytes.fromhex(data.key)
    else:
        key = AESGCM.generate_key(bit_length=256)
    
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data.plaintext.encode(), None)
    encrypted = base64.b64encode(nonce + ciphertext).decode()
    
    return {
        "ciphertext": encrypted,
        "key": key.hex() if not data.key else None,
        "algorithm": "AES-256-GCM"
    }


@app.post("/api/aes/decrypt")
async def aes_decrypt(data: DecryptInput):
    """
    Decrypt AES-256-GCM encrypted text
    Uses: tools/symmetric_crypto.py logic
    """
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    import base64
    
    try:
        key = bytes.fromhex(data.key)
        aesgcm = AESGCM(key)
        
        encrypted_data = base64.b64decode(data.ciphertext)
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        return {
            "plaintext": plaintext.decode(),
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Decryption failed: {str(e)}")


@app.post("/api/rsa/generate")
async def rsa_generate():
    """
    Generate RSA-2048 key pair
    Uses: tools/asymmetric_crypto.py logic
    """
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()
    
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    
    return {
        "private_key": private_pem,
        "public_key": public_pem,
        "key_size": 2048
    }


@app.post("/api/rsa/encrypt")
async def rsa_encrypt(message: str = Form(...), public_key: str = Form(...)):
    """
    Encrypt message with RSA public key
    Uses: tools/asymmetric_crypto.py logic
    """
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import serialization, hashes
    import base64
    
    try:
        pub_key = serialization.load_pem_public_key(public_key.encode())
        
        encrypted = pub_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return {
            "ciphertext": base64.b64encode(encrypted).decode()
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/rsa/decrypt")
async def rsa_decrypt(ciphertext: str = Form(...), private_key: str = Form(...)):
    """
    Decrypt message with RSA private key
    Uses: tools/asymmetric_crypto.py logic
    """
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import serialization, hashes
    import base64
    
    try:
        priv_key = serialization.load_pem_private_key(
            private_key.encode(),
            password=None
        )
        
        decrypted = priv_key.decrypt(
            base64.b64decode(ciphertext),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return {
            "plaintext": decrypted.decode()
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/password/strength")
async def password_strength(data: PasswordInput):
    """
    Analyze password strength using zxcvbn
    Uses: tools/password_security.py logic
    """
    from zxcvbn import zxcvbn
    
    result = zxcvbn(data.password)
    score = result['score']
    
    strength_labels = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Strong",
        4: "Very Strong"
    }
    
    return {
        "score": score,
        "strength": strength_labels[score],
        "crack_time": result['crack_times_display']['offline_slow_hashing_1e4_per_second'],
        "warning": result['feedback']['warning'],
        "suggestions": result['feedback']['suggestions']
    }


@app.post("/api/password/hash")
async def password_hash(data: PasswordInput):
    """
    Hash password using bcrypt
    Uses: tools/password_security.py logic
    """
    import bcrypt
    
    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt(rounds=12))
    
    return {
        "hash": hashed.decode(),
        "algorithm": "bcrypt",
        "rounds": 12
    }


@app.post("/api/password/verify")
async def password_verify(password: str = Form(...), hash: str = Form(...)):
    """
    Verify password against bcrypt hash
    Uses: tools/password_security.py logic
    """
    import bcrypt
    
    match = bcrypt.checkpw(password.encode(), hash.encode())
    
    return {
        "match": match,
        "valid": match
    }


# ============ NETWORK ENDPOINTS ============

@app.post("/api/scan/ports")
async def port_scan(data: TargetInput):
    """
    Scan ports on target host
    Uses: tools/scanner.py logic
    EDUCATIONAL USE ONLY - Requires explicit permission
    """
    
    # Safety limit: max 100 ports
    if "-" in data.ports:
        start, end = map(int, data.ports.split("-"))
        ports = list(range(start, min(end + 1, start + 100)))
    else:
        ports = [int(p) for p in data.ports.split(",")[:100]]
    
    if len(ports) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 ports allowed")
    
    def scan_single_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((data.target, port))
            sock.close()
            
            if result == 0:
                return {"port": port, "status": "open"}
            return None
        except:
            return None
    
    # Multi-threaded scanning
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(scan_single_port, ports))
    
    open_ports = [r for r in results if r]
    
    return {
        "target": data.target,
        "ports_scanned": len(ports),
        "open_ports": open_ports,
        "open_count": len(open_ports),
        "warning": "Only scan systems you own or have explicit permission to test"
    }


# ============ ANALYSIS ENDPOINTS ============

@app.post("/api/scan/secrets")
async def scan_secrets(data: TextInput):
    """
    Scan code for secrets and API keys
    Uses: tools/secret_scanner.py logic
    """
    import re
    
    patterns = [
        (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API Key"),
        (r'AKIA[0-9A-Z]{16}', "AWS Access Key ID"),
        (r'ghp_[0-9a-zA-Z]{36}', "GitHub Personal Access Token"),
        (r'(?i)password\s*=\s*["\'][^"\']{6,}["\']', "Password Assignment"),
        (r'(?i)api[_-]?key\s*[:=]\s*["\'][^"\']{10,}["\']', "API Key Assignment"),
        (r'sk_live_[0-9a-zA-Z]{24,}', "Stripe Live Key"),
    ]
    
    findings = []
    lines = data.text.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        for pattern, label in patterns:
            if re.search(pattern, line):
                findings.append({
                    "line": line_num,
                    "type": label,
                    "content": line.strip()[:100]
                })
    
    risk_level = "High" if len(findings) > 5 else "Medium" if len(findings) > 0 else "Low"
    
    return {
        "total_found": len(findings),
        "risk_level": risk_level,
        "findings": findings
    }


@app.post("/api/detect/webtech")
async def detect_webtech(data: URLInput):
    """
    Detect technologies used by website
    Uses: tools/web_tech_detector.py logic
    """
    import requests
    from bs4 import BeautifulSoup
    
    # Ensure URL has protocol
    if not data.url.startswith(("http://", "https://")):
        url = "https://" + data.url
    else:
        url = data.url
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        technologies = []
        html_lower = response.text.lower()
        
        # Check for common technologies
        tech_signatures = {
            "React": ["react", "reactjs", "__next", "next.js"],
            "Vue.js": ["vue", "vuejs", "vue.min.js"],
            "Angular": ["angular", "ng-app", "angularjs"],
            "jQuery": ["jquery"],
            "Bootstrap": ["bootstrap", "bootstrap.min.css"],
            "WordPress": ["/wp-content/", "wp-includes", "wordpress"],
            "Django": ["django", "csrfmiddlewaretoken"],
            "Flask": ["flask", "werkzeug"],
            "Next.js": ["__next", "_next/static"],
            "Laravel": ["laravel", "csrf-token"],
            "Ruby on Rails": ["rails", "csrf-param"],
        }
        
        for tech, signatures in tech_signatures.items():
            if any(sig in html_lower for sig in signatures):
                technologies.append(tech)
        
        # Check headers
        server = response.headers.get('Server', '')
        powered_by = response.headers.get('X-Powered-By', '')
        
        return {
            "url": url,
            "technologies": technologies,
            "detected_count": len(technologies),
            "server": server,
            "powered_by": powered_by
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")


# ============ SCORECARD ENDPOINTS ============

@app.post("/api/scorecard")
async def repo_scorecard(data: RepoInput):
    """
    Analyze GitHub repository security
    Uses: tools/scorecard.py logic
    """
    
    token = os.environ.get("GITHUB_TOKEN")
    
    # Demo mode if no token
    if not token:
        return {
            "demo_mode": True,
            "repository": f"{data.owner}/{data.repo}",
            "score": 65,
            "max_score": 100,
            "grade": "C",
            "checks": {
                "has_license": True,
                "has_readme": True,
                "has_security_md": False,
                "has_codeowners": False,
                "branch_protection": False,
                "requires_pr_reviews": False,
                "signed_commits": False
            },
            "note": "Set GITHUB_TOKEN environment variable for live analysis"
        }
    
    try:
        from github import Github
        
        g = Github(token)
        repo = g.get_repo(f"{data.owner}/{data.repo}")
        
        # Run checks
        checks = {}
        
        # Check for license
        try:
            repo.get_license()
            checks["has_license"] = True
        except:
            checks["has_license"] = False
        
        # Check for README
        try:
            repo.get_contents("README.md")
            checks["has_readme"] = True
        except:
            checks["has_readme"] = False
        
        # Check for SECURITY.md
        security_paths = ["SECURITY.md", ".github/SECURITY.md", "docs/SECURITY.md"]
        checks["has_security_md"] = any(
            _file_exists(repo, path) for path in security_paths
        )
        
        # Check for CODEOWNERS
        codeowner_paths = ["CODEOWNERS", ".github/CODEOWNERS", "docs/CODEOWNERS"]
        checks["has_codeowners"] = any(
            _file_exists(repo, path) for path in codeowner_paths
        )
        
        # Check branch protection (requires admin access, often fails)
        checks["branch_protection"] = False
        checks["requires_pr_reviews"] = False
        checks["signed_commits"] = False
        
        try:
            branch = repo.get_branch("main")
            protection = branch.get_protection()
            checks["branch_protection"] = True
            checks["requires_pr_reviews"] = protection.required_pull_request_reviews is not None
        except:
            try:
                branch = repo.get_branch("master")
                protection = branch.get_protection()
                checks["branch_protection"] = True
            except:
                pass
        
        # Calculate score
        weights = {
            "has_license": 15,
            "has_codeowners": 20,
            "has_readme": 10,
            "has_security_md": 15,
            "branch_protection": 25,
            "requires_pr_reviews": 10,
            "signed_commits": 5
        }
        
        score = sum(weights.get(check, 0) for check, passed in checks.items() if passed)
        max_score = sum(weights.values())
        percentage = round((score / max_score) * 100)
        
        # Determine grade
        if percentage >= 90:
            grade = "A"
        elif percentage >= 75:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 40:
            grade = "D"
        else:
            grade = "F"
        
        return {
            "repository": f"{data.owner}/{data.repo}",
            "score": score,
            "max_score": max_score,
            "percentage": percentage,
            "grade": grade,
            "checks": checks
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def _file_exists(repo, path):
    """Helper to check if file exists in repo"""
    try:
        repo.get_contents(path)
        return True
    except:
        return False
# Add this import at the top with other imports
from typing import Optional
import threading
import queue

# ============ PACKET ANALYZER ENDPOINTS ============

class PacketCaptureRequest(BaseModel):
    interface: Optional[str] = None
    duration: int = 30  # seconds
    packet_count: int = 100
    detect_scans: bool = True

class PacketCaptureResponse(BaseModel):
    packets: list
    total_captured: int
    syn_alerts: int
    http_requests: int
    duration: float

# Global storage for packet capture (in production, use Redis or database)
packet_storage = {
    "capturing": False,
    "packets": [],
    "start_time": None,
    "interface": None
}

@app.post("/api/network/capture")
async def start_packet_capture(request: PacketCaptureRequest):
    """
    Start packet capture on specified interface
    Requires admin/root privileges
    """
    import time
    from scapy.all import sniff, IP, TCP, UDP, Raw
    from scapy.layers.http import HTTPRequest
    
    # Check if already capturing
    if packet_storage["capturing"]:
        raise HTTPException(status_code=409, detail="Capture already in progress")
    
    packet_storage["capturing"] = True
    packet_storage["packets"] = []
    packet_storage["start_time"] = time.time()
    packet_storage["interface"] = request.interface
    
    syn_counter = {}
    syn_threshold = 10
    alerts = []
    
    def packet_handler(packet):
        if not packet.haslayer(IP):
            return
            
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        
        packet_info = {
            "timestamp": time.time(),
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "protocol": "OTHER",
            "src_port": None,
            "dst_port": None,
            "flags": None,
            "payload_preview": None,
            "http_request": None,
            "alert": None
        }
        
        # TCP handling
        if packet.haslayer(TCP):
            sport = packet[TCP].sport
            dport = packet[TCP].dport
            flags = str(packet[TCP].flags)
            
            packet_info["protocol"] = "TCP"
            packet_info["src_port"] = sport
            packet_info["dst_port"] = dport
            packet_info["flags"] = flags
            
            # SYN scan detection
            if request.detect_scans and flags == "S":
                syn_counter[src_ip] = syn_counter.get(src_ip, 0) + 1
                if syn_counter[src_ip] == syn_threshold:
                    alert = f"Potential SYN scan from {src_ip}"
                    alerts.append(alert)
                    packet_info["alert"] = alert
            
            # HTTP detection
            if packet.haslayer(HTTPRequest):
                try:
                    host = packet[HTTPRequest].Host.decode('utf-8', errors='ignore')
                    path = packet[HTTPRequest].Path.decode('utf-8', errors='ignore')
                    method = packet[HTTPRequest].Method.decode('utf-8', errors='ignore')
                    packet_info["http_request"] = f"{method} {host}{path}"
                except:
                    pass
            
            # Payload preview
            if packet.haslayer(Raw):
                try:
                    payload = packet[Raw].load.decode('utf-8', errors='ignore')[:100]
                    packet_info["payload_preview"] = payload
                except:
                    packet_info["payload_preview"] = str(packet[Raw].load[:50])
        
        # UDP handling
        elif packet.haslayer(UDP):
            packet_info["protocol"] = "UDP"
            packet_info["src_port"] = packet[UDP].sport
            packet_info["dst_port"] = packet[UDP].dport
        
        packet_storage["packets"].append(packet_info)
        
        # Stop if we have enough packets
        if len(packet_storage["packets"]) >= request.packet_count:
            return False  # Stop sniffing
    
    def capture_thread():
        try:
            sniff(
                iface=request.interface,
                prn=packet_handler,
                store=False,
                timeout=request.duration,
                stop_filter=lambda x: len(packet_storage["packets"]) >= request.packet_count
            )
        except Exception as e:
            packet_storage["error"] = str(e)
        finally:
            packet_storage["capturing"] = False
    
    # Start capture in background thread
    thread = threading.Thread(target=capture_thread)
    thread.start()
    
    return {
        "status": "started",
        "interface": request.interface or "default",
        "duration": request.duration,
        "max_packets": request.packet_count,
        "message": "Capture started. Use /api/network/capture/status to check progress."
    }

@app.get("/api/network/capture/status")
async def get_capture_status():
    """Get current capture status and results"""
    return {
        "capturing": packet_storage["capturing"],
        "interface": packet_storage["interface"],
        "packets_captured": len(packet_storage["packets"]),
        "elapsed_time": packet_storage["start_time"] and (time.time() - packet_storage["start_time"]),
        "packets": packet_storage["packets"][-50:]  # Return last 50 packets
    }

@app.post("/api/network/capture/stop")
async def stop_capture():
    """Stop active packet capture"""
    packet_storage["capturing"] = False
    return {
        "status": "stopped",
        "total_packets": len(packet_storage["packets"]),
        "packets": packet_storage["packets"]
    }

# ============ WEB VULNERABILITY SCANNER ENDPOINTS ============

class VulnScanRequest(BaseModel):
    url: str
    timeout: Optional[int] = 10

@app.post("/api/scan/vulnerabilities")
async def scan_vulnerabilities(request: VulnScanRequest):
    """
    Scan website for vulnerabilities
    SQL Injection, XSS, Security Headers, Information Disclosure
    """
    try:
        from web_vuln_scanner import WebVulnScanner
        
        scanner = WebVulnScanner(request.url, request.timeout)
        results = scanner.scan_all()
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

@app.get("/api/scan/vulnerabilities/signature")
async def get_vulnerability_signatures():
    """Get list of vulnerabilities this scanner can detect"""
    return {
        "vulnerabilities": [
            {
                "type": "SQL Injection",
                "severity": "Critical",
                "description": "Database injection through user input",
                "tests": ["Error-based detection", "Union-based detection"]
            },
            {
                "type": "Cross-Site Scripting (XSS)",
                "severity": "High", 
                "description": "JavaScript injection in web pages",
                "tests": ["Reflected XSS detection"]
            },
            {
                "type": "Missing Security Headers",
                "severity": "Medium",
                "description": "HSTS, CSP, X-Frame-Options, etc.",
                "tests": ["Header analysis"]
            },
            {
                "type": "Information Disclosure",
                "severity": "Medium",
                "description": "Sensitive files and version information exposed",
                "tests": ["Common file detection", "Header analysis"]
            },
            {
                "type": "Directory Listing",
                "severity": "Low",
                "description": "Directory indexing enabled",
                "tests": ["Path enumeration"]
            },
            {
                "type": "Outdated Software",
                "severity": "High",
                "description": "Known vulnerable software versions",
                "tests": ["Version fingerprinting"]
            }
        ]
    }

# ============ HEALTH CHECK ============

@app.get("/api/health")
def health_check():
    """API health check endpoint"""
    return {
        "status": "operational",
        "version": "1.0.0",
        "tools_available": [
            "hash", "aes_encrypt", "aes_decrypt", "rsa_generate", 
            "rsa_encrypt", "rsa_decrypt", "password_strength", 
            "password_hash", "password_verify", "port_scan",
            "secret_scan", "webtech_detect", "repo_scorecard"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)