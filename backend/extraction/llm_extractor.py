import json
import logging
import time
from datetime import date

import httpx

from config import settings

logger = logging.getLogger(__name__)

MODEL = "llama3.2:3b"
MAX_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 5

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


def _parse_response(data: dict) -> dict:
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


def extract(description: str) -> dict:
    """Return extracted fields for a single listing description. Never raises — returns empty
    dict on failure. Retries on timeout rather than immediately falling back to regex-only
    extraction, since the nightly scrape job has time to spare; still gives up after
    MAX_ATTEMPTS so a genuinely-down Ollama instance can't hang the job forever."""
    if not description or not description.strip():
        return {}

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = httpx.post(
                settings.ollama_url,
                json={"model": MODEL, "prompt": _build_prompt() + description, "format": "json", "stream": False},
                timeout=60.0,
            )
            response.raise_for_status()
            data = json.loads(response.json()["response"])
            return _parse_response(data)
        except httpx.TimeoutException as e:
            logger.warning("llm_extractor timed out (attempt %d/%d): %s", attempt, MAX_ATTEMPTS, e)
            if attempt < MAX_ATTEMPTS:
                time.sleep(RETRY_DELAY_SECONDS)
        except Exception as e:
            logger.warning("llm_extractor failed: %s", e)
            return {}

    logger.error("llm_extractor gave up after %d timeout retries", MAX_ATTEMPTS)
    return {}
