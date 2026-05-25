import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { gqlFetch } from '@/api/client'
import { LISTINGS_QUERY } from '@/api/queries'
import { useFiltersStore } from '@/stores/filtersStore'
import type { Listing, PaginatedListings } from '@/types/listing'

export const useListingsStore = defineStore('listings', () => {
  const filtersStore = useFiltersStore()

  const items = ref<Listing[]>([])
  const total = ref(0)
  const page = ref(1)
  const pageSize = ref(20)
  const totalPages = ref(1)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchListings() {
    loading.value = true
    error.value = null
    try {
      const data = await gqlFetch<{ listings: PaginatedListings }>(LISTINGS_QUERY, {
        filters: filtersStore.toQueryVars(),
        page: page.value,
        pageSize: pageSize.value,
      })
      items.value = data.listings.items
      total.value = data.listings.total
      totalPages.value = data.listings.totalPages
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  function setPage(n: number) {
    page.value = n
    fetchListings()
  }

  watch(
    () => filtersStore.filters,
    () => {
      page.value = 1
      fetchListings()
    },
    { deep: true },
  )

  return { items, total, page, pageSize, totalPages, loading, error, fetchListings, setPage }
})
