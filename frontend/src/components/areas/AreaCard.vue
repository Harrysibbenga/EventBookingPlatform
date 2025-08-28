// src/components/areas/AreaCard.vue
<template>
  <div 
    :class="[
      'bg-white rounded-2xl border-2 transition-all duration-300 hover:shadow-lg hover:-translate-y-1',
      isPrimary ? 'border-primary-200 hover:border-primary-300' : 'border-neutral-200 hover:border-neutral-300'
    ]"
  >
    <!-- Card Header -->
    <div :class="[
      'p-6 rounded-t-2xl',
      isPrimary ? 'bg-gradient-to-r from-primary-50 to-orange-50' : 'bg-neutral-50'
    ]">
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center">
          <div :class="[
            'w-12 h-12 rounded-full flex items-center justify-center text-2xl mr-4',
            isPrimary ? 'bg-primary-100' : 'bg-neutral-100'
          ]">
            {{ area.icon }}
          </div>
          <div>
            <h3 class="text-xl font-bold text-neutral-900">{{ area.name }}</h3>
            <p class="text-sm text-neutral-600">{{ area.county }}</p>
          </div>
        </div>
        <div v-if="isPrimary" class="bg-primary-500 text-white px-3 py-1 rounded-full text-xs font-medium">
          PRIMARY
        </div>
      </div>
      
      <p class="text-neutral-700 text-sm leading-relaxed">{{ area.description }}</p>
    </div>

    <!-- Card Content -->
    <div class="p-6">
      <!-- Key Details -->
      <div class="grid grid-cols-2 gap-4 mb-6">
        <div class="text-center p-3 bg-neutral-50 rounded-lg">
          <div class="text-lg font-bold text-neutral-900">
            {{ area.deliveryFee === 0 ? 'FREE' : `£${area.deliveryFee}` }}
          </div>
          <div class="text-xs text-neutral-600">Delivery Fee</div>
        </div>
        <div class="text-center p-3 bg-neutral-50 rounded-lg">
          <div class="text-lg font-bold text-neutral-900">{{ area.setupTime }}</div>
          <div class="text-xs text-neutral-600">Setup Time</div>
        </div>
      </div>

      <!-- Highlights -->
      <div class="mb-6">
        <h4 class="font-semibold text-neutral-900 mb-3 text-sm">Service Highlights</h4>
        <div class="grid grid-cols-2 gap-2">
          <div 
            v-for="highlight in area.highlights" 
            :key="highlight"
            class="flex items-center text-xs text-neutral-600"
          >
            <CheckCircle class="w-3 h-3 text-green-500 mr-2 flex-shrink-0" />
            {{ highlight }}
          </div>
        </div>
      </div>

      <!-- Areas/Postcodes -->
      <div v-if="area.areas || area.postcodes">
        <h4 class="font-semibold text-neutral-900 mb-3 text-sm">Coverage Areas</h4>
        <div class="flex flex-wrap gap-1">
          <span 
            v-for="location in (area.areas || area.postcodes?.slice(0, 6))" 
            :key="location"
            class="px-2 py-1 bg-neutral-100 text-neutral-700 text-xs rounded"
          >
            {{ location }}
          </span>
          <span 
            v-if="area.postcodes && area.postcodes.length > 6"
            class="px-2 py-1 bg-primary-100 text-primary-700 text-xs rounded font-medium"
          >
            +{{ area.postcodes.length - 6 }} more
          </span>
        </div>
      </div>

      <!-- Popular Venues -->
      <div class="mt-6">
        <h4 class="font-semibold text-neutral-900 mb-3 text-sm">Popular Venues</h4>
        <div class="space-y-2">
          <div 
            v-for="venue in area.popularVenues.slice(0, 3)" 
            :key="venue"
            class="flex items-center text-xs text-neutral-600"
          >
            <div class="w-2 h-2 bg-primary-400 rounded-full mr-2 flex-shrink-0"></div>
            {{ venue }}
          </div>
        </div>
      </div>
    </div>

    <!-- Card Footer -->
    <div class="px-6 pb-6">
      <button class="w-full py-2 px-4 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors duration-200 text-sm">
        View {{ area.name }} Details
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { CheckCircle } from 'lucide-vue-next'

interface ServiceArea {
  id: string
  name: string
  county: string
  icon: string
  isPrimary: boolean
  deliveryFee: number
  setupTime: string
  coverage: string
  description: string
  highlights: string[]
  areas?: string[]
  postcodes?: string[]
  popularVenues: string[]
}

defineProps<{
  area: ServiceArea
  isPrimary: boolean
}>()
</script>