<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import LayoutGost from '@/layouts/LayoutGost.vue'
import LayoutAplikacija from '@/layouts/LayoutAplikacija.vue'

const route = useRoute()
const layout = computed(() => route.meta.layout ?? 'gost')
</script>

<template>
  <LayoutGost v-if="layout === 'gost'">
    <RouterView />
  </LayoutGost>
  <LayoutAplikacija v-else>
    <RouterView />
  </LayoutAplikacija>
</template>
