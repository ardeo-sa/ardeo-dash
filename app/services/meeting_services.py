"""
Service module for fetching and enriching meeting data from the backend API.
"""
from typing import List, Dict
import requests

from app.config import BASE_URL, TIMEOUT, DISABLE_MEETINGS_FETCH

def fetch_meetings() -> List[Dict]:
    """
    Fetch all meetings along with their participants, patients, and notes.

    Returns:
        List[Dict]: List of enriched meetings.
        Empty list if fetching fails
    """

    if DISABLE_MEETINGS_FETCH:
        print("Meeting fetch disabled by env var DISABLE_MEETINGS_FETCH")
        return []

    try:
        meetings_resp = requests.get(f"{BASE_URL}/meetings/", timeout=TIMEOUT)
        meetings_resp.raise_for_status()
        meetings = meetings_resp.json()
    except requests.RequestException as e:
        print(f"Warning: Failed to fetch meetings: {e}")
        return []  # Return empty list instead of raising

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
