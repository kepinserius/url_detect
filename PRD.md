# Product Requirements Document (PRD) - Phishing URL Detector

## 1. Tujuan Utama
Deteksi phishing URL berbasis ML yang open-source, bisa self-host, dan API-first.

## 2. Fitur Utama
- **Static Analysis**: Ekstraksi fitur tanpa mengunjungi URL (aman).
- **REST API v1**: Endpoint `/v1/check` untuk prediksi.
- **Self-hosted**: Support Docker Compose.
- **Multiple Models**: Mendukung XGBoost, Random Forest, dll.

## 3. Komponen Teknis
- **Language**: Python 3.9+
- **Framework API**: FastAPI
- **ML Libraries**: Scikit-learn, XGBoost, Pandas
- **Dataset**: PhiUSIIL Phishing URL Dataset

## 4. Keamanan & Privasi
- Tidak ada auto-fetch URL.
- Redaksi data sensitif di log.
- API versioning (v1).

## 5. Roadmap
- **Phase 1**: Research & Model (v0.x)
- **Phase 2**: Engine & API (v0.x)
- **Phase 3**: Release & SDK (v1.0+)
