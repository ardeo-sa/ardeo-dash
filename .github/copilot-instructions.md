# AI Coding Instructions for Ardeo Dashboard

## Project Overview

**Ardeo Dashboard** is a healthcare metrics aggregation and visualization system for enhanced MDT (multidisciplinary team) coordination and patient care monitoring. It combines a FastAPI backend with a Plotly Dash frontend to produce real-time dashboards from patient and operational data.

### Architecture Overview

```
Primary DB (MySQL)
    ↓
FastAPI (port 8000) + Dash UI
    ├── /api/metrics/* (FastAPI routes)
    └── /dashboard (Dash UI)
    ↓
Metrics DB (PostgreSQL)
    ↓
Celery worker (background tasks) + Redis
```

**Key principle**: Separation of concerns via dual databases:
- **Primary DB**: Raw clinical/operational data (MySQL)
- **Metrics DB**: Pre-computed metrics (PostgreSQL, read-only for Dash)

## Critical Architecture Patterns

### 1. Dual-Database Architecture

The system maintains **two separate databases** to separate transactional data from analytics:

- **Primary DB** (`app/database/primary.py`): Source of truth; contains raw patient, clinical, and operational data (MySQL). Read via `PRIMARY_SESSION_LOCAL`.
- **Metrics DB** (`app/database/metrics.py`): Pre-aggregated metrics; purely for reporting/dashboards (PostgreSQL). Written by aggregator jobs; read by Dash frontend.

**When to use which**: Queries for *raw data extraction* use Primary; *metric calculations* source from Primary and write to Metrics.

### 2. Metrics Aggregation Pipeline

All metrics flow through a **centralized aggregator pattern** in `app/services/metrics/aggregator.py`:

```python
METRIC_SOURCES = {
    "operational": (aggregate_operational_metrics, OperationalMetrics),
    "pathway": (aggregate_pathway_metrics, PathwayMetrics),
    "mdt": (aggregate_mdt_metrics, MDTMetrics),
    # ... other categories
}

def aggregate_all_metrics():
    # Pulls from Primary DB, computes metrics, writes to Metrics DB
    for category, (aggregator, model_cls) in METRIC_SOURCES.items():
        metrics = aggregator(primary_db, date)  # Returns Dict[metric_name, (value, unit)]
```

**Pattern**: Each `aggregate_X_metrics()` function:
- Takes a SQLAlchemy session + optional date
- Returns `Dict[str, Tuple[float, str]]` mapping metric names to (value, unit) tuples
- Logs at INFO level for aggregation tracking

**Adding new metrics**: Create a new module in `app/services/metrics/`, implement `aggregate_*_metrics()`, register in `METRIC_SOURCES`, and bind to appropriate ORM model.

### 3. Callback-Driven Dashboard

Dash dashboards are tab-based with lazy-loaded layouts and callbacks registered in `app/dash_app/callbacks/`:

```python
# In app/dash_app/callbacks/__init__.py:
@app.callback(
    Output('tabs-content', 'children'),
    Input('dropdown-tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return operational_layout()  # Each tab has a separate layout module
```

Each tab has:
- Dedicated `app/dash_app/layouts/*.py` for component tree
- Dedicated `app/dash_app/callbacks/*_callbacks.py` for interactivity
- Shared `data_loader` passed at registration time (switchable between synthetic CSV and real database)

**Important**: Data fetching in callbacks uses `data_loader.get_*()` methods (see `app/dash_app/data_sources.py`).

### 4. Data Source Abstraction

The dashboard supports **real and synthetic data** via environment variable `ARDEO_DATA_SOURCE`:

- **Synthetic** (default): CSV files in `app/dash_app/data/` (for dev/testing)
- **Real**: Direct database queries via `MetricsSessionLocal`

This is managed in `app/dash_app/data_sources.py` through a `DataLoader` factory. When modifying data fetching, ensure both paths are tested.

## Key File Locations & Responsibilities

| Path | Purpose |
|------|---------|
| `app/main.py` | FastAPI app setup, lifespan management, health check |
| `app/config.py` | Environment variables, DB URIs; raises `RuntimeError` if required vars missing |
| `app/database/{primary,metrics}.py` | Engine/session initialization for each DB |
| `app/models/primary/` | ORM models for raw data (not yet well-documented) |
| `app/models/reporting/` | ORM models for metrics tables (Pathway, Operational, MDT, etc.) |
| `app/services/metrics/aggregator.py` | Central hub; routes to category-specific aggregators |
| `app/services/metrics/{pathway,operational,mdt,referral,clinician,admin}.py` | Metric calculation logic |
| `app/services/data_processing/` | ETL pipelines from Primary to Metrics DB |
| `app/api/routes/metrics.py` | FastAPI endpoint to trigger aggregation |
| `app/dash_app/app.py` | Dash factory; instantiates app with data source |
| `app/dash_app/callbacks/` | Tab switching + per-tab callback registration |
| `app/tasks/worker.py` | Celery setup (Redis-backed, optional) |
| `app/tasks/run_metric_aggregation.py` | Celery scheduled task wrapper around `aggregate_all_metrics()` |

## Development Workflows

### Running Locally

```bash
# 1. Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Configure .env (copy from env.example)
cp env.example .env
# Edit .env with local DB credentials

# 3. Start services
redis-server  # In separate terminal (or Docker)
postgres      # Must have metrics DB running

# 4. Run app (FastAPI + Dash)
python run.py  # Starts at http://localhost:8000

# 5. (Optional) Background metrics aggregation
celery -A app.tasks.worker worker --beat --loglevel=info
```

