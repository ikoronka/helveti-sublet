<script setup lang="ts">
import { useFiltersStore } from '@/stores/filtersStore'
import ListingGrid from '@/components/listings/ListingGrid.vue'
import PriceRangeSlider from '@/components/filters/PriceRangeSlider.vue'
import RoomSelector from '@/components/filters/RoomSelector.vue'
import KreisFilter from '@/components/filters/KreisFilter.vue'
import SmartFilterChips from '@/components/filters/SmartFilterChips.vue'
import DateRangePicker from '@/components/filters/DateRangePicker.vue'

const filtersStore = useFiltersStore()
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white border-b border-gray-100 px-6 py-4 flex items-center justify-between">
      <h1 class="text-xl font-bold text-gray-900">HelvétiSublet</h1>
      <a
        href="https://github.com/ikoronka/helveti-sublet"
        target="_blank"
        rel="noopener noreferrer"
        aria-label="View source on GitHub"
        class="text-gray-400 hover:text-gray-900 transition-colors"
      >
        <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true">
          <path
            d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.207 11.387.6.113.793-.26.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.84 1.237 1.84 1.237 1.07 1.834 2.807 1.304 3.492.997.108-.775.42-1.305.763-1.605-2.665-.303-5.467-1.333-5.467-5.93 0-1.31.469-2.381 1.236-3.221-.124-.303-.536-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.29-1.552 3.297-1.23 3.297-1.23.655 1.652.243 2.873.12 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.48 5.921.43.372.823 1.102.823 2.222v3.293c0 .32.192.694.801.576C20.566 21.797 24 17.298 24 12c0-6.63-5.37-12-12-12"
          />
        </svg>
      </a>
    </header>

    <div class="max-w-7xl mx-auto px-4 py-6 flex gap-6">
      <aside class="w-64 shrink-0 space-y-6">
        <PriceRangeSlider />
        <RoomSelector />
        <KreisFilter />
        <SmartFilterChips />
        <DateRangePicker />
        <button
          @click="filtersStore.reset()"
          class="text-xs text-gray-400 hover:text-gray-600 underline"
        >
          Reset filters
        </button>
      </aside>

      <main class="flex-1">
        <ListingGrid />
      </main>
    </div>
  </div>
</template>
