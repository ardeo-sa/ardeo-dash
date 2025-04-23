# emdt-dash
Management dashboards for eMDT monitoring


## Project structure
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

