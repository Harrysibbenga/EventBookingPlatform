<template>
  <nav 
    class="fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-md border-b border-neutral-200/50 transition-all duration-300"
    :class="{ 'shadow-lg': isScrolled }"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16 lg:h-20">
        <!-- Logo -->
        <div class="flex-shrink-0 flex items-center">
          <a 
            href="/" 
            class="flex items-center space-x-3 group"
            @click="closeMobileMenu"
          >
            <div class="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center shadow-md group-hover:shadow-lg transition-shadow">
              <img :src="image" alt="Logo" class="w-8 h-8" />
            </div>
            <div class="hidden sm:block">
              <h1 class="text-xl font-bold text-neutral-900 group-hover:text-primary-600 transition-colors">
                {{ BUSINESS_INFO.name }}
              </h1>
              <p class="text-sm text-neutral-600 -mt-1">{{ BUSINESS_INFO.tagline }}</p>
            </div>
          </a>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden lg:block">
          <div class="ml-10 flex items-baseline space-x-8">
            <a
              v-for="link in navigationLinks"
              :key="link.path"
              :href="link.path"
              class="nav-link"
              :class="{ 'nav-link-active': isCurrentPage(link.path) }"
            >
              {{ link.name }}
            </a>
          </div>
        </div>

        <!-- CTA Button -->
        <div class="hidden lg:block">
          <a
            href="/booking"
            class="bg-primary-600 hover:bg-primary-700 text-white px-6 py-2.5 rounded-lg font-medium transition-all duration-200 hover:shadow-lg hover:scale-105 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          >
            Get Quote
          </a>
        </div>

        <!-- Mobile menu button -->
        <div class="lg:hidden">
          <button
            @click="toggleMobileMenu"
            class="p-2 rounded-md text-neutral-600 hover:text-neutral-900 hover:bg-neutral-100 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
            :aria-expanded="isMobileMenuOpen"
            aria-label="Toggle navigation menu"
          >
            <svg
              class="w-6 h-6 transition-transform duration-200"
              :class="{ 'rotate-90': isMobileMenuOpen }"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                v-if="!isMobileMenuOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation Menu -->
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="transform -translate-y-full opacity-0"
      enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform -translate-y-full opacity-0"
    >
      <div 
        v-show="isMobileMenuOpen"
        class="lg:hidden bg-white border-b border-neutral-200 shadow-lg"
      >
        <div class="px-4 pt-4 pb-6 space-y-1">
          <a
            v-for="link in navigationLinks"
            :key="link.path"
            :href="link.path"
            @click="closeMobileMenu"
            class="mobile-nav-link"
            :class="{ 'mobile-nav-link-active': isCurrentPage(link.path) }"
          >
            <component :is="link.icon" class="w-5 h-5" />
            {{ link.name }}
          </a>
          
          <!-- Mobile CTA -->
          <div class="pt-4 mt-4 border-t border-neutral-200">
            <a
              href="/booking"
              @click="closeMobileMenu"
              class="flex items-center justify-center w-full bg-primary-600 hover:bg-primary-700 text-white px-4 py-3 rounded-lg font-medium transition-colors"
            >
              <Calendar class="w-5 h-5 mr-2" />
              Get Your Quote
            </a>
          </div>
          
          <!-- Contact Info -->
          <div class="pt-4 space-y-2">
            <div class="flex items-center text-neutral-600">
              <Phone class="w-4 h-4 mr-2" />
              <a :href="`tel:${BUSINESS_INFO.phone}`" class="hover:text-primary-600 transition-colors">
                {{ BUSINESS_INFO.phone }}
              </a>
            </div>
            <div class="flex items-center text-neutral-600">
              <Mail class="w-4 h-4 mr-2" />
              <a :href="`mailto:${BUSINESS_INFO.email}`" class="hover:text-primary-600 transition-colors">
                {{ BUSINESS_INFO.email }}
              </a>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Mobile Menu Overlay -->
    <Transition
      enter-active-class="transition-opacity duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-show="isMobileMenuOpen"
        class="fixed inset-0 bg-black/20 backdrop-blur-sm lg:hidden -z-10"
        @click="closeMobileMenu"
        aria-hidden="true"
      />
    </Transition>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { 
  Home, 
  Image, 
  DollarSign, 
  Calendar, 
  Mail, 
  Phone, 
  Info,
  Sparkles
} from 'lucide-vue-next'
import { BUSINESS_INFO, SEO_CONFIG } from '../../utils/constants'

const image = SEO_CONFIG.image

// Navigation links configuration
const navigationLinks = [
  {
    name: 'Home',
    path: '#home',
    icon: Home
  },
  {
    name: 'Services',
    path: '#services',
    icon: Sparkles
  },
  {
    name: 'Gallery',
    path: '#gallery',
    icon: Image
  },
  {
    name: 'Why Us',
    path: '#why',
    icon: Info
  },
  {
    name: 'Contact',
    path: '#contact',
    icon: Mail
  }
] as const


// Reactive state
const isMobileMenuOpen = ref(false)
const isScrolled = ref(false)

// Get current page path
const getCurrentPath = () => {
  if (typeof window !== 'undefined') {
    return window.location.pathname
  }
  return '/'
}

// Check if current page matches link
const isCurrentPage = (path: string): boolean => {
  const currentPath = getCurrentPath()
  if (path === '/') {
    return currentPath === '/'
  }
  return currentPath.startsWith(path)
}

// Mobile menu functions
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

// Scroll handler for navigation styling
const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

// Handle escape key
const handleEscape = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && isMobileMenuOpen.value) {
    closeMobileMenu()
  }
}

// Lifecycle hooks
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  document.addEventListener('keydown', handleEscape)
  
  // Close menu on route change (for client-side navigation)
  window.addEventListener('popstate', closeMobileMenu)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.removeEventListener('keydown', handleEscape)
  window.removeEventListener('popstate', closeMobileMenu)
})
</script>

<style scoped>
/* Desktop Navigation Links */
.nav-link {
  @apply text-neutral-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 relative;
}

.nav-link::after {
  content: '';
  @apply absolute bottom-0 left-0 w-0 h-0.5 bg-primary-600 transition-all duration-200;
}

.nav-link:hover::after {
  @apply w-full;
}

.nav-link-active {
  @apply text-primary-600;
}

.nav-link-active::after {
  @apply w-full;
}

/* Mobile Navigation Links */
.mobile-nav-link {
  @apply flex items-center space-x-3 text-neutral-700 hover:text-primary-600 hover:bg-primary-50 px-3 py-3 rounded-md text-base font-medium transition-all duration-200;
}

.mobile-nav-link-active {
  @apply text-primary-600 bg-primary-50;
}

/* Animation classes for smooth transitions */
.nav-enter-active,
.nav-leave-active {
  transition: all 0.3s ease;
}

.nav-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.nav-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Focus states for accessibility */
.nav-link:focus,
.mobile-nav-link:focus {
  @apply outline-none ring-2 ring-primary-500 ring-offset-2;
}

/* Hover animations */
.nav-link:hover {
  transform: translateY(-1px);
}

/* Logo hover effect */
.group:hover .w-10 {
  transform: rotate(5deg) scale(1.05);
}
</style>