from datetime import date
from typing import Optional
import strawberry


@strawberry.type
class ListingType:
    id: str
    source: str
    source_url: str
    title: str
    price_chf: int
    rooms: float
    city: str
    address: Optional[str]
    zip_code: Optional[str]
    kreis: Optional[int]
    area_m2: Optional[int]
    is_furnished: Optional[bool]
    gender_preference: Optional[str]
    is_sublet: bool
    available_from: Optional[date]
    available_to: Optional[date]
    min_stay_days: Optional[int]
    max_stay_days: Optional[int]
    images: str
    is_active: bool


@strawberry.input
class ListingFilterInput:
    price_min: Optional[int] = None
    price_max: Optional[int] = None
    rooms_min: Optional[float] = None
    rooms_max: Optional[float] = None
    city: Optional[str] = None
    in_zurich: Optional[bool] = None
    kreis: Optional[int] = None
    is_furnished: Optional[bool] = None
    gender_preference: Optional[str] = None
    available_from: Optional[date] = None
    available_to: Optional[date] = None
    is_sublet: Optional[bool] = None
    commute_dest_lat: Optional[float] = None
    commute_dest_lng: Optional[float] = None
    commute_mode: Optional[str] = None
    commute_max_minutes: Optional[int] = None


@strawberry.type
class PaginatedListings:
    items: list[ListingType]
    total: int
    page: int
    page_size: int
    total_pages: int


@strawberry.type
class FilterOptions:
    price_min: int
    price_max: int
    rooms_min: float
    rooms_max: float