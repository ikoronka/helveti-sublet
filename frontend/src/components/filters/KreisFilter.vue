<script setup lang="ts">
import { computed } from 'vue'
import { useFiltersStore } from '@/stores/filtersStore'

const store = useFiltersStore()

const KREISE = Array.from({ length: 12 }, (_, i) => i + 1)

const inZurich = computed(() => store.filters.inZurich === true)

function toggleInZurich() {
  if (inZurich.value) {
    store.filters.inZurich = null
    store.filters.kreis = null
  } else {
    store.filters.inZurich = true
  }
}

function onKreisChange(event: Event) {
  const value = (event.target as HTMLSelectElement).value
  store.filters.kreis = value ? Number(value) : null
}
</script>

<template>
  <div class="space-y-2">
    <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Location</h3>
    <label class="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
      <input type="checkbox" :checked="inZurich" @change="toggleInZurich" class="rounded" />
      In Zürich
    </label>
    <select
      v-if="inZurich"
      :value="store.filters.kreis ?? ''"
      @change="onKreisChange"
      class="w-full rounded-lg border border-gray-200 bg-white px-3 py-1.5 text-sm text-gray-700 focus:border-gray-400 focus:outline-none"
    >
      <option value="">All Kreise</option>
      <option v-for="k in KREISE" :key="k" :value="k">Kreis {{ k }}</option>
    </select>
  </div>
</template>
