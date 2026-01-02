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

## 📹 Entropy Source Setup (Required to Run)

⚠️ **Traffic video data is NOT included in this repository.**

This is an intentional design decision due to:
- Dataset size
- Licensing constraints
- Cryptographic best practices (entropy sources should not be fixed or shipped)

### How to provide an entropy source:

1. Obtain **any continuous traffic video**:
   - Fixed camera
   - Visible vehicle movement
   - 5–10 minutes recommended

2. Place the video at:
   backend/data/video/<your_video.mp4>
   
3. Start the backend:
cd backend
uvicorn api.main:app --reload
-----

## ▶️ How to Run the Project
Backend
cd backend
source venv/bin/activate
uvicorn api.main:app --reload

Frontend
cd frontend
npm install
npm run dev


Open the browser at the displayed local URL.
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
