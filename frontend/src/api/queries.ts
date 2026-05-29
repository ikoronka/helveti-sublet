export const LISTINGS_QUERY = `
  query Listings($filters: ListingFilterInput, $page: Int, $pageSize: Int) {
    listings(filters: $filters, page: $page, pageSize: $pageSize) {
      total
      page
      pageSize
      totalPages
      items {
        id
        source
        sourceUrl
        title
        priceChf
        rooms
        city
        address
        zipCode
        kreis
        areaM2
        isFurnished
        genderPreference
        isSublet
        isSummerSublet
        availableFrom
        availableTo
        minStayDays
        maxStayDays
        images
        isActive
      }
    }
  }
`

export const FILTER_OPTIONS_QUERY = `
  query FilterOptions {
    filterOptions {
      priceMin
      priceMax
      roomsMin
      roomsMax
    }
  }
`
