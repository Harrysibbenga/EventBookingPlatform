<!-- src/components/legal/CookieManager.vue -->
<template>
    <div class="max-w-2xl mx-auto">
      
      <!-- Current Settings Display -->
      <div class="bg-white rounded-lg border border-neutral-200 p-6 mb-6">
        <h3 class="text-lg font-semibold text-neutral-900 mb-4">Current Cookie Settings</h3>
        
        <div class="space-y-4">
          <!-- Essential Cookies -->
          <div class="flex items-center justify-between p-4 bg-red-50 rounded-lg border border-red-200">
            <div class="flex items-center">
              <div class="w-3 h-3 bg-red-500 rounded-full mr-3"></div>
              <div>
                <h4 class="font-medium text-red-900">Essential Cookies</h4>
                <p class="text-sm text-red-700">Required for website functionality</p>
              </div>
            </div>
            <div class="bg-red-200 text-red-800 px-3 py-1 rounded-full text-sm font-medium">
              Always On
            </div>
          </div>
  
          <!-- Analytics Cookies -->
          <div class="flex items-center justify-between p-4 bg-blue-50 rounded-lg border border-blue-200">
            <div class="flex items-center flex-1">
              <div class="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
              <div>
                <h4 class="font-medium text-blue-900">Analytics Cookies</h4>
                <p class="text-sm text-blue-700">Help us improve our website</p>
              </div>
            </div>
            <button
              @click="toggleAnalytics"
              :class="[
                'relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                analyticsEnabled ? 'bg-blue-600' : 'bg-neutral-200'
              ]"
            >
              <span
                :class="[
                  'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                  analyticsEnabled ? 'translate-x-6' : 'translate-x-1'
                ]"
              />
            </button>
          </div>
  
          <!-- Marketing Cookies -->
          <div class="flex items-center justify-between p-4 bg-purple-50 rounded-lg border border-purple-200">
            <div class="flex items-center flex-1">
              <div class="w-3 h-3 bg-purple-500 rounded-full mr-3"></div>
              <div>
                <h4 class="font-medium text-purple-900">Marketing Cookies</h4>
                <p class="text-sm text-purple-700">Enable personalized advertising</p>
              </div>
            </div>
            <button
              @click="toggleMarketing"
              :class="[
                'relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2',
                marketingEnabled ? 'bg-purple-600' : 'bg-neutral-200'
              ]"
            >
              <span
                :class="[
                  'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                  marketingEnabled ? 'translate-x-6' : 'translate-x-1'
                ]"
              />
            </button>
          </div>
        </div>
      </div>
  
      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-3">
        <button
          @click="acceptAll"
          class="flex-1 bg-gradient-to-r from-primary-600 to-orange-600 text-white px-6 py-3 rounded-lg font-medium hover:from-primary-700 hover:to-orange-700 transition-all duration-200 flex items-center justify-center"
        >
          <CheckCircle class="w-5 h-5 mr-2" />
          Accept All Cookies
        </button>
        
        <button
          @click="savePreferences"
          :disabled="!hasChanges"
          :class="[
            'flex-1 px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center justify-center',
            hasChanges 
              ? 'bg-blue-600 text-white hover:bg-blue-700' 
              : 'bg-neutral-200 text-neutral-500 cursor-not-allowed'
          ]"
        >
          <Settings class="w-5 h-5 mr-2" />
          Save My Preferences
        </button>
        
        <button
          @click="rejectNonEssential"
          class="flex-1 bg-neutral-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-neutral-700 transition-all duration-200 flex items-center justify-center"
        >
          <XCircle class="w-5 h-5 mr-2" />
          Reject Non-Essential
        </button>
      </div>
  
      <!-- Success Message -->
      <Transition
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-2"
      >
        <div v-if="showSuccess" class="mt-6 bg-green-50 border border-green-200 rounded-lg p-4">
          <div class="flex items-center">
            <CheckCircle class="w-5 h-5 text-green-600 mr-3" />
            <div>
              <h4 class="font-medium text-green-900">Preferences Saved</h4>
              <p class="text-sm text-green-700">Your cookie preferences have been updated successfully.</p>
            </div>
          </div>
        </div>
      </Transition>
  
      <!-- Cookie Details -->
      <div class="mt-8 bg-neutral-50 rounded-lg p-6">
        <h3 class="text-lg font-semibold text-neutral-900 mb-4">Cookie Details</h3>
        
        <div class="space-y-4 text-sm text-neutral-600">
          <div>
            <h4 class="font-medium text-neutral-900 mb-2">🔴 Essential Cookies</h4>
            <ul class="space-y-1">
              <li>• <strong>session_id:</strong> Maintains your booking form session</li>
              <li>• <strong>csrf_token:</strong> Security protection</li>
              <li>• <strong>cookie_consent:</strong> Remembers your cookie preferences</li>
            </ul>
          </div>
          
          <div v-if="analyticsEnabled">
            <h4 class="font-medium text-neutral-900 mb-2">🔵 Analytics Cookies</h4>
            <ul class="space-y-1">
              <li>• <strong>_ga:</strong> Google Analytics user identification</li>
              <li>• <strong>_gid:</strong> Google Analytics session identification</li>
              <li>• <strong>_ga_*:</strong> Google Analytics 4 property data</li>
            </ul>
          </div>
          
          <div v-if="marketingEnabled">
            <h4 class="font-medium text-neutral-900 mb-2">🟣 Marketing Cookies</h4>
            <ul class="space-y-1">
              <li>• <strong>_fbp:</strong> Facebook Pixel tracking</li>
              <li>• <strong>_gcl_au:</strong> Google Ads conversion tracking</li>
              <li>• <strong>ig_*:</strong> Instagram integration cookies</li>
            </ul>
          </div>
        </div>
      </div>
  
      <!-- Legal Notice -->
      <div class="mt-6 text-center text-xs text-neutral-500">
        <p>
          By using our website, you agree to our cookie usage as described in this policy.
          <br>
          For more information, see our 
          <a href="/privacy" class="text-primary-600 hover:underline">Privacy Policy</a> 
          and 
          <a href="/terms" class="text-primary-600 hover:underline">Terms of Service</a>.
        </p>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed, onMounted } from 'vue'
  import { CheckCircle, XCircle, Settings } from 'lucide-vue-next'
  
  // Cookie preferences state
  const analyticsEnabled = ref(false)
  const marketingEnabled = ref(false)
  
  // UI state
  const showSuccess = ref(false)
  
  // Initial preferences (stored values)
  const initialAnalytics = ref(false)
  const initialMarketing = ref(false)
  
  // Check if preferences have changed
  const hasChanges = computed(() => {
    return analyticsEnabled.value !== initialAnalytics.value || 
           marketingEnabled.value !== initialMarketing.value
  })
  
  // Cookie management functions
  const setCookie = (name: string, value: string, days: number) => {
    const expires = new Date()
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000))
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Lax`
  }
  
  const getCookie = (name: string): string | null => {
    const nameEQ = name + "="
    const ca = document.cookie.split(';')
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i]
      while (c.charAt(0) === ' ') c = c.substring(1, c.length)
      if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length)
    }
    return null
  }
  
  const deleteCookie = (name: string) => {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`
  }
  
  // Load existing preferences
  const loadPreferences = () => {
    const consent = getCookie('cookie_consent')
    if (consent) {
      try {
        const preferences = JSON.parse(consent)
        analyticsEnabled.value = preferences.analytics || false
        marketingEnabled.value = preferences.marketing || false
        initialAnalytics.value = preferences.analytics || false
        initialMarketing.value = preferences.marketing || false
      } catch (e) {
        console.warn('Failed to parse cookie preferences:', e)
      }
    }
  }
  
  // Save preferences to cookie
  const saveConsentPreferences = () => {
    const preferences = {
      essential: true, // Always true
      analytics: analyticsEnabled.value,
      marketing: marketingEnabled.value,
      timestamp: Date.now()
    }
    
    setCookie('cookie_consent', JSON.stringify(preferences), 365)
    
    // Update initial values
    initialAnalytics.value = analyticsEnabled.value
    initialMarketing.value = marketingEnabled.value
    
    // Apply cookie settings
    applyCookieSettings()
  }
  
  // Apply cookie settings (enable/disable tracking scripts)
  const applyCookieSettings = () => {
    // Handle Google Analytics
    if (analyticsEnabled.value) {
      // Enable Google Analytics (would normally load GA script here)
      console.log('✅ Analytics cookies enabled')
    } else {
      // Disable Google Analytics
      console.log('❌ Analytics cookies disabled')
      // Delete existing GA cookies
      deleteCookie('_ga')
      deleteCookie('_gid')
      deleteCookie('_gat_UA-*')
    }
  
    // Handle Marketing cookies
    if (marketingEnabled.value) {
      // Enable marketing cookies (would normally load marketing scripts here)
      console.log('✅ Marketing cookies enabled')
    } else {
      // Disable marketing cookies
      console.log('❌ Marketing cookies disabled')
      // Delete existing marketing cookies
      deleteCookie('_fbp')
      deleteCookie('_gcl_au')
    }
  }
  
  // Button handlers
  const toggleAnalytics = () => {
    analyticsEnabled.value = !analyticsEnabled.value
  }
  
  const toggleMarketing = () => {
    marketingEnabled.value = !marketingEnabled.value
  }
  
  const acceptAll = () => {
    analyticsEnabled.value = true
    marketingEnabled.value = true
    saveConsentPreferences()
    showSuccessMessage()
  }
  
  const rejectNonEssential = () => {
    analyticsEnabled.value = false
    marketingEnabled.value = false
    saveConsentPreferences()
    showSuccessMessage()
  }
  
  const savePreferences = () => {
    if (hasChanges.value) {
      saveConsentPreferences()
      showSuccessMessage()
    }
  }
  
  const showSuccessMessage = () => {
    showSuccess.value = true
    setTimeout(() => {
      showSuccess.value = false
    }, 3000)
  }
  
  // Initialize component
  onMounted(() => {
    loadPreferences()
  })
  </script>
  
  <style scoped>
  /* Additional component-specific styles if needed */
  button:disabled {
    pointer-events: none;
  }
  
  /* Smooth transitions for toggles */
  button[role="switch"] {
    transition: all 0.2s ease-in-out;
  }
  </style>