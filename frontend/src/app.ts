/**
 * Vue app entry point for Astro integration.
 * Configures global Vue settings, plugins, and directives.
 */

import type { App } from 'vue'

export default function (app: App) {
  // Global properties that can be accessed in all Vue components
  app.config.globalProperties.$apiBaseUrl = import.meta.env.PUBLIC_API_BASE_URL || 'http://localhost:8000'
  
  // Global error handler for Vue components
  app.config.errorHandler = (err, instance, info) => {
    console.error('Vue Error:', err)
    console.error('Component Info:', info)
    
    // In production, you might want to send errors to an error tracking service
    if (import.meta.env.PROD) {
      // Example: Send to error tracking service
      // errorTrackingService.captureException(err, { extra: { info } })
    }
  }

  // Global warn handler (development only)
  if (import.meta.env.DEV) {
    app.config.warnHandler = (msg, instance, trace) => {
      console.warn('Vue Warning:', msg)
      console.warn('Trace:', trace)
    }
  }

  // Performance tracking
  app.config.performance = import.meta.env.DEV

  // Custom global directives
  
  // v-focus directive for auto-focusing elements
  app.directive('focus', {
    mounted(el) {
      // Focus the element when it's mounted
      el.focus()
    }
  })

  // v-click-outside directive for detecting clicks outside an element
  app.directive('click-outside', {
    beforeMount(el, binding) {
      // Only add event listener on client-side
      if (typeof document !== 'undefined') {
        el.clickOutsideEvent = (event: Event) => {
          // Check if the click was outside the element
          if (!(el === event.target || el.contains(event.target as Node))) {
            binding.value(event)
          }
        }
        document.addEventListener('click', el.clickOutsideEvent)
      }
    },
    unmounted(el) {
      // Only remove event listener on client-side
      if (typeof document !== 'undefined' && el.clickOutsideEvent) {
        document.removeEventListener('click', el.clickOutsideEvent)
      }
    }
  })

  // v-lazy directive for lazy loading images
  app.directive('lazy', {
    beforeMount(el, binding) {
      // Only use IntersectionObserver on client-side
      if (typeof window !== 'undefined' && 'IntersectionObserver' in window) {
        const options = {
          threshold: 0.1,
          rootMargin: '50px'
        }

        const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              const img = entry.target as HTMLImageElement
              img.src = binding.value
              img.classList.remove('opacity-0')
              img.classList.add('opacity-100', 'transition-opacity', 'duration-300')
              observer.unobserve(img)
            }
          })
        }, options)

        el.classList.add('opacity-0')
        observer.observe(el)
      } else {
        // Fallback for SSR: just set the src immediately
        el.src = binding.value
      }
    }
  })

  // Global mixins (use sparingly)
  app.mixin({
    methods: {
      // Utility method to format currency
      $formatCurrency(amount: number, currency: string = 'USD'): string {
        return new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: currency
        }).format(amount)
      },

      // Utility method to format dates
      $formatDate(date: string | Date, options?: Intl.DateTimeFormatOptions): string {
        const dateObj = typeof date === 'string' ? new Date(date) : date
        return new Intl.DateTimeFormat('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          ...options
        }).format(dateObj)
      },

      // Utility method to truncate text
      $truncate(text: string, length: number = 100): string {
        if (text.length <= length) return text
        return text.substring(0, length) + '...'
      },

      // Utility method to validate email
      $isValidEmail(email: string): boolean {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        return emailRegex.test(email)
      },

      // Utility method to validate phone
      $isValidPhone(phone: string): boolean {
        const phoneRegex = /^[\+]?[1-9][\d\s\-\(\)]{7,15}$/
        return phoneRegex.test(phone)
      }
    }
  })

  // Global provide/inject for app-wide state
  app.provide('apiClient', {
    baseUrl: import.meta.env.PUBLIC_API_BASE_URL || 'http://localhost:8000'
  })

  // Development helpers
  if (import.meta.env.DEV) {
    // Make app instance available globally for debugging (client-side only)
    if (typeof window !== 'undefined') {
      ;(window as any).__VUE_APP__ = app
    }
    
    // Add helpful development methods
    app.config.globalProperties.$log = console.log
    app.config.globalProperties.$warn = console.warn
    app.config.globalProperties.$error = console.error
  }
}

// Type declarations for global properties
declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $apiBaseUrl: string
    $formatCurrency: (amount: number, currency?: string) => string
    $formatDate: (date: string | Date, options?: Intl.DateTimeFormatOptions) => string
    $truncate: (text: string, length?: number) => string
    $isValidEmail: (email: string) => boolean
    $isValidPhone: (phone: string) => boolean
    $log?: typeof console.log
    $warn?: typeof console.warn
    $error?: typeof console.error
  }
}