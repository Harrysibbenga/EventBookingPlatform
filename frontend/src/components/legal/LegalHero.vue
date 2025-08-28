// src/components/legal/LegalHero.vue
<template>
  <section class="relative bg-gradient-to-br from-primary-600 via-primary-700 to-orange-600 text-white py-20 lg:py-28 overflow-hidden">
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent transform -skew-y-1"></div>
      <div class="absolute top-0 left-0 w-full h-1/3 bg-gradient-radial from-white/10 to-transparent"></div>
    </div>

    <div class="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <!-- Badge -->
      <div class="inline-flex items-center px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-sm font-medium mb-6 border border-white/30">
        <span class="mr-2">⚖️</span>
        Legal Information
      </div>

      <!-- Main Title -->
      <h1 class="text-4xl lg:text-6xl font-bold mb-6 tracking-tight">
        {{ title }}
      </h1>

      <!-- Subtitle -->
      <p class="text-xl lg:text-2xl text-primary-100 mb-8 max-w-2xl mx-auto leading-relaxed">
        {{ subtitle }}
      </p>

      <!-- Effective Date Info -->
      <div class="bg-black/20 backdrop-blur-sm rounded-2xl p-6 max-w-md mx-auto border border-white/20">
        <div class="space-y-2 text-sm text-primary-100">
          <p><strong class="text-white">Effective Date:</strong> {{ effectiveDate }}</p>
          <p><strong class="text-white">Last Updated:</strong> {{ lastUpdated }}</p>
        </div>
      </div>

      <!-- Scroll Indicator -->
      <div class="mt-12">
        <div 
          class="inline-flex items-center text-primary-200 hover:text-white transition-colors duration-200 cursor-pointer"
          @click="scrollToContent"
        >
          <span class="mr-2 text-sm">Read Document</span>
          <ChevronDown class="w-5 h-5 animate-bounce" />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ChevronDown } from 'lucide-vue-next'

defineProps<{
  title: string
  subtitle: string
  effectiveDate: string
  lastUpdated: string
}>()

const scrollToContent = () => {
  const element = document.querySelector('#main-content')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}
</script>