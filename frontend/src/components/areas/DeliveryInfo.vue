// src/components/areas/DeliveryInfo.vue
<template>
  <section class="py-16 lg:py-24 bg-gradient-to-br from-blue-50 to-indigo-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <div class="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium mb-6">
          🚛 Delivery Information
        </div>
        <h2 class="text-3xl lg:text-4xl font-bold text-neutral-900 mb-4">
          Professional Setup & Collection Service
        </h2>
        <p class="text-lg text-neutral-600 max-w-3xl mx-auto">
          We handle everything from delivery to setup, styling, and next-day collection so you can focus on enjoying your celebration.
        </p>
      </div>

      <div class="grid lg:grid-cols-3 gap-8">
        
        <!-- Delivery Process -->
        <div class="bg-white rounded-2xl shadow-sm border border-neutral-200 p-8">
          <div class="text-center mb-6">
            <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <Truck class="w-8 h-8 text-white" />
            </div>
            <h3 class="text-xl font-bold text-neutral-900">Delivery & Setup</h3>
          </div>
          
          <div class="space-y-4 text-sm">
            <div class="flex items-start">
              <Clock class="w-4 h-4 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
              <div>
                <div class="font-medium text-neutral-900">{{ serviceDetails.standardDelivery.time }}</div>
                <div class="text-neutral-600">Flexible delivery window</div>
              </div>
            </div>
            
            <div class="flex items-start">
              <Phone class="w-4 h-4 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
              <div>
                <div class="font-medium text-neutral-900">{{ serviceDetails.standardDelivery.notification }}</div>
                <div class="text-neutral-600">Advance notification call</div>
              </div>
            </div>
            
            <div class="flex items-start">
              <Settings class="w-4 h-4 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
              <div>
                <div class="font-medium text-neutral-900">{{ serviceDetails.standardDelivery.included }}</div>
                <div class="text-neutral-600">Professional presentation</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pricing Structure -->
        <div class="bg-white rounded-2xl shadow-sm border border-neutral-200 p-8">
          <div class="text-center mb-6">
            <div class="w-16 h-16 bg-gradient-to-r from-primary-500 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <PoundSterling class="w-8 h-8 text-white" />
            </div>
            <h3 class="text-xl font-bold text-neutral-900">Delivery Pricing</h3>
          </div>
          
          <div class="space-y-4">
            <div class="p-4 bg-green-50 border border-green-200 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium text-green-900">{{ primaryArea }}</span>
                <span class="text-lg font-bold text-green-600">FREE</span>
              </div>
              <div class="text-sm text-green-700">
                {{ serviceDetails.coverage.primary }}
              </div>
            </div>
            
            <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium text-blue-900">Extended Areas</span>
                <span class="text-sm text-blue-600">£15-30</span>
              </div>
              <div class="text-sm text-blue-700">
                {{ serviceDetails.coverage.extended }}
              </div>
            </div>
            
            <div class="p-4 bg-neutral-50 border border-neutral-200 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium text-neutral-900">Special Locations</span>
                <span class="text-sm text-neutral-600">Quote</span>
              </div>
              <div class="text-sm text-neutral-600">
                {{ serviceDetails.coverage.quote }}
              </div>
            </div>
          </div>
        </div>

        <!-- Collection Service -->
        <div class="bg-white rounded-2xl shadow-sm border border-neutral-200 p-8">
          <div class="text-center mb-6">
            <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <Calendar class="w-8 h-8 text-white" />
            </div>
            <h3 class="text-xl font-bold text-neutral-900">Collection</h3>
          </div>
          
          <div class="space-y-4 text-sm">
            <div class="flex items-start">
              <Calendar class="w-4 h-4 text-purple-500 mr-3 mt-0.5 flex-shrink-0" />
              <div>
                <div class="font-medium text-neutral-900">{{ serviceDetails.collection.time }}</div>
                <div class="text-neutral-600">Standard 24-hour hire</div>
              </div>
            </div>
            
            <div class="flex items-start">
              <Clock class="w-4 h-4 text-purple-500 mr-3 mt-0.5 flex-shrink-0" />
              <div>
                <div class="font-medium text-neutral-900">{{ serviceDetails.collection.window }}</div>
                <div class="text-neutral-600">Convenient timing</div>
              </div>
            </div>
            
            <div class="flex items-start">
              <CheckCircle class="w-4 h-4 text-purple-500 mr-3 mt-0.5 flex-shrink-0" />
              <div>
                <div class="font-medium text-neutral-900">{{ serviceDetails.collection.flexibility }}</div>
                <div class="text-neutral-600">Accommodating schedules</div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Service Guarantee -->
      <div class="mt-12 bg-gradient-to-r from-primary-600 to-orange-600 text-white rounded-2xl p-8 text-center">
        <div class="max-w-3xl mx-auto">
          <h3 class="text-2xl font-bold mb-4">Our Service Promise</h3>
          <p class="text-primary-100 mb-6 leading-relaxed">
            Professional, reliable service across all our coverage areas. We're fully insured, experienced with all venue types, and committed to making your celebration perfect.
          </p>
          <div class="grid md:grid-cols-3 gap-6 text-center">
            <div>
              <Shield class="w-8 h-8 mx-auto mb-2 text-primary-200" />
              <div class="font-semibold">Fully Insured</div>
            </div>
            <div>
              <Award class="w-8 h-8 mx-auto mb-2 text-primary-200" />
              <div class="font-semibold">Experienced Team</div>
            </div>
            <div>
              <Heart class="w-8 h-8 mx-auto mb-2 text-primary-200" />
              <div class="font-semibold">Customer Focused</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { 
  Truck, Clock, Phone, Settings, PoundSterling, Calendar, 
  CheckCircle, Shield, Award, Heart 
} from 'lucide-vue-next'

interface ServiceDetails {
  standardDelivery: {
    time: string
    notification: string
    included: string
  }
  collection: {
    time: string
    window: string
    flexibility: string
  }
  coverage: {
    primary: string
    extended: string
    quote: string
  }
}

defineProps<{
  serviceDetails: ServiceDetails
  primaryArea: string
  freeDeliveryRadius: string
}>()
</script>