<script setup lang="ts">
import { useFiltersStore } from '@/stores/filtersStore'

const store = useFiltersStore()
const options = [1, 1.5, 2, 2.5, 3, 3.5, 4]

function toggle(value: number) {
  if (store.filters.roomsMin === value && store.filters.roomsMax === value) {
    store.filters.roomsMin = null
    store.filters.roomsMax = null
  } else {
    store.filters.roomsMin = value
    store.filters.roomsMax = value
  }
}

function isActive(value: number) {
  return store.filters.roomsMin === value && store.filters.roomsMax === value
}
</script>

<template>
  <div class="space-y-2">
    <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Rooms</h3>
    <div class="flex flex-wrap gap-1.5">
      <button
        v-for="n in options"
        :key="n"
        @click="toggle(n)"
        :class="[
          'px-3 py-1 rounded-full text-sm border transition-colors',
          isActive(n)
            ? 'bg-gray-900 text-white border-gray-900'
            : 'bg-white text-gray-600 border-gray-200 hover:border-gray-400',
        ]"
      >
        {{ n }}
      </button>
    </div>
  </div>
</template>
