# Contributing

We welcome contributions! To keep things simple and transparent, we use a lightweight CLA gate.

**To contribute:**

1. Open an issue using the **"CLA Signature"** template. Confirm you’ve read and agree to the CLA.
2. Submit your Pull Request. The `cla-check` status must pass before merging.
* CLA text: `CLA/CLA-Individual.md`
* Sign the CLA: https://github.com/ardeo-sa/ardeo-dash/issues/new?template=cla.yml

# eMDT Dash

Management dashboards for enhanced MDT coordination and patient care monitoring in secondary healthcare.
This project aggregates patient and operational data to produce real-time dashboards for clinical teams, analysts, and administrators.

## 📚 Table of Contents

- [Features](#features)
- [Metrics](#metrics)
  - [Patient Flow & Operational Metrics](#patient-flow--operational-metrics)
  - [Treatment Pathway Metrics](#treatment-pathway-metrics)
  - [MDT Coordination Metrics](#mdt-coordination-metrics)
  - [Administrative & Utilization Metrics](#administrative--utilization-metrics)
  - [Coming Soon](#coming-soon)
- [Project Structure](#project-structure)
- [Data Flow Overview](#data-flow-overview)
- [Getting Started](#getting-started)

## Features

* Automated aggregation of key healthcare metrics 
* FastAPI backend for efficient API serving 
* Dash (by Plotly) for interactive, customizable frontend dashboards 
* Dual-database architecture separating raw data and metrics 
* Celery + Redis (optional) for background task scheduling

## Metrics

### Patient Flow & Operational Metrics

* Number of admissions/discharges per day/week/month
* Average Length of Stay (ALOS) per treatment or condition
* Bed occupancy rate 
* Patient wait times:
  * Time from admission to treatment start 
  * Time between referral and MDT review 
* Readmission rates (within 30/60 days)
* Patient no-show / cancellation rate for appointments or MDTs

### Treatment Pathway Metrics

* Pathway adherence rate: Are patients following the recommended pathway steps? 
* Time to treatment milestones:
  * Diagnosis to treatment start 
  * Treatment start to completion 
* Treatment dropout rate 
* Treatment outcomes:
  * Success/failure rates 
  * Complication or relapse rates

### MDT Coordination Metrics

* Number of MDT meetings held 
* Attendance rate (clinicians, specialists, etc.)
* Average time per case discussed 
* Time from referral to MDT discussion 
* Actions assigned vs. completed (follow-up tracking)

### Clinician Performance Metrics

* Patients admitted per clinician
* Average time to treatment start per clinician
* Readmission rate per clinician
* No-show rate per clinician
* Clinician workload:
  * Patients seen per day 
  * Outstanding tasks or follow-ups

### Referral & Source Metrics

* Referrals by source (e.g., GP, self, ED, internal)
* Referral conversion rate: % of referrals resulting in admission
* Referral-to-admission time
* Referral volume trend (by day/week/month)

### Administrative & Utilization Metrics

* Patient-to-clinician ratio
* Resource utilization:
  * Imaging
  * lab tests
  * treatment slots 

### To be added later

#### Patient-Centered Metrics (data not yet available)

* Patient satisfaction scores 
* Patient-reported outcomes (PROMs)
* Patient engagement rate (portal logins, form completions, etc.)

### Predictive or Risk-Based Metrics (Data not available and/or algorithms not developed yet)

* Risk scores (e.g., risk of readmission, deterioration)
* Early warning flags from lab/vital sign trends 
* Forecasted resource demands (beds, staff)

## Project Structure

```text
fastapi_dash_metrics/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # Starts FastAPI app
│   ├── config.py                # Env vars, DB URIs
│   ├── database/
│   │   ├── __init__.py
│   │   ├── primary.py           # Engine/session for source DB
│   │   └── metrics.py           # Engine/session for metrics DB
│   │
│   ├── models/ # ORM models
│   │   ├── __init__.py
│   │   ├── patient.py
│   │   └── appointments.py
│   │   └── mdt.py
│   │   └── metrics.py
│   │   └── metrics.py
│   │   └── metrics.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   └── metrics.py       # FastAPI endpoints
│   │   └── schemas/
│   │       └── metrics.py       # Pydantic validation models
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── aggregations.py      # Data pulling & processing logic
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── worker.py            # Celery setup
│   │   └── metric_tasks.py      # Background metric calculations
│   │
│   └── dash_app/
│       ├── __init__.py
│       ├── dashboard.py         # Dash layout and callbacks
│       └── integration.py       # Mount Dash to FastAPI
│
├── .env                         # Secrets, DB URIs
├── requirements.txt
└── run.py                       # Entry script to run FastAPI + Dash
```

             ┌───────────────────────┐
             │    Source DB (SQL)    │◀──────────┐
             └───────────────────────┘           │
                                                ▼
         ┌──────────────────────┐     ┌──────────────────────────┐
         │ FastAPI (main.py)    │◀────│  API routes (metrics.py) │
         └────────┬─────────────┘     └──────────────────────────┘
                  │
                  ▼
      ┌──────────────────────┐
      │  Aggregation Service │─────┐
      └──────────────────────┘     │
             │                    ▼
     (via Celery or on-demand) ┌───────────────┐
                               │ Metrics DB    │
                               └───────────────┘
                                        │
                                        ▼
                          ┌────────────────────────┐
                          │ Dash App (UI frontend) │
                          └────────────────────────┘

## Getting Started

### Dashboard: Manual Setup
1. Create virtual env and install dependencies

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Configure environment variables
Copy .env.example (if present) to .env and update values as needed (DB connection string, secrets, etc.).

4. Ensure required services are running (e.g., Redis, PostgreSQL)
Start Redis (use instructions below to enable it)

5. Run backend FastAPI app and dashboard
```bash
python run.py
```
6. Run background metrics aggregation
```bash
# Run celery
celery -A app.tasks.worker worker --beat --loglevel=info
```

7. Monitor celery tasks
```bash
# Use flower dashboard to monitor 
# http://localhost:5555
celery -A app.tasks.worker flower --port=5555
```

### To run in prod as service
```bash
# 1. Create dedicated user
sudo useradd -r -s /bin/false dash-runner

2. copy config
sudo cp ardeo-dash.service /etc/systemd/system/

# 3. enable and start
sudo systemctl daemon-reload
sudo systemctl enable ardeo-dash.service
sudo systemctl start ardeo-dash.service

# 3. Check logs
journalctl -u ardeo-dash.service -f 
```

### Docker
```bash
# Run all services
docker compose up -d
```

## Optional setup steps
### Install Redis server
#### Manual Setup (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install Redis
sudo apt install redis-server

# Start Redis
sudo systemctl start redis

# (Optional) Enable Redis to start on boot
sudo systemctl enable redis

# Verify it's running
redis-cli ping
```
#### Run docker
```bash
# Pull the latest lightweight Redis image and starts it on port 6379
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7-alpine
# Verify
docker logs redis
docker exec -it redis redis-cli ping
```

### Install PostgreSQL
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql

# To enable it at boot
sudo systemctl enable postgresql

# Verify
sudo systemctl status postgresql

# Connect to test
sudo -u postgres psql
# Run
\conninfo
# Quit
\q
```

### Databse setup
```bash
# Run once to create database and users
./utils/setup_reporting_db.sh
```

## Maintainance
### Reporting database migrations
```bash
# Generate initial migration
alembic revision --autogenerate -m "init reporting models"

# Generate migrations when models change
alembic revision --autogenerate -m "add new table xyz"

# Apply migrations
alembic upgrade head
```

### Troubleshooting
* Connection Refused errors? Make sure Redis, Postgres, or other services your app depends on are running.
* WireGuard traffic not routing correctly? Avoid using the same LAN subnet as the remote peer (e.g., 192.168.0.0/24).
* Can't SSH to internal IPs via VPN? Ensure your local IP doesn't conflict and the server allows forwarding.

