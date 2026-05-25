export interface Listing {
  id: string
  source: string
  sourceUrl: string
  title: string
  priceChf: number
  rooms: number
  city: string
  address: string | null
  zipCode: string | null
  areaM2: number | null
  isFurnished: boolean | null
  genderPreference: string | null
  isSublet: boolean
  availableFrom: string | null
  availableTo: string | null
  minStayDays: number | null
  maxStayDays: number | null
  images: string
  isActive: boolean
}

export interface PaginatedListings {
  items: Listing[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

export interface FilterOptions {
  priceMin: number
  priceMax: number
  roomsMin: number
  roomsMax: number
}

export interface ListingFilters {
  priceMin: number | null
  priceMax: number | null
  roomsMin: number | null
  roomsMax: number | null
  city: string | null
  isFurnished: boolean | null
  genderPreference: string | null
  isSublet: boolean | null
  availableFrom: string | null
  availableTo: string | null
}
