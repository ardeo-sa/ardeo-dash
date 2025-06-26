import random
import csv
import os
from typing import List, Dict
from datetime import date

FIRST_NAMES = ["Alice", "Ben", "Clara", "David", "Emily", "Farah", "George", "Hannah"]
LAST_NAMES = ["Smith", "Jones", "Taylor", "Brown", "Wilson", "Davies", "Evans", "Thomas"]

ROLE_DISTRIBUTION = {
    "Consultant": 0.1,
    "Registrar": 0.15,
    "SHO": 0.15,
    "Nurse": 0.4,
    "Allied Health": 0.1,
    "Admin": 0.1,
}

SPECIALISATIONS = {
    "Oncology": ["Medical Oncology", "Radiation Oncology"],
    "Cardiology": ["Interventional", "Heart Failure"],
    "Emergency": ["Acute", "Trauma"],
    "Surgery": ["General", "Orthopaedics"]
}

NURSE_BANDS = ["Band 5", "Band 6", "Band 7"]
AHP_BANDS = ["Band 6", "Band 7", "Band 8a"]

def generate_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def assign_band(role):
    if role == "Nurse":
        return random.choice(NURSE_BANDS)
    elif role == "Allied Health":
        return random.choice(AHP_BANDS)
    return ""

def assign_seniority(role):
    if role == "Consultant":
        return "Senior"
    elif role == "Registrar":
        return "Mid"
    elif role == "SHO":
        return "Junior"
    elif role in ["Nurse", "Allied Health"]:
        return random.choice(["Junior", "Mid", "Senior"])
    return "Support"

def assign_fte():
    return round(random.choice([0.6, 0.8, 1.0]), 1)

def generate_clinician_registry(departments, clinicians_per_dept=20, output_file="clinician_registry.csv") -> List[Dict]:
    if os.path.exists(output_file):
        # Load from existing file
        with open(output_file) as f:
            reader = csv.DictReader(f)
            return list(reader)

    roster = []
    clinician_id = 1

    for dept in departments:
        specs = SPECIALISATIONS.get(dept, [dept])
        total = clinicians_per_dept

        for role, proportion in ROLE_DISTRIBUTION.items():
            count = int(total * proportion)
            for _ in range(count):
                roster.append({
                    "clinician_id": clinician_id,
                    "full_name": generate_name(),
                    "role": role,
                    "seniority": assign_seniority(role),
                    "department": dept,
                    "specialisation": random.choice(specs),
                    "band": assign_band(role),
                    "fte": assign_fte()
                })
                clinician_id += 1

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=roster[0].keys())
        writer.writeheader()
        writer.writerows(roster)

    return roster


def generate_clinician_daily_metrics(roster: List[Dict]) -> List[Dict]:
    """
    Simulate individual clinician performance for a single day.
    Adds absence status and 0s for performance if absent.
    Returns a list of dicts per clinician with stats like patients seen, tasks, etc.
    """
    daily_data = []

    for c in roster:
        if c["role"] in ["Consultant", "Registrar", "SHO", "Nurse", "Allied Health"]:
            fte = float(c["fte"])
            # Simulate absence: 5% chance per day
            is_absent = random.random() < 0.05

            if is_absent:
                patients_seen = 0
                patients_admitted = 0
                tasks_done = 0
            else:
                patients_seen = max(int(random.gauss(6, 2) * fte), 0)
                tasks_done = max(int(random.gauss(4, 1.5) * fte), 0)
                patients_admitted = max(int(random.gauss(1.5, 0.7) * fte), 0) if c["role"] in ["Consultant",
                                                                                               "Registrar"] else 0
            daily_data.append({
                "date": date_.isoformat(),
                "clinician_id": c["clinician_id"],
                "full_name": c["full_name"],
                "role": c["role"],
                "department": c["department"],
                "specialisation": c["specialisation"],
                "seniority": c["seniority"],
                "band": c["band"],
                "fte": c["fte"],
                "is_absent": is_absent,
                "patients_seen": patients_seen,
                "patients_admitted": patients_admitted,
                "tasks_completed": tasks_done,
            })

    return daily_data
