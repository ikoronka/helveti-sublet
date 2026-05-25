<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useListingsStore } from '@/stores/listingsStore'
import ListingCard from './ListingCard.vue'

const store = useListingsStore()

onMounted(() => store.fetchListings())

// Returns page numbers and '...' sentinels for the paginator
const pages = computed<(number | '...')[]>(() => {
  const total = store.totalPages
  const cur = store.page
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)

  const near = new Set([1, total, cur - 2, cur - 1, cur, cur + 1, cur + 2].filter(n => n >= 1 && n <= total))
  const sorted = [...near].sort((a, b) => a - b)

  const result: (number | '...')[] = []
  for (let i = 0; i < sorted.length; i++) {
    if (i > 0 && sorted[i]! - sorted[i - 1]! > 1) result.push('...')
    result.push(sorted[i]!)
  }
  return result
})
</script>

<template>
  <div>
    <p v-if="store.loading" class="text-gray-400 text-sm">Loading...</p>
    <p v-else-if="store.error" class="text-red-500 text-sm">{{ store.error }}</p>
    <p v-else-if="store.items.length === 0" class="text-gray-400 text-sm">
      No listings match your filters.
    </p>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
      <ListingCard v-for="listing in store.items" :key="listing.id" :listing="listing" />
    </div>

    <div v-if="store.totalPages > 1" class="flex items-center gap-1 mt-6 justify-center">
      <button
        :disabled="store.page === 1"
        @click="store.setPage(store.page - 1)"
        class="px-3 py-1 rounded text-sm bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-30 disabled:cursor-not-allowed"
      >‹</button>

      <template v-for="p in pages" :key="p">
        <span v-if="p === '...'" class="px-2 text-gray-400 text-sm select-none">…</span>
        <button
          v-else
          @click="store.setPage(p)"
          :class="[
            'px-3 py-1 rounded text-sm',
            p === store.page
              ? 'bg-gray-900 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200',
          ]"
        >{{ p }}</button>
      </template>

      <button
        :disabled="store.page === store.totalPages"
        @click="store.setPage(store.page + 1)"
        class="px-3 py-1 rounded text-sm bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-30 disabled:cursor-not-allowed"
      >›</button>
    </div>
  </div>
</template>
