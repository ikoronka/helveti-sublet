# Primary Stadtkreis (1–12) per Zürich city postal code. PLZ boundaries don't
# perfectly align with Kreis boundaries (a few PLZ straddle two Kreise); we map
# each PLZ to its dominant Kreis, which is the convention public PLZ→Kreis
# tables use. A None result means the listing is not in Zürich city.
_ZIP_TO_KREIS: dict[str, int] = {
    "8001": 1,
    "8002": 2,
    "8003": 3,
    "8004": 4,
    "8005": 5,
    "8006": 6,
    "8008": 8,
    "8032": 7,
    "8037": 10,
    "8038": 2,
    "8041": 2,
    "8044": 7,
    "8045": 3,
    "8046": 11,
    "8047": 9,
    "8048": 9,
    "8049": 10,
    "8050": 11,
    "8051": 12,
    "8052": 11,
    "8053": 7,
    "8055": 3,
    "8057": 6,
    "8064": 9,
}

KREISE = list(range(1, 13))


def kreis_from_zip(zip_code: str | None) -> int | None:
    if not zip_code:
        return None
    return _ZIP_TO_KREIS.get(zip_code.strip())
