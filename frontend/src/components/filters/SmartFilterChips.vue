<script setup lang="ts">
import { useFiltersStore } from '@/stores/filtersStore'

const store = useFiltersStore()

function toggleFurnished() {
  store.filters.isFurnished = store.filters.isFurnished === true ? null : true
}

function toggleFemaleOnly() {
  store.filters.genderPreference = store.filters.genderPreference === 'female' ? null : 'female'
}

function toggleSublet() {
  store.filters.isSublet = store.filters.isSublet === true ? null : true
}

function toggleSummerSublet() {
  store.filters.summerSublet = store.filters.summerSublet === true ? null : true
}
</script>

<template>
  <div class="space-y-2">
    <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Features</h3>
    <div class="flex flex-col gap-1.5">
      <button
        @click="toggleFurnished"
        :class="[
          'px-3 py-1 rounded-full text-sm border transition-colors text-left',
          store.filters.isFurnished === true
            ? 'bg-gray-900 text-white border-gray-900'
            : 'bg-white text-gray-600 border-gray-200 hover:border-gray-400',
        ]"
      >
        Furnished
      </button>
      <button
        @click="toggleFemaleOnly"
        :class="[
          'px-3 py-1 rounded-full text-sm border transition-colors text-left',
          store.filters.genderPreference === 'female'
            ? 'bg-gray-900 text-white border-gray-900'
            : 'bg-white text-gray-600 border-gray-200 hover:border-gray-400',
        ]"
      >
        Female only
      </button>
      <button
        @click="toggleSublet"
        :class="[
          'px-3 py-1 rounded-full text-sm border transition-colors text-left',
          store.filters.isSublet === true
            ? 'bg-gray-900 text-white border-gray-900'
            : 'bg-white text-gray-600 border-gray-200 hover:border-gray-400',
        ]"
      >
        Sublet
      </button>
      <button
        @click="toggleSummerSublet"
        :class="[
          'px-3 py-1 rounded-full text-sm border transition-colors text-left',
          store.filters.summerSublet === true
            ? 'bg-gray-900 text-white border-gray-900'
            : 'bg-white text-gray-600 border-gray-200 hover:border-gray-400',
        ]"
      >
        Summer sublet
      </button>
    </div>
  </div>
</template>