### Testing

- Test setup in `tests/conftest.py`: Uses in-memory SQLite, auto-registers model factories
- Fixtures: `db_session`, `patient`, `clinician`, `referral`, `pathway_progress`, `treatment`
- Run: `pytest tests/` or `pytest tests/models/test_*.py` for specific category

**Important**: Tests auto-mock `TESTING=1` env var and enforce foreign key constraints.

### Database Migrations

```bash
# After modifying models in app/models/reporting/:
alembic revision --autogenerate -m "describe changes"
alembic upgrade head  # Apply in dev/prod
```

### Aggregation Scheduling

- **Manual trigger**: `POST /api/metrics/aggregate` (FastAPI endpoint)
- **Automatic**: Celery beat scheduler (requires Redis + celery worker)
- **Default behavior**: Aggregates for `date.today()` (not historical backfill yet)

## Project-Specific Conventions

### Logging

- All modules use `logger = logging.getLogger(__name__)`
- Level mapping: DEBUG (low-level details), INFO (business events), ERROR (failures with recovery)
- Config in `app/logging_config.py` (JSON logger + file rotation)
- **New code**: Log at INFO level for start/completion of operations, DEBUG for intermediate steps

### Error Handling

- **Database errors**: Catch `SQLAlchemyError`, log and re-raise or return sensible defaults (e.g., `0` for metrics)
- **Missing env vars**: `config.py` raises `RuntimeError` on startup if required vars missing
- **API errors**: Use `HTTPException(status_code=500, detail="...") from e` pattern

### Metrics Data Format

All aggregator functions return:
```python
Dict[str, Tuple[float, str]]  # {metric_name: (value, unit)}
```
Units are strings like `"percent"`, `"days"`, `"count"`, `"ratio"`, `"minutes"`.

### ORM Model Conventions

- Reporting models inherit from `Base` defined in `app/config.py`
- Always include timestamps (created_at, updated_at) where applicable
- Use `nullable=False` + sensible defaults to avoid NULL surprises in queries
- Models are auto-registered on import (done in test `load_models` fixture)

## Integration Points & Dependencies

### External Services

- **Redis**: Optional but required for Celery beat scheduling (production)
- **PostgreSQL**: Metrics DB (required in production; SQLite for testing)
- **MySQL**: Primary DB (healthcare data source; usually external)

### Dependency Highlights

- **FastAPI + Uvicorn**: Web framework + server
- **SQLAlchemy**: ORM for both DBs
- **Dash + Plotly**: Interactive dashboard framework
- **Celery + Flower**: Background task scheduling + monitoring
- **Prometheus**: Metrics export (instrumented via `prometheus-fastapi-instrumentator`)
- **Alembic**: Database migration management

## Common Tasks & Patterns

### Adding a New Metric

1. **Create calculation function** in `app/services/metrics/new_category.py`:
   ```python
   def calculate_metric_X(session: Session) -> float:
       # Query primary DB, compute value
       return value
   ```

2. **Create aggregator** in same file:
   ```python
   def aggregate_new_metrics(session: Session, date_: date = None) -> Dict[str, Tuple]:
       return {
           "metric_x": (calculate_metric_X(session), "unit"),
       }
   ```

3. **Register in aggregator.py**:
   ```python
   METRIC_SOURCES["new"] = (aggregate_new_metrics, NewMetricsModel)
   ```

4. **Create ORM model** in `app/models/reporting/new_category.py`:
   ```python
   class NewMetrics(Base):
       __tablename__ = "new_metrics"
       date = Column(Date)
       metric_name = Column(String)
       value = Column(Float)
   ```

### Switching Data Source (Real vs. Synthetic)

Set `ARDEO_DATA_SOURCE` environment variable:
```bash
ARDEO_DATA_SOURCE=real   # Use PostgreSQL Metrics DB
ARDEO_DATA_SOURCE=synthetic  # Use CSV files (default)
```

The Dash app auto-detects via `app/config.py` and passes to `create_dash_app()`.

### Querying Metrics Data

From Dash callbacks:
```python
def my_callback(data_loader):
    df = data_loader.get_operational_metrics()  # Returns DataFrame
```

From API routes: Query `MetricsSessionLocal` directly and construct response.

## Anti-Patterns to Avoid

1. **Direct DB queries in callbacks**: Use `data_loader` abstraction instead
2. **Hardcoding DB URIs**: Always read from `config.py` / environment
3. **Aggregating metrics for past dates**: Current system only handles today; no backfill mechanism exists yet
4. **Ignoring DISABLE_PRIMARY_DB flag**: If set, primary DB is optional (for Dash-only mode)
5. **Returning non-Dict from aggregators**: Always return `Dict[str, Tuple[float, str]]`
6. **Skipping unit annotations**: Every metric must have a unit for consistent UI rendering

## Testing Approach

- Use provided fixtures (db_session, patient, clinician, etc.) to avoid repetitive setup
- SQLite in-memory DB auto-created for each test session
- Foreign key constraints enforced; use fixtures to create related records properly
- Avoid mocking database layers; test via real (in-memory) SQL
- For integration tests: Use `mock_env_vars` to override DB URIs

---

**Last updated**: December 2024  
For questions on architecture, check README.md or explore `app/main.py` lifespan context manager.
