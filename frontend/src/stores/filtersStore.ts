import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ListingFilters } from '@/types/listing'

export const useFiltersStore = defineStore('filters', () => {
  const filters = ref<ListingFilters>({
    priceMin: null,
    priceMax: null,
    roomsMin: null,
    roomsMax: null,
    city: null,
    inZurich: null,
    kreis: null,
    isFurnished: null,
    genderPreference: null,
    isSublet: null,
    summerSublet: null,
    availableFrom: null,
    availableTo: null,
  })

  function reset() {
    filters.value = {
      priceMin: null,
      priceMax: null,
      roomsMin: null,
      roomsMax: null,
      city: null,
      inZurich: null,
      kreis: null,
      isFurnished: null,
      genderPreference: null,
      isSublet: null,
      summerSublet: null,
      availableFrom: null,
      availableTo: null,
    }
  }

  function toQueryVars() {
    const f = filters.value
    return {
      priceMin: f.priceMin ?? undefined,
      priceMax: f.priceMax ?? undefined,
      roomsMin: f.roomsMin ?? undefined,
      roomsMax: f.roomsMax ?? undefined,
      city: f.city ?? undefined,
      inZurich: f.inZurich ?? undefined,
      kreis: f.kreis ?? undefined,
      isFurnished: f.isFurnished ?? undefined,
      genderPreference: f.genderPreference ?? undefined,
      isSublet: f.isSublet ?? undefined,
      summerSublet: f.summerSublet ?? undefined,
      availableFrom: f.availableFrom ?? undefined,
      availableTo: f.availableTo ?? undefined,
    }
  }

  return { filters, reset, toQueryVars }
})
