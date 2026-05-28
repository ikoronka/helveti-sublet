import calendar
import re
from datetime import date


def extract_gender_preference(text: str) -> str | None:
    t = text.lower()
    female = [
        r"frauen.?wg", r"nur (für )?frauen", r"nur weiblich", r"female only",
        r"only female", r"suchen (eine|eine neue) mitbewohnerin",
        r"wir sind (alles |nur )?frauen", r"reine frauen", r"mädels.?wg",
        r"wg von frauen", r"frauenwohnung",
    ]
    male = [
        r"männer.?wg", r"nur (für )?männer", r"nur männlich", r"men only",
        r"only men", r"suchen (einen|einen neuen) mitbewohner(?!in)",
        r"wir sind (alles |nur )?männer", r"reine männer",
    ]
    if any(re.search(p, t) for p in female):
        return "female"
    if any(re.search(p, t) for p in male):
        return "male"
    return None


def extract_is_furnished(text: str) -> bool | None:
    t = text.lower()
    furnished = [r"\bmöbliert\b", r"\bfurnished\b", r"\beingerichtet\b", r"mit möbeln"]
    unfurnished = [r"\bunmöbliert\b", r"\bunfurnished\b", r"ohne möbel"]
    if any(re.search(p, t) for p in furnished):
        return True
    if any(re.search(p, t) for p in unfurnished):
        return False
    return None


def extract_is_sublet(text: str) -> bool | None:
    t = text.lower()
    patterns = [r"\bzwischenmiete\b", r"\buntermiete\b", r"\bsublet\b", r"\bsubletting\b"]
    if any(re.search(p, t) for p in patterns):
        return True
    return None


MONTHS = {
    "jan": 1, "januar": 1, "january": 1,
    "feb": 2, "februar": 2, "february": 2,
    "mär": 3, "maerz": 3, "märz": 3, "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "mai": 5, "may": 5,
    "jun": 6, "juni": 6, "june": 6,
    "jul": 7, "juli": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "okt": 10, "oktober": 10, "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dez": 12, "dezember": 12, "dec": 12, "december": 12,
}
_MONTH_RE = "|".join(sorted(MONTHS.keys(), key=len, reverse=True))


def _resolve_year(month: int, day: int) -> int:
    today = date.today()
    candidate = date(today.year, month, day)
    return today.year if candidate >= today else today.year + 1


def _two_digit_year(yy: int) -> int:
    return 2000 + yy if yy < 70 else 1900 + yy


def _safe_date(year: int, month: int, day: int) -> date | None:
    try:
        return date(year, month, day)
    except ValueError:
        return None


def _parse_numeric_dmy(s: str) -> date | None:
    m = re.match(r"(\d{1,2})\.(\d{1,2})\.?(\d{2,4})?", s)
    if not m:
        return None
    day, month = int(m.group(1)), int(m.group(2))
    if not (1 <= month <= 12 and 1 <= day <= 31):
        return None
    if m.group(3):
        y = int(m.group(3))
        year = _two_digit_year(y) if y < 100 else y
    else:
        year = _resolve_year(month, day)
    return _safe_date(year, month, day)


def _parse_month_name(day_part: str | None, month_word: str, year_part: str | None, end_of_month: bool = False) -> date | None:
    month = MONTHS.get(month_word.lower())
    if not month:
        return None
    if end_of_month:
        day = calendar.monthrange(2026, month)[1]  # year doesn't matter for non-Feb
    elif day_part:
        day = int(day_part)
    else:
        day = 1
    if year_part:
        y = int(year_part)
        year = _two_digit_year(y) if y < 100 else y
    else:
        year = _resolve_year(month, day)
    if month == 2:
        day = min(day, calendar.monthrange(year, month)[1])
    return _safe_date(year, month, day)


