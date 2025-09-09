<!-- src/components/legal/UniversalCookieBanner.vue -->
<template>
    <!-- Cookie Banner -->
    <div 
      v-if="showBanner" 
      class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50 transition-transform duration-300"
      :class="{ 'translate-y-full': !showBanner }"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div class="flex-1">
            <div class="flex items-center mb-2">
              <span class="text-2xl mr-3">🍪</span>
              <h3 class="font-semibold text-gray-900">We use cookies</h3>
            </div>
            <p class="text-sm text-gray-600 leading-relaxed">
              We use cookies to enhance your browsing experience, analyze site traffic, and personalize content.
              <a href="/cookies" class="text-primary-600 hover:text-primary-700 underline font-medium">
                Learn more about our cookie policy
              </a>
            </p>
          </div>
          <div class="flex flex-wrap gap-2">
            <a
              href="/cookies"
              class="px-4 py-2 text-sm border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
            >
              Customize
            </a>
            <button 
              @click="rejectNonEssential"
              class="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 transition-colors"
            >
              Reject All
            </button>
            <button 
              @click="acceptAll"
              class="px-6 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
            >
              Accept All
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  
  // Props to get GA_MEASUREMENT_ID from parent
  const props = defineProps<{
    gaMeasurementId?: string
  }>()
  
  // UI state
  const showBanner = ref(false)
  
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
  const loadPreferences = (): boolean => {
    const consent = getCookie('cookie-consent')
    if (consent) {
      try {
        const preferences = JSON.parse(consent)
        // Apply existing preferences
        applyCookieSettings(preferences.analytics || false, preferences.marketing || false)
        return true
      } catch (e) {
        console.warn('Failed to parse cookie preferences:', e)
      }
    }
    return false
  }
  
  // Save preferences to cookie
  const saveConsentPreferences = (analytics: boolean, marketing: boolean) => {
    const preferences = {
      essential: true,
      analytics: analytics,
      marketing: marketing,
      timestamp: Date.now()
    }
    
    setCookie('cookie-consent', JSON.stringify(preferences), 365)
    applyCookieSettings(analytics, marketing)
  }
  
  // Clear analytics cookies
  const clearAnalyticsCookies = () => {
    if (props.gaMeasurementId && props.gaMeasurementId !== 'GA_MEASUREMENT_ID') {
      const gaId = props.gaMeasurementId.replace('G-', '')
      const cookiesToDelete = [
        '_ga', 
        `_ga_${gaId}`, 
        '_gid', 
        '_gat',
        `_gat_gtag_${props.gaMeasurementId}`
      ]
      
      cookiesToDelete.forEach(cookie => deleteCookie(cookie))
      
      // Clear any remaining GA cookies
      document.cookie.split(';').forEach(cookie => {
        const cookieName = cookie.split('=')[0].trim()
        if (cookieName.startsWith('_ga') || cookieName.startsWith('_gat')) {
          deleteCookie(cookieName)
        }
      })
    }
  }
  
  // Load Google Analytics
  const loadAnalytics = () => {
    if (props.gaMeasurementId && props.gaMeasurementId !== 'GA_MEASUREMENT_ID') {
      // Check if gtag is already loaded
      if (typeof (window as any).gtag === 'undefined') {
        const script = document.createElement('script')
        script.async = true
        script.src = `https://www.googletagmanager.com/gtag/js?id=${props.gaMeasurementId}`
        document.head.appendChild(script)
        
        script.onload = () => {
          ;(window as any).dataLayer = (window as any).dataLayer || []
          function gtag(...args: any[]) {
            ;(window as any).dataLayer.push(args)
          }
          gtag('js', new Date())
          gtag('config', props.gaMeasurementId, {
            anonymize_ip: true,
            cookie_flags: 'SameSite=Lax',
            page_title: document.title,
            page_location: window.location.href,
          })
          ;(window as any).gtag = gtag
          console.log('✅ Google Analytics loaded with consent')
        }
      } else {
        // If gtag is already loaded, just configure it
        ;(window as any).gtag('config', props.gaMeasurementId, {
          anonymize_ip: true,
          cookie_flags: 'SameSite=Lax',
          page_title: document.title,
          page_location: window.location.href,
        })
        console.log('✅ Google Analytics reconfigured with consent')
      }
    }
  }
  
  // Apply cookie settings
  const applyCookieSettings = (analyticsEnabled: boolean, marketingEnabled: boolean) => {
    if (analyticsEnabled) {
      loadAnalytics()
      console.log('✅ Analytics cookies enabled')
    } else {
      clearAnalyticsCookies()
      console.log('❌ Analytics cookies disabled')
    }
  
    if (marketingEnabled) {
      console.log('✅ Marketing cookies enabled')
      // Load marketing scripts here if needed
    } else {
      console.log('❌ Marketing cookies disabled')
      // Clear marketing cookies
      deleteCookie('_fbp')
      deleteCookie('_gcl_au')
    }
  }
  
  // Button handlers
  const acceptAll = () => {
    saveConsentPreferences(true, true)
    showBanner.value = false
    console.log('✅ All cookies accepted')
  }
  
  const rejectNonEssential = () => {
    saveConsentPreferences(false, false)
    showBanner.value = false
    console.log('❌ Non-essential cookies rejected')
  }
  
  // Initialize component
  onMounted(() => {
    const hasConsent = loadPreferences()
    
    if (!hasConsent) {
      // Show banner after a short delay for better UX
      setTimeout(() => {
        showBanner.value = true
      }, 1000)
    }
  })
  
  // Handle ESC key to hide banner
  const handleKeydown = (e: KeyboardEvent) => {
    if (e.key === 'Escape' && showBanner.value) {
      showBanner.value = false
    }
  }
  
  onMounted(() => {
    document.addEventListener('keydown', handleKeydown)
  })
  
  // Cleanup
  import { onUnmounted } from 'vue'
  onUnmounted(() => {
    document.removeEventListener('keydown', handleKeydown)
  })
  
  // Expose methods for external control (optional)
  defineExpose({
    acceptAll,
    rejectNonEssential,
    showBanner: () => showBanner.value = true,
    hideBanner: () => showBanner.value = false
  })
  </script>
  
  <style scoped>
  button:disabled {
    pointer-events: none;
  }
  
  /* Ensure banner is above other fixed elements */
  .z-50 {
    z-index: 50;
  }
  
  /* Smooth banner animation */
  .translate-y-full {
    transform: translateY(100%);
  }
  </style>