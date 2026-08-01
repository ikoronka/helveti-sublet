<script setup lang="ts">
defineProps<{ source: string }>()
</script>

<template>
  <span
    v-if="source === 'flatfox'"
    class="px-2 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-700"
  >Flatfox</span>
  <span
    v-else
    class="px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-500"
  >{{ source }}</span>
</template>
