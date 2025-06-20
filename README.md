# 🎧 TrackIQ

**TrackIQ** is an AI-powered audio insight tool designed to help musicians, sync agents, and producers understand the hidden metadata in their tracks — no manual tagging required.

It analyzes `.wav` files to extract high-quality audio features, then presents those features through a clean, modern web interface. This information can help users align their songs with music supervisors’ expectations, pitch better for sync, or organize their catalogs with consistent metadata.

---

## 🧠 Tech Stack

### ⚙️ Backend — FastAPI + Audio Analysis

- **FastAPI** serves a REST API that:
  - Accepts uploaded audio files (`/upload`)
  - Extracts features using signal processing and ML libraries
  - Stores those features in a SQLite database
  - Offers endpoints to list, inspect, and query extracted data

- **Essentia** is a powerful C++/Python library for audio analysis and music information retrieval. In TrackIQ, it provides:
  - **Timbre descriptors**
  - **Spectral complexity**
  - **MFCC (Mel-Frequency Cepstral Coefficients)**
  - **HPCP (key estimation)**
  - **Spectral centroid, flux, crest, rolloff**
  - **Energy, RMS, flatness**

  These features help quantify how a song “feels” sonically — useful for genre classification, mood analysis, and sync tagging.

- **Librosa** is a high-level Python library for music and audio analysis, excellent for:
  - **Tempo (BPM) estimation**
  - **Onset strength (rhythmic activity)**
  - **Chromagram (harmonic features)**
  - **Zero-crossing rate (percussive vs. tonal)**
  - **Harmonic/percussive separation**
  - Complementary feature extraction for cross-validation with Essentia.

- **SQLite** is used to store the extracted metadata locally in `trackiq.db`.

---

### 🎨 Frontend — Next.js (React + TypeScript)

- Built with **Next.js** (React framework) in the `next-frontend/` directory
- Features a simple but extensible UI to:
  - Fetch available analyzed tracks
  - Display extracted audio features interactively
- Clean interface for inspecting how a track’s metadata compares to sync targets

---

## 🔌 API Overview (FastAPI)

All routes run on `http://localhost:8000` when the backend is active.

| Endpoint              | Method | Description                                 |
|-----------------------|--------|---------------------------------------------|
| `/upload/`            | POST   | Upload a `.wav` file and extract features   |
| `/features/`          | GET    | List all audio entries and filenames        |
| `/features/{id}`      | GET    | Get all extracted features for a track      |

API docs are auto-generated at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🚀 Getting Started

### 🔧 Backend Setup

```bash
cd TackIQ
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn trackiq_backend.main:app --reload
