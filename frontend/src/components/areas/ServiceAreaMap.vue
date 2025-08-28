// src/components/areas/ServiceAreaMap.vue
<template>
  <div class="bg-white rounded-2xl shadow-lg border border-neutral-200 p-8">
    <!-- Map Header -->
    <div class="text-center mb-8">
      <h3 class="text-2xl font-bold text-neutral-900 mb-2">Interactive Coverage Map</h3>
      <p class="text-neutral-600">Click on an area to see detailed information</p>
    </div>

    <!-- Map Container -->
    <div class="relative bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-8 mb-8 overflow-hidden min-h-96">
      <!-- Central Milton Keynes -->
      <div 
        class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-20"
        @click="selectArea('milton-keynes')"
      >
        <div class="relative">
          <div class="w-16 h-16 bg-primary-500 rounded-full flex items-center justify-center text-white font-bold text-lg cursor-pointer hover:bg-primary-600 transition-all duration-200 transform hover:scale-110 shadow-lg">
            MK
          </div>
          <div class="absolute -bottom-8 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
            <div class="bg-white px-2 py-1 rounded shadow-md text-sm font-medium text-neutral-900">
              Milton Keynes
            </div>
          </div>
          <!-- Primary coverage circle -->
          <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-32 h-32 border-2 border-primary-300 rounded-full animate-pulse -z-10"></div>
        </div>
      </div>

      <!-- Surrounding Areas -->
      <div 
        v-for="(area, index) in surroundingAreas" 
        :key="area.id"
        :class="getAreaClasses(area)"
        :style="getAreaPosition(area.id)"
        @click="selectArea(area.id)"
      >
        <div class="text-sm font-medium text-center cursor-pointer hover:scale-110 transition-all duration-200">
          <div :class="getAreaIconClasses(area.isPrimary)">
            {{ area.icon }}
          </div>
          <div class="mt-2 text-xs font-medium">{{ area.name }}</div>
          <div v-if="area.deliveryFee === 0" class="text-xs text-green-600 font-medium">FREE</div>
          <div v-else class="text-xs text-neutral-500">£{{ area.deliveryFee }}</div>
        </div>
      </div>

      <!-- Distance Indicators -->
      <div class="absolute bottom-4 right-4 bg-white/80 backdrop-blur-sm rounded-lg p-3">
        <div class="text-xs text-neutral-600 space-y-1">
          <div class="flex items-center">
            <div class="w-3 h-3 bg-primary-500 rounded-full mr-2"></div>
            <span>Primary Areas</span>
          </div>
          <div class="flex items-center">
            <div class="w-3 h-3 bg-blue-500 rounded-full mr-2"></div>
            <span>Extended Areas</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Selected Area Details -->
    <div v-if="selectedArea" class="bg-gradient-to-r from-primary-50 to-orange-50 rounded-xl p-6">
      <div class="flex items-start justify-between mb-4">
        <div>
          <h4 class="text-xl font-bold text-primary-900 mb-1">{{ selectedArea.name }}</h4>
          <p class="text-primary-700">{{ selectedArea.county }}</p>
        </div>
        <div class="text-3xl">{{ selectedArea.icon }}</div>
      </div>
      
      <p class="text-primary-800 mb-4">{{ selectedArea.description }}</p>
      
      <div class="grid sm:grid-cols-3 gap-4 text-sm">
        <div class="bg-white/50 rounded-lg p-3">
          <div class="font-semibold text-primary-900 mb-1">Delivery Fee</div>
          <div class="text-primary-700">
            {{ selectedArea.deliveryFee === 0 ? 'FREE' : `£${selectedArea.deliveryFee}` }}
          </div>
        </div>
        <div class="bg-white/50 rounded-lg p-3">
          <div class="font-semibold text-primary-900 mb-1">Setup Time</div>
          <div class="text-primary-700">{{ selectedArea.setupTime }}</div>
        </div>
        <div class="bg-white/50 rounded-lg p-3">
          <div class="font-semibold text-primary-900 mb-1">Coverage</div>
          <div class="text-primary-700">{{ selectedArea.coverage }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

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
}

const props = defineProps<{
  areas: ServiceArea[]
  primaryLocation: string
}>()

const selectedAreaId = ref<string>('milton-keynes')

const selectedArea = computed(() => 
  props.areas.find(area => area.id === selectedAreaId.value)
)

const surroundingAreas = computed(() => 
  props.areas.filter(area => area.id !== 'milton-keynes')
)

const selectArea = (areaId: string) => {
  selectedAreaId.value = areaId
}

const getAreaClasses = (area: ServiceArea) => {
  return [
    'absolute transform -translate-x-1/2 -translate-y-1/2',
    area.isPrimary ? 'z-10' : 'z-5'
  ]
}

const getAreaIconClasses = (isPrimary: boolean) => {
  return [
    'w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold mx-auto',
    isPrimary ? 'bg-primary-400 text-white' : 'bg-blue-400 text-white'
  ]
}

const getAreaPosition = (areaId: string) => {
  const positions: Record<string, string> = {
    'buckinghamshire': 'top: 30%; left: 30%',
    'bedfordshire': 'top: 25%; right: 20%',
    'northamptonshire': 'bottom: 35%; left: 25%',
    'oxfordshire': 'bottom: 30%; left: 15%',
    'hertfordshire': 'top: 40%; right: 15%'
  }
  return positions[areaId] || 'top: 50%; left: 50%'
}
</script>