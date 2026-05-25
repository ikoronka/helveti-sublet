<script setup lang="ts">
import type { Listing } from '@/types/listing'
import SourceBadge from './SourceBadge.vue'

const props = defineProps<{ listing: Listing }>()

const images = JSON.parse(props.listing.images) as string[]
</script>

<template>
  <a
    :href="listing.sourceUrl"
    target="_blank"
    rel="noopener noreferrer"
    class="block bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow"
  >
    <div class="bg-gray-100 h-40 flex items-center justify-center text-gray-400 text-sm">
      <img v-if="images[0]" :src="images[0]" class="w-full h-full object-cover" />
      <span v-else>No image</span>
    </div>

    <div class="p-4 space-y-2">
      <div class="flex items-start justify-between gap-2">
        <h3 class="font-semibold text-gray-900 text-sm leading-snug">{{ listing.title }}</h3>
        <span class="text-base font-bold text-gray-900 whitespace-nowrap"
          >CHF {{ listing.priceChf }}</span
        >
      </div>

      <p class="text-xs text-gray-500">
        {{ listing.city }}<span v-if="listing.zipCode"> · {{ listing.zipCode }}</span>
      </p>

      <div class="flex flex-wrap gap-1.5 pt-1">
        <SourceBadge :source="listing.source" />
        <span class="px-2 py-0.5 rounded-full text-xs bg-gray-100 text-gray-600"
          >{{ listing.rooms }} rooms</span
        >
        <span
          v-if="listing.areaM2"
          class="px-2 py-0.5 rounded-full text-xs bg-gray-100 text-gray-600"
          >{{ listing.areaM2 }} m²</span
        >
        <span
          v-if="listing.isFurnished"
          class="px-2 py-0.5 rounded-full text-xs bg-amber-100 text-amber-700"
          >Furnished</span
        >
        <span
          v-if="listing.isSublet"
          class="px-2 py-0.5 rounded-full text-xs bg-blue-100 text-blue-700"
          >Sublet</span
        >
        <span
          v-if="listing.genderPreference === 'female'"
          class="px-2 py-0.5 rounded-full text-xs bg-pink-100 text-pink-700"
          >Female only</span
        >
        <span
          v-if="listing.genderPreference === 'male'"
          class="px-2 py-0.5 rounded-full text-xs bg-indigo-100 text-indigo-700"
          >Male only</span
        >
      </div>
    </div>
  </a>
</template>
