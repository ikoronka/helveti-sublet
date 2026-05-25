<script setup lang="ts">
import { useFiltersStore } from '@/stores/filtersStore'

const store = useFiltersStore()
</script>

<template>
  <div class="space-y-2">
    <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Available</h3>
    <div class="space-y-1.5">
      <input
        type="date"
        :value="store.filters.availableFrom ?? ''"
        @input="store.filters.availableFrom = ($event.target as HTMLInputElement).value || null"
        class="w-full border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
      />
      <input
        type="date"
        :value="store.filters.availableTo ?? ''"
        @input="store.filters.availableTo = ($event.target as HTMLInputElement).value || null"
        class="w-full border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
      />
    </div>
  </div>
</template>
