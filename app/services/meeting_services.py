import os
import requests
from typing import List, Dict

BASE_URL = "http://localhost:8000"  # Replace with your actual app URL if different


def fetch_meetings() -> List[Dict]:
    """
    Fetch all meetings along with their participants, patients, and notes.

    Returns:
        List[Dict]: List of enriched meetings.
    """

    # if os.getenv("TESTING") == "1":
    #     return [{"id": "test", "timestamp": "2024-06-01T00:00:00Z", "read": False}]

    try:
        meetings_resp = requests.get(f"{BASE_URL}/meetings/")
        meetings_resp.raise_for_status()
        meetings = meetings_resp.json()
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch meetings: {e}")

    enriched_meetings = []

    for meeting in meetings:
        meeting_id = meeting["id"]
        enriched = dict(meeting)

        try:
            participants_resp = requests.get(f"{BASE_URL}/meetings/{meeting_id}/participants")
            patients_resp = requests.get(f"{BASE_URL}/meetings/{meeting_id}/patients")
            notes_resp = requests.get(f"{BASE_URL}/meetings/{meeting_id}/notes")

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
