from datetime import date

SUMMER_WINDOW_START = date(2026, 6, 1)
SUMMER_WINDOW_END = date(2026, 9, 15)
SUMMER_CORE_START = date(2026, 8, 1)
SUMMER_CORE_END = date(2026, 8, 31)


def is_summer_sublet(available_from: date | None, available_to: date | None) -> bool:
    if available_from is None or available_to is None:
        return False
    return (
        SUMMER_WINDOW_START <= available_from <= SUMMER_CORE_START
        and SUMMER_CORE_END <= available_to <= SUMMER_WINDOW_END
    )
