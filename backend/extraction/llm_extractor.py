import json
import logging
from datetime import date

import httpx

from config import settings

logger = logging.getLogger(__name__)

MODEL = "llama3.2:3b"

PROMPT_TEMPLATE = """\
You are extracting structured data from a Swiss apartment/room listing description.
The description may be in German, English, or mixed.

Today's date is {today}.

Return ONLY a valid JSON object with these fields (use null if unknown):
{{
  "gender_preference": "female" | "male" | null,
  "is_furnished": true | false | null,
  "is_sublet": true | false | null,
  "available_from": "YYYY-MM-DD" | null,
  "available_to": "YYYY-MM-DD" | null
}}

Rules:
- gender_preference "female": "Frauen-WG", "nur weiblich", "female only", "suchen eine Mitbewohnerin", "wir sind Frauen", etc.
- gender_preference "male": "Männer-WG", "men only", "suchen einen Mitbewohner", etc.
- is_furnished: true if "möbliert", "furnished", "eingerichtet", "mit Möbeln"; false if "unmöbliert", "ohne Möbel"
- is_sublet: true if "Zwischenmiete", "Untermiete", "sublet", "subletting"
- available_from / available_to: ISO dates parsed from phrases like "ab 1. August", "vom 15.06.2026 bis 10.09.2026", "from August 1 to September 15", "bis Ende August".
- If a month is mentioned without a year, assume the next occurrence of that month relative to today.
- Return null for any field you are not confident about.

Listing description:
"""


def _build_prompt() -> str:
    return PROMPT_TEMPLATE.format(today=date.today().isoformat())


def extract(description: str) -> dict:
    """Return extracted fields for a single listing description. Never raises — returns empty dict on failure."""
    if not description or not description.strip():
        return {}
    try:
        response = httpx.post(
            settings.ollama_url,
            json={"model": MODEL, "prompt": _build_prompt() + description, "format": "json", "stream": False},
            timeout=60.0,
        )
        response.raise_for_status()
        data = json.loads(response.json()["response"])
        result = {}
        if data.get("gender_preference") in ("female", "male"):
            result["gender_preference"] = data["gender_preference"]
        if isinstance(data.get("is_furnished"), bool):
            result["is_furnished"] = data["is_furnished"]
        if isinstance(data.get("is_sublet"), bool):
            result["is_sublet"] = data["is_sublet"]
        for key in ("available_from", "available_to"):
            val = data.get(key)
            if isinstance(val, str):
                try:
                    result[key] = date.fromisoformat(val)
                except ValueError:
                    pass
        return result
    except Exception as e:
        logger.warning("llm_extractor failed: %s", e)
        return {}
