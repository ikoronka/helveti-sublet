import re


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
    return result
