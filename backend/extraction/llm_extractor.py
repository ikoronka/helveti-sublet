import json
import logging

import httpx

from config import settings

logger = logging.getLogger(__name__)

MODEL = "llama3.2:3b"

PROMPT = """\
You are extracting structured data from a Swiss apartment/room listing description.
The description may be in German, English, or mixed.

Return ONLY a valid JSON object with these fields (use null if unknown):
{
  "gender_preference": "female" | "male" | null,
  "is_furnished": true | false | null,
  "is_sublet": true | false | null
}

Rules:
- gender_preference "female": "Frauen-WG", "nur weiblich", "female only", "suchen eine Mitbewohnerin", "wir sind Frauen", etc.
- gender_preference "male": "Männer-WG", "men only", "suchen einen Mitbewohner", etc.
- is_furnished: true if "möbliert", "furnished", "eingerichtet", "mit Möbeln"; false if "unmöbliert", "ohne Möbel"
- is_sublet: true if "Zwischenmiete", "Untermiete", "sublet", "subletting"
- Return null for any field you are not confident about.

Listing description:
"""


def extract(description: str) -> dict:
    """Return extracted fields for a single listing description. Never raises — returns empty dict on failure."""
    if not description or not description.strip():
        return {}
    try:
        response = httpx.post(
            settings.ollama_url,
            json={"model": MODEL, "prompt": PROMPT + description, "format": "json", "stream": False},
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
        return result
    except Exception as e:
        logger.warning("llm_extractor failed: %s", e)
        return {}
