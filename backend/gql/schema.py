from typing import Optional

import strawberry

from gql.resolvers import get_filter_options, get_listings
from types_ import FilterOptions, ListingFilterInput, PaginatedListings


@strawberry.type
class Query:
    listings: PaginatedListings = strawberry.field(resolver=get_listings)
    filter_options: FilterOptions = strawberry.field(resolver=get_filter_options)


schema = strawberry.Schema(query=Query)
