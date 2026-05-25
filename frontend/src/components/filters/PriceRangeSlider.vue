<script setup lang="ts">
import { useFiltersStore } from '@/stores/filtersStore'

const store = useFiltersStore()
</script>

<template>
  <div class="space-y-2">
    <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Price (CHF/mo)</h3>
    <div class="flex gap-2 items-center">
      <input
        type="number"
        placeholder="Min"
        :value="store.filters.priceMin ?? ''"
        @input="store.filters.priceMin = ($event.target as HTMLInputElement).valueAsNumber || null"
        class="w-full border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
      />
      <span class="text-gray-400 text-sm">–</span>
      <input
        type="number"
        placeholder="Max"
        :value="store.filters.priceMax ?? ''"
        @input="store.filters.priceMax = ($event.target as HTMLInputElement).valueAsNumber || null"
        class="w-full border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
      />
    </div>
  </div>
</template>
