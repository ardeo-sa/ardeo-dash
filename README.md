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


### Manual Setup
```bash
# 1. (Optional) Generate SSH key for remote access
ssh-keygen -t ed25519 -C "your_email@example.com"
# Then add the public key (~/.ssh/id_ed25519.pub) to your server's ~/.ssh/authorized_keys

# 2. Connect via WireGuard (if required)
# Ensure you're not on the same subnet (192.168.0.0/24) as the remote LAN
# If needed, switch to a different network (e.g. mobile hotspot)

# 3. Clone the repository and enter the project directory
git clone git@github.com:your-org/ardeo-dash.git
cd ardeo-dash

# 4. Create virtual env and install dependencies
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 5. Set up environment variables
cp env.example .env  # Edit DB URIs, secrets

# 6. Ensure required services are running (e.g., Redis, PostgreSQL)
# Start Redis (use instructions above to enable it)
# redis-server (when redis installed from sources)

# Start PostgreSQL (use instructions above to enable it)
# sudo systemctl start postgresql

# 7. Run backend and dashboard
python run.py

# 4. (Optional) Run background metrics aggregation
celery -A app.tasks.worker worker --loglevel=info
```
### Docker
```bash
# Start all services with Docker
docker compose up -d
```

## Troubleshooting
* Connection Refused errors? Make sure Redis, Postgres, or other services your app depends on are running.
* WireGuard traffic not routing correctly? Avoid using the same LAN subnet as the remote peer (e.g., 192.168.0.0/24).
* Can't SSH to internal IPs via VPN? Ensure your local IP doesn't conflict and the server allows forwarding.