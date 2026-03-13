# Security Toolkit

A unified web interface for cybersecurity tools. This project combines multiple security utilities into a single platform with both a web UI and REST API.

## Included Tools

| Tool | Category | Description |
|------|----------|-------------|
| Crypto Toolkit | Cryptography | SHA-256 hashing, AES-256-GCM encryption/decryption, RSA-2048 key generation and operations |
| Password Tools | Cryptography | Password strength analysis with zxcvbn, bcrypt hashing and verification |
| Port Scanner | Network | Multi-threaded TCP port scanner with configurable port ranges |
| Secret Scanner | Analysis | Detects API keys, passwords, and sensitive tokens in source code |
| Web Tech Detector | Reconnaissance | Identifies web technologies and frameworks used by websites |
| Repo Scorecard | DevSecOps | Analyzes GitHub repository security practices and compliance |

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/security-toolkit.git
   cd security-toolkit
   start.bat

**Manual Setup**

Backend:
cd api
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

Frontend:
cd frontend
npm install

**Usage**
Running the Application
Development Mode:
# Backend (Port 8000)
cd api
uvicorn main:app --reload

# Frontend (Port 5173)
cd frontend
npm run dev

Access the interface at http://localhost:5173

**API Endpoints**

| Endpoint                 | Method | Description                   |
| ------------------------ | ------ | ----------------------------- |
| `/api/hash`              | POST   | SHA-256 string hashing        |
| `/api/aes/encrypt`       | POST   | AES-256-GCM encryption        |
| `/api/aes/decrypt`       | POST   | AES-256-GCM decryption        |
| `/api/rsa/generate`      | POST   | RSA key pair generation       |
| `/api/rsa/encrypt`       | POST   | RSA public key encryption     |
| `/api/rsa/decrypt`       | POST   | RSA private key decryption    |
| `/api/password/strength` | POST   | Password strength analysis    |
| `/api/password/hash`     | POST   | bcrypt password hashing       |
| `/api/scan/ports`        | POST   | TCP port scanning             |
| `/api/scan/secrets`      | POST   | Secret detection in code      |
| `/api/detect/webtech`    | POST   | Web technology identification |
| `/api/scorecard`         | POST   | GitHub repository analysis    |
| `/api/health`            | GET    | Service health check          |
