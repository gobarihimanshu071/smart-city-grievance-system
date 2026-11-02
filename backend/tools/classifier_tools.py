
import re


def normalize_complaint(text: str) -> str:
    """Clean complaint text before classification."""

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Complaint cannot be empty.")

    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)

    return text


def classify_category(text: str) -> str:
    """Identify the grievance category using keywords."""

    normalized = normalize_complaint(text)

    keywords = {
        "water": [
            "water leakage",
            "water leak",
            "water supply",
            "water shortage",
            "pipe burst",
            "drinking water",
            "water"
        ],
        "roads": [
            "pothole",
            "road damage",
            "broken road",
            "road repair",
            "damaged road",
            "road"
        ],
        "electricity": [
            "power cut",
            "electricity",
            "streetlight",
            "electric pole",
            "power outage",
            "transformer"
        ],
        "sanitation": [
            "garbage",
            "waste",
            "drainage",
            "sewage",
            "dirty street",
            "sanitation",
            "overflowing drain"
        ]
    }

    for category, terms in keywords.items():
        if any(term in normalized for term in terms):
            return category

    return "unknown"


def extract_location(text: str) -> str | None:
    """Extract a location introduced by near, in, or at."""

    patterns = [
        r"\bnear\s+(.+?)(?:[,.!?]|$)",
        r"\bin\s+(.+?)(?:[,.!?]|$)",
        r"\bat\s+(.+?)(?:[,.!?]|$)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip().title()

    return None