_FROM_PREFIX = r"(?:ab|from|available\s+from|verfügbar\s+ab|frei\s+ab|bezugsbereit\s+ab|vom)"
_TO_PREFIX = r"(?:bis|until|to|bis\s+zum|until\s+the|–|-)"
_RANGE_SEP = r"\s*(?:bis|until|to|-|–|—)\s*"


def _find_range(text: str) -> tuple[date | None, date | None]:
    # numeric range: 01.08.2026 - 31.08.2026 (year optional on either side)
    m = re.search(
        r"(\d{1,2}\.\d{1,2}\.?(?:\d{2,4})?)" + _RANGE_SEP + r"(\d{1,2}\.\d{1,2}\.?(?:\d{2,4})?)",
        text,
    )
    if m:
        return _parse_numeric_dmy(m.group(1)), _parse_numeric_dmy(m.group(2))
    # month-name range: 1. August - 15. September (2026)?
    m = re.search(
        rf"(?:(\d{{1,2}})\.?\s*)?({_MONTH_RE})(?:\s+(\d{{2,4}}))?" + _RANGE_SEP +
        rf"(?:(\d{{1,2}})\.?\s*)?({_MONTH_RE})(?:\s+(\d{{2,4}}))?",
        text,
    )
    if m:
        start = _parse_month_name(m.group(1), m.group(2), m.group(3) or m.group(6))
        end = _parse_month_name(m.group(4), m.group(5), m.group(6))
        return start, end
    return None, None


def _find_from(text: str) -> date | None:
    # ab 01.08.2026 / ab 1.8.26 / from 01.08.2026
    m = re.search(_FROM_PREFIX + r"\s+(\d{1,2}\.\d{1,2}\.?(?:\d{2,4})?)", text)
    if m:
        return _parse_numeric_dmy(m.group(1))
    # ab 1. August (2026)? / from 1 August / from August 1
    m = re.search(
        _FROM_PREFIX + rf"\s+(?:(\d{{1,2}})\.?\s+)?({_MONTH_RE})(?:\s+(\d{{1,2}}))?(?:\s+(\d{{2,4}}))?",
        text,
    )
    if m:
        day_part = m.group(1) or m.group(3)
        return _parse_month_name(day_part, m.group(2), m.group(4))
    return None


def _find_to(text: str) -> date | None:
    # bis Ende August / until end of August
    m = re.search(rf"(?:bis\s+ende|until\s+end\s+of|end\s+of)\s+({_MONTH_RE})(?:\s+(\d{{2,4}}))?", text)
    if m:
        return _parse_month_name(None, m.group(1), m.group(2), end_of_month=True)
    # bis 31.08.2026
    m = re.search(r"(?:bis|until|to)\s+(\d{1,2}\.\d{1,2}\.?(?:\d{2,4})?)", text)
    if m:
        return _parse_numeric_dmy(m.group(1))
    # bis 15. September (2026)? / until September 15
    m = re.search(
        rf"(?:bis|until|to)\s+(?:(\d{{1,2}})\.?\s+)?({_MONTH_RE})(?:\s+(\d{{1,2}}))?(?:\s+(\d{{2,4}}))?",
        text,
    )
    if m:
        day_part = m.group(1) or m.group(3)
        return _parse_month_name(day_part, m.group(2), m.group(4))
    return None


def extract_available_from(text: str) -> date | None:
    t = text.lower()
    start, _ = _find_range(t)
    return start or _find_from(t)


def extract_available_to(text: str) -> date | None:
    t = text.lower()
    _, end = _find_range(t)
    return end or _find_to(t)


def extract_all(description: str) -> dict:
    result = {}
    gp = extract_gender_preference(description)
    if gp is not None:
        result["gender_preference"] = gp
    furn = extract_is_furnished(description)
    if furn is not None:
        result["is_furnished"] = furn
    sublet = extract_is_sublet(description)
    if sublet is not None:
        result["is_sublet"] = sublet
    af = extract_available_from(description)
    if af is not None:
        result["available_from"] = af
    at = extract_available_to(description)
    if at is not None:
        result["available_to"] = at
    return result
