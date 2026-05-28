import math
from typing import Optional

import strawberry
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from types_ import FilterOptions, ListingFilterInput, ListingType, PaginatedListings
from models import Listing

async def get_listings(
    info: strawberry.types.Info,
    filters: Optional[ListingFilterInput] = None,
    page: int = 1,
    page_size: int = 20,
) -> PaginatedListings:
    db: AsyncSession = info.context["db"]

    query = select(Listing).where(Listing.is_active == True)

    if filters:
        if filters.price_min is not None:
            query = query.where(Listing.price_chf >= filters.price_min)
        if filters.price_max is not None:
            query = query.where(Listing.price_chf <= filters.price_max)
        if filters.rooms_min is not None:
            query = query.where(Listing.rooms >= filters.rooms_min)
        if filters.rooms_max is not None:
            query = query.where(Listing.rooms <= filters.rooms_max)
        if filters.city is not None:
            query = query.where(Listing.city == filters.city)
        if filters.is_furnished is not None:
            query = query.where(Listing.is_furnished == filters.is_furnished)
        if filters.gender_preference is not None:
            query = query.where(Listing.gender_preference == filters.gender_preference)
        if filters.is_sublet is not None:
            query = query.where(Listing.is_sublet == filters.is_sublet)
        if filters.summer_sublet is True:
            query = query.where(Listing.is_summer_sublet.is_(True))
        if filters.available_from is not None:
            query = query.where(Listing.available_from >= filters.available_from)
        if filters.available_to is not None:
            query = query.where(Listing.available_to <= filters.available_to)

    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar_one()

    offset = (page - 1) * page_size
    result = await db.execute(query.order_by(Listing.first_seen.desc()).offset(offset).limit(page_size))
    listings = result.scalars().all()

    return PaginatedListings(
        items=[_to_listing_type(l) for l in listings],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total > 0 else 1,
    )


async def get_filter_options(info: strawberry.types.Info) -> FilterOptions:
    db: AsyncSession = info.context["db"]

    result = await db.execute(
        select(
            func.min(Listing.price_chf),
            func.max(Listing.price_chf),
            func.min(Listing.rooms),
            func.max(Listing.rooms),
        ).where(Listing.is_active == True)
    )
    row = result.one()

    return FilterOptions(
        price_min=row[0] or 0,
        price_max=row[1] or 10000,
        rooms_min=row[2] or 1.0,
        rooms_max=row[3] or 5.0,
    )


def _to_listing_type(l: Listing) -> ListingType:
    return ListingType(
        id=l.id,
        source=l.source,
        source_url=l.source_url,
        title=l.title,
        price_chf=l.price_chf,
        rooms=l.rooms,
        city=l.city,
        address=l.address,
        zip_code=l.zip_code,
        area_m2=l.area_m2,
        is_furnished=l.is_furnished,
        gender_preference=l.gender_preference,
        is_sublet=l.is_sublet,
        is_summer_sublet=l.is_summer_sublet,
        available_from=l.available_from,
        available_to=l.available_to,
        min_stay_days=l.min_stay_days,
        max_stay_days=l.max_stay_days,
        images=l.images,
        is_active=l.is_active,
    )