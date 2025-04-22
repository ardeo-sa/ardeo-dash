# emdt-dash
Management dashboards for eMDT monitoring

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

### Administrative & Utilization Metrics
* Patient-to-clinician ratio 
* Clinician workload metrics (patients seen per day, tasks pending)
* Resource utilization:
  * Imaging, lab tests, treatment slots 
  * Referral source breakdown (e.g., primary care, ED, internal transfer)

### To be added in the next phase 
#### Patient-Centered Metrics (data not yet available)
* Patient satisfaction scores 
* Patient-reported outcomes (PROMs)
* Patient engagement rate (portal logins, form completions, etc.)

### Predictive or Risk-Based Metrics (Data not available and/or algorithms not developed yet)
* Risk scores (e.g., risk of readmission, deterioration)
* Early warning flags from lab/vital sign trends 
* Forecasted resource demands (beds, staff)

## Project structure

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
│   ├── models/
│   │   ├── __init__.py
│   │   ├── patient.py           # ORM models from primary DB
│   │   └── metrics.py           # ORM models for metrics
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

