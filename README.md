# 🔐 EntropyLane  
### Secure Messaging Powered by Real-World Traffic Entropy

EntropyLane is a secure messaging system that derives cryptographic keys from
**real-world physical entropy**, specifically traffic motion dynamics, instead
of relying on traditional pseudo-random number generators.

The project demonstrates how **physical micro-variations** such as vehicle
movement, motion jitter, and temporal unpredictability can be transformed into
high-quality entropy and used for practical cryptographic applications.

---

## 🚀 Motivation

Most software systems rely on algorithmic or system-provided randomness, which
can be predictable or vulnerable in constrained environments.

EntropyLane explores an alternative approach:
> **Using physical-world unpredictability as a cryptographic entropy source.**

Traffic scenes provide continuous, non-deterministic motion patterns that are
difficult to predict or reproduce, making them suitable as a real-world entropy
source.

---

## ✨ Key Features

- 🚦 **Traffic-based entropy extraction**
- 📊 **Shannon & Min-Entropy evaluation**
- 🧪 **Bias removal and entropy conditioning**
- 🔐 **AES-256-GCM encrypted messaging**
- ♻️ **One-time entropy consumption (no key reuse)**
- 🛡️ **Replay and tamper resistance**
- 🔍 **Visible cryptographic artifacts (nonce & ciphertext)**
- 🖥️ **Interactive React-based chat UI**

---

## 🧠 System Overview

Traffic Video
↓
Frame Preprocessing
↓
Motion Feature Extraction
↓
Entropy Computation (Sliding Windows)
↓
Entropy Conditioning
↓
Key Derivation (AES-256)
↓
Encrypted Messaging (AES-256-GCM)

---

## 🧰 Tech Stack

### Backend
- Python
- FastAPI
- NumPy, SciPy

### Frontend
- React
- Chart.js

### Cryptography
- AES-256-GCM
- SHA-256 (key derivation)

---

## 📹 Demo Video

A short demo showcasing:
- Traffic-based entropy generation
- Encrypted chat workflow
- Different ciphertext for identical messages
- One-time entropy consumption

---
-----
##▶️ How to Run EntropyLane (Actual Workflow)

EntropyLane consists of three coordinated parts:

Backend (Entropy extraction + crypto engine)

Frontend (Secure chat UI)

Cloudflare Tunnel (External access for demo)
---
##🧩 Prerequisites

Linux / Kali / Ubuntu (recommended)

Python 3.10+

Node.js 18+

npm

A traffic video file (entropy source)
----

##📁 Entropy Source Setup (Mandatory)

⚠️ Traffic video is NOT included in this repository.

This is intentional due to:

Dataset size

Licensing constraints

Cryptographic correctness (entropy sources must not be static or shipped)

Provide your own entropy source:

Obtain any continuous traffic video

Fixed camera

Visible vehicle motion

5–10 minutes recommended

Place it at:

backend/data/video/<your_video>.mp4

🔐 Step 1: Start the Backend (Entropy Engine)

Navigate to the backend directory:

cd backend


Activate the virtual environment:

source venv/bin/activate


Start the API server:

uvicorn api.main:app --host 0.0.0.0 --port 8000

✅ Expected Backend Output
[INIT] Entropy blocks loaded     : 84
[INIT] Entropy per block         : 512 bits
[INIT] NIST SP 800-22 compliance : PASS
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000


This confirms:

Traffic entropy has been successfully extracted

Bias conditioning is complete

Entropy passes NIST SP 800-22

Backend is ready to serve encrypted messaging requests

Backend is powered by FastAPI.

💬 Step 2: Start the Frontend (Chat Interface)

Open a new terminal, then:

cd frontend
npm install
npm run dev


The frontend is built using React.

You will see a local development URL (example):

http://localhost:5173

🌐 Step 3: Enable Cloudflare Tunneling (Demo Access)

For demo and external access, EntropyLane uses Cloudflare Tunnel.

From the project root directory:

cd ..
./start-demo.sh

Open the final URL in the browser or scan the QR code generated.

This script:

Creates a secure Cloudflare tunnel

Exposes backend + frontend externally

Avoids port forwarding or public IP exposure

Tunneling is handled via Cloudflare.

##🔎 What the Demo Shows

Real-time entropy consumption

AES-256-GCM encryption per message

Different ciphertext for identical plaintext

One-time entropy usage (no reuse)

Visible nonce & ciphertext (for demonstration only)
-----
##🔐 Security Design Notes

Each message consumes fresh entropy

No entropy block is ever reused

AES-256-GCM ensures confidentiality + integrity

Raw entropy and secret keys are never exposed

Nonce and ciphertext visibility is strictly for demo transparency

----
## 🔐 Security Design Notes

Each message consumes fresh entropy

No entropy block is reused

AES-256-GCM ensures confidentiality and integrity

Nonce and ciphertext are exposed only for demonstration

Secret keys and raw entropy are never revealed
----
## 📌 Project Status

🚧 Under active development
---
## Future enhancements include:

Live entropy dashboards

Multi-source entropy fusion

Distributed entropy collection

Extended cryptographic evaluation
