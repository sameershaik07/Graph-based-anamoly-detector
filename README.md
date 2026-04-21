# 🚢 Maritime Watch — Anomaly Detection Platform

> Graph-based multi-dimensional anomaly detection for maritime vessel monitoring.
> **No single parameter can trigger an alert alone.**

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MARITIME WATCH                          │
├─────────────┬───────────────────────┬───────────────────────┤
│  Frontend   │     Flask API         │    ML Pipeline        │
│             │                       │                       │
│  Leaflet.js │  /api/auth/*          │  preprocessor.py      │
│  Chart.js   │  /api/vessels         │  graph_builder.py     │
│  Dashboard  │  /api/anomalies       │  features.py (5 dim)  │
│  Alerts     │  /api/alerts          │  scorer.py            │
│  Upload     │  /api/stats           │  anomaly_engine.py    │
│  Vessel     │  /api/vessel/<id>     │  pipeline.py          │
│  Profile    │  /api/upload          │                       │
├─────────────┴───────────────────────┼───────────────────────┤
│          SQLAlchemy ORM             │   NetworkX Graphs     │
├─────────────────────────────────────┼───────────────────────┤
│     SQLite (default) / MySQL        │   graphs.pkl          │
└─────────────────────────────────────┴───────────────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
cd maritime-watch
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# SQLite is used by default — no database setup needed!
# To use MySQL, edit .env:
cp .env.example .env
```

### 3. Generate Sample Data & Seed Database

```bash
python seed.py
```

This creates:
- Default users: `admin / maritime2024`, `operator / watch2024`
- 20 vessels with positions in the Gulf of Mexico
- Sample CSV at `data/sample_ais_data.csv`

### 4. Run the Server

```bash
python app.py
```

Visit **http://localhost:5000/login** and sign in with `admin / maritime2024`.

### 5. Upload Data

Go to **Upload** → drop `data/sample_ais_data.csv` → click **Upload & Detect Anomalies**.

---

## 5-Dimension Scoring System

The anomaly detection engine scores each vessel across **five independent dimensions**.
A vessel **cannot** be flagged based on a single parameter alone.

| Dimension | Weight | What It Measures | Min Readings |
|-----------|--------|------------------|-------------|
| **Kinematic** | 20% | Speed, acceleration, course changes, zigzag patterns | 3 |
| **Behavioral** | 25% | AIS gaps, loitering, erratic movement, sudden stops | 4 |
| **Contextual** | 20% | Shipping lane deviation, restricted zones, type mismatch | 1 |
| **Graph** | 20% | Network centrality, proximity, rendezvous detection | In graph |
| **Historical** | 15% | Deviation from own speed/course baseline | 20 |

### How Verdicts Work

```
                    Dimension scores
                    ┌─────────────┐
  Kinematic  ────── │  0.82  ████ │ ← above threshold (0.40)
  Behavioral ────── │  0.71  ███  │ ← above threshold
  Contextual ────── │  0.65  ███  │ ← above threshold
  Graph      ────── │  0.12  █    │ ← below threshold
  Historical ────── │  N/A       │ ← no data
                    └─────────────┘
                         │
                    3 of 5 above ─── corroboration bonus +18%
                         │
                    Weighted score + bonus ── 0.72
                         │
                    3 dims ≥ 3 required ── ✅ ALERT
```

### Anti-False-Positive Rules

| Rule | Effect |
|------|--------|
| Single dimension above threshold | **Never** produces ALERT |
| Fewer than 2 dimensions with data | Returns `INSUFFICIENT_DATA` |
| WARNING requires | ≥ 2 dimensions above threshold + score ≥ 0.35 |
| ALERT requires | ≥ 3 dimensions above threshold + score ≥ 0.60 |
| Corroboration bonus | 0% for 0-1 dims, 8% for 2, 18% for 3, 28% for 4, 35% for 5 |

---

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/auth/login` | Login with `{username, password}` |
| `POST` | `/api/auth/logout` | End session |
| `GET` | `/api/auth/me` | Current user info |
| `POST` | `/api/upload` | Upload CSV (multipart form) |
| `GET` | `/api/vessels` | All vessels with latest scores |
| `GET` | `/api/anomalies` | Vessels with score > 0.3 |
| `GET` | `/api/alerts` | Unacknowledged ALERT-level |
| `POST` | `/api/alerts/<id>` | Acknowledge alert |
| `GET` | `/api/stats` | Dashboard summary stats |
| `GET` | `/api/vessel/<id>` | Full vessel profile |
| `POST` | `/api/vessel/<id>/flag` | Flag for review |
| `POST` | `/api/vessel/<id>/safe` | Mark safe |
| `GET` | `/api/sample-csv` | Download sample data |
| `GET` | `/api/export` | Export all results |

### Response Formats

**`GET /api/vessels`**
```json
[{
  "vessel_id": "V013",
  "lat": 24.2,
  "lon": -87.5,
  "speed": 22.3,
  "anomaly_score": 0.78,
  "status": "ALERT",
  "confidence": 0.75,
  "dimensions_available": 3,
  "dimensions_above_threshold": 3
}]
```

**`GET /api/stats`**
```json
{
  "total_vessels": 15,
  "alert_count": 2,
  "warning_count": 3,
  "insufficient_data_count": 0,
  "avg_score": 0.34,
  "last_updated": "2024-06-15T10:00:00"
}
```

---

## Sample CSV Format

```csv
vessel_id,timestamp,lat,lon,speed,course,ship_type
V001,2024-06-15 08:00:00,25.500000,-90.000000,12.3,45.2,tanker
V002,2024-06-15 08:00:00,27.000000,-88.000000,14.1,90.5,cargo
```

| Column | Type | Description |
|--------|------|-------------|
| `vessel_id` | string | Unique vessel identifier |
| `timestamp` | datetime | `YYYY-MM-DD HH:MM:SS` |
| `lat` | float | Latitude (-90 to 90) |
| `lon` | float | Longitude (-180 to 180) |
| `speed` | float | Speed in knots |
| `course` | float | Course in degrees (0-360) |
| `ship_type` | string | tanker, cargo, fishing, passenger, tug, etc. |

---

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

Key test validations:
- ✅ Single-parameter deviation → never ALERT
- ✅ `INSUFFICIENT_DATA` when < 2 dimensions
- ✅ Multi-dimension anomaly → ALERT
- ✅ Score always in [0.0, 1.0]
- ✅ V015 (fast-only) false-positive suppression
- ✅ Full pipeline runs end-to-end

---

## Project Structure

```
maritime-watch/
├── app.py                 # Flask app + all API routes
├── config.py              # Environment config
├── models.py              # SQLAlchemy ORM models
├── pipeline.py            # End-to-end pipeline orchestrator
├── anomaly_engine.py      # Detection orchestrator
├── graph_builder.py       # NetworkX proximity graphs
├── preprocessor.py        # CSV cleaning + sensor fusion
├── features.py            # 5-dimension feature extraction
├── scorer.py              # Multi-dimensional ensemble scorer
├── seed.py                # Database seeding + sample data
├── schema.sql             # SQL schema reference
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── static/
│   ├── css/theme.css      # Maritime ops dark theme
│   └── js/
│       ├── map.js         # Leaflet map + markers
│       ├── alerts.js      # Alert panel
│       ├── stats.js       # Stats + charts
│       └── notifications.js # Toasts + browser notifications
├── templates/
│   ├── login.html         # Login page
│   ├── dashboard.html     # Main dashboard
│   ├── upload.html        # CSV upload
│   └── vessel.html        # Vessel profile
├── tests/
│   ├── test_features.py
│   ├── test_scorer.py
│   ├── test_graph_builder.py
│   ├── test_api.py
│   └── test_pipeline.py
└── data/
    └── sample_ais_data.csv
```

---


