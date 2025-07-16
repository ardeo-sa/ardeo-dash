"""
Service module for fetching and enriching meeting data from the backend API.
"""
from typing import List, Dict
import requests

BASE_URL = "http://localhost:8000"  # Replace with your actual app URL if different
TIMEOUT = 5  # seconds


def fetch_meetings() -> List[Dict]:
    """
    Fetch all meetings along with their participants, patients, and notes.

    Returns:
        List[Dict]: List of enriched meetings.
    """

    # if os.getenv("TESTING") == "1":
    #     return [{"id": "test", "timestamp": "2024-06-01T00:00:00Z", "read": False}]

    try:
        meetings_resp = requests.get(f"{BASE_URL}/meetings/", timeout=TIMEOUT)
        meetings_resp.raise_for_status()
        meetings = meetings_resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch meetings {e}") from e

    enriched_meetings = []

    for meeting in meetings:
        meeting_id = meeting["id"]
        enriched = dict(meeting)

        try:
            participants_resp = requests.get(f"{BASE_URL}/meetings/{meeting_id}/participants", timeout=TIMEOUT)
            patients_resp = requests.get(f"{BASE_URL}/meetings/{meeting_id}/patients", timeout=TIMEOUT)
            notes_resp = requests.get(f"{BASE_URL}/meetings/{meeting_id}/notes", timeout=TIMEOUT)

            if participants_resp.ok:
                enriched["participants"] = participants_resp.json()
            if patients_resp.ok:
                enriched["patients"] = patients_resp.json()
            if notes_resp.ok:
                enriched["notes"] = notes_resp.json()

        except requests.RequestException as e:
            enriched["enrichment_error"] = str(e)

        enriched_meetings.append(enriched)

    return enriched_meetings
