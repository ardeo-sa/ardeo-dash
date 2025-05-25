## Setup environment 
```bash
python3.12 -m venv venv312
```

## Load virtual environment
```bash
source venv312/bin/activate
```

## To run
```bash
python generate_synthetic_metrics.py --days 90 --beds 120 --csv synthetic_metrics.csv
```