import re
from typing import Dict, Optional
from datetime import datetime, timedelta

import dateparser.search

# Keywords that imply a deadline where we should schedule the reminder ahead of time
_DEADLINE_TRIGGERS = [
    "apply before",
    "register before",
    "last date",
    "deadline",
]


def _extract_first_link(text: str) -> str:
    """Return the first URL-looking substring if present."""
    match = re.search(r"(https?://\S+)", text)
    return match.group(1) if match else ""


def _extract_first_datetime(text: str) -> Optional[datetime]:
    """Return the first datetime detected by dateparser (None if not found)."""
    results = dateparser.search.search_dates(
        text,
        settings={"PREFER_DATES_FROM": "future", "RETURN_AS_TIMEZONE_AWARE": False},
    )
    if results:
        # results is a list of (substring, datetime) tuples; take the first
        return results[0][1]
    return None


def _make_title(text: str) -> str:
    """Create a short title from the first line, stripped of URLs and non-alnum noise."""
    first_line = text.strip().splitlines()[0]
    first_line = re.sub(r"https?://\S+", "", first_line)  # remove URLs in title
    first_line = re.sub(r"[^A-Za-z0-9 ]+", " ", first_line)  # non-alnum → space
    return first_line.strip()[:100] or "Reminder"


def parse_message(text: str) -> Dict:
    """Parse a WhatsApp message and return a dict with title, datetime, link, raw."""
    data: Dict = {
        "title": _make_title(text),
        "datetime": None,
        "link": _extract_first_link(text),
        "raw": text,
    }

    dt = _extract_first_datetime(text)
    if dt:
        # If wording suggests a hard deadline, remind 30 minutes earlier
        lowered = text.lower()
        if any(trigger in lowered for trigger in _DEADLINE_TRIGGERS):
            dt -= timedelta(minutes=30)
        data["datetime"] = dt

    return data