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
    <header class="bg-white border-b border-gray-100 px-6 py-4">
      <h1 class="text-xl font-bold text-gray-900">HelvétiSublet</h1>
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
