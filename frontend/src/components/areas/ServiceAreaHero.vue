// src/components/areas/ServiceAreaHero.vue
<template>
  <section class="relative bg-gradient-to-br from-primary-600 via-primary-700 to-orange-600 text-white py-20 lg:py-32 overflow-hidden">
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent transform -skew-y-1"></div>
      <div class="absolute top-0 left-0 w-full h-1/3 bg-gradient-radial from-white/10 to-transparent"></div>
    </div>

    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <!-- Badge -->
        <div class="inline-flex items-center px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-sm font-medium mb-6 border border-white/30">
          <MapPin class="w-4 h-4 mr-2" />
          {{ totalCoverage }} Coverage
        </div>

        <!-- Main Title -->
        <h1 class="text-4xl lg:text-6xl font-bold mb-6 tracking-tight">
          {{ title }}
        </h1>

        <!-- Subtitle -->
        <p class="text-xl lg:text-2xl text-primary-100 mb-8 max-w-3xl mx-auto leading-relaxed">
          {{ subtitle }}
        </p>

        <!-- Primary Area Highlight -->
        <div class="inline-flex items-center px-6 py-3 bg-white/15 backdrop-blur-sm rounded-full border border-white/20">
          <Star class="w-5 h-5 text-yellow-300 mr-2" />
          <span class="text-white font-medium">Based in {{ primaryArea }} • Free Local Delivery</span>
        </div>
      </div>

      <!-- Service Areas Overview -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 max-w-4xl mx-auto">
        <div 
          v-for="(area, index) in areas" 
          :key="area"
          class="text-center p-4 bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 hover:bg-white/15 transition-all duration-200"
          :style="{ animationDelay: `${index * 100}ms` }"
        >
          <div class="text-2xl mb-2">
            {{ getAreaIcon(area) }}
          </div>
          <div class="text-sm font-medium text-white">
            {{ area }}
          </div>
        </div>
      </div>

      <!-- Key Stats -->
      <div class="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto text-center">
        <div class="p-6 bg-black/20 backdrop-blur-sm rounded-xl border border-white/20">
          <div class="text-3xl font-bold text-white mb-2">FREE</div>
          <div class="text-primary-200">Delivery in Milton Keynes</div>
        </div>
        <div class="p-6 bg-black/20 backdrop-blur-sm rounded-xl border border-white/20">
          <div class="text-3xl font-bold text-white mb-2">50+</div>
          <div class="text-primary-200">Towns & Villages</div>
        </div>
        <div class="p-6 bg-black/20 backdrop-blur-sm rounded-xl border border-white/20">
          <div class="text-3xl font-bold text-white mb-2">24HR</div>
          <div class="text-primary-200">Hire Period</div>
        </div>
      </div>

      <!-- Scroll Indicator -->
      <div class="mt-12 text-center">
        <button 
          @click="scrollToContent"
          class="inline-flex flex-col items-center text-primary-200 hover:text-white transition-colors duration-200"
        >
          <span class="text-sm mb-2">Explore Coverage Areas</span>
          <ChevronDown class="w-6 h-6 animate-bounce" />
        </button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ChevronDown, MapPin, Star } from 'lucide-vue-next'

defineProps<{
  title: string
  subtitle: string
  areas: string[]
  primaryArea: string
  totalCoverage: string
}>()

const getAreaIcon = (area: string) => {
  const icons: Record<string, string> = {
    'Milton Keynes': '🏢',
    'Buckinghamshire': '🌳',
    'Bedfordshire': '🏰',
    'Northamptonshire': '⚡',
    'Oxfordshire': '🎓',
    'Hertfordshire': '🌹'
  }
  return icons[area] || '📍'
}

const scrollToContent = () => {
  const element = document.querySelector('#coverage-map, .py-16')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}
</script>