<template>
  <nav
    class="fixed top-0 left-0 right-0 z-50 border-b transition-all duration-300"
    :class="[
      isScrolled
        ? 'bg-brand-black/80 border-brand-gold/20 backdrop-blur-md shadow-gold-glow'
        : 'bg-transparent border-transparent'
    ]"
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
            <div
              class="w-10 h-10 rounded-lg flex items-center justify-center bg-gold-gradient shadow-gold-glow transition-all duration-300 group-hover:shadow-gold-strong"
            >
              <img :src="image" alt="Logo" class="w-8 h-8" />
            </div>
            <div class="hidden sm:block">
              <h1 class="text-xl font-bold text-brand-gold transition-colors group-hover:text-brand-gold/90">
                {{ BUSINESS_INFO.name }}
              </h1>
              <p class="text-sm text-neutral-200/70 -mt-1">{{ BUSINESS_INFO.tagline }}</p>
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
            class="inline-flex items-center justify-center rounded-lg px-6 py-2.5 font-semibold
                   text-brand-black bg-gold-gradient shadow-gold-strong
                   transition-all duration-200 hover:shadow-gold-glow hover:-translate-y-0.5
                   focus:outline-none focus:ring-2 focus:ring-brand-gold/40"
          >
            Get Quote
          </a>
        </div>

        <!-- Mobile menu button -->
        <div class="lg:hidden">
          <button
            @click="toggleMobileMenu"
            class="p-2 rounded-md text-brand-gold hover:text-brand-gold/90 hover:bg-white/5 focus:outline-none focus:ring-2 focus:ring-brand-gold/40 transition-colors"
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
        class="lg:hidden bg-brand-black/95 border-b border-brand-gold/15 shadow-gold-glow"
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
          <div class="pt-4 mt-4 border-t border-brand-gold/15">
            <a
              href="/booking"
              @click="closeMobileMenu"
              class="flex items-center justify-center w-full rounded-lg px-4 py-3 font-semibold
                     text-brand-black bg-gold-gradient shadow-gold-strong
                     transition-all hover:shadow-gold-glow"
            >
              <Calendar class="w-5 h-5 mr-2" />
              Get Your Quote
            </a>
          </div>

          <!-- Contact Info -->
          <div class="pt-4 space-y-2">
            <div class="flex items-center text-neutral-200/80">
              <Phone class="w-4 h-4 mr-2 text-brand-gold" />
              <a :href="`tel:${BUSINESS_INFO.phone}`" class="hover:text-brand-gold transition-colors">
                {{ BUSINESS_INFO.phone }}
              </a>
            </div>
            <div class="flex items-center text-neutral-200/80">
              <Mail class="w-4 h-4 mr-2 text-brand-gold" />
              <a :href="`mailto:${BUSINESS_INFO.email}`" class="hover:text-brand-gold transition-colors">
                {{ BUSINESS_INFO.email }}
              </a>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </nav>

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
        class="fixed inset-0 bg-black/50 backdrop-blur-sm lg:hidden"
        @click="closeMobileMenu"
        aria-hidden="true"
      />
    </Transition>
</template>


<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { 
  Home, 
  Image, 
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
    name: 'Why Us',
    path: '#why',
    icon: Info
  },
  {
    name: 'Gallery',
    path: '#gallery',
    icon: Image
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
/* Desktop Navigation Links (black + gold) */
.nav-link {
  @apply relative px-3 py-2 text-sm font-medium
         text-neutral-200/80 hover:text-brand-gold
         rounded-md transition-all duration-200;
}

.nav-link::after {
  content: '';
  @apply absolute bottom-0 left-0 h-0.5 w-0
         bg-brand-gold transition-all duration-200;
}

.nav-link:hover::after {
  @apply w-full;
}

.nav-link-active {
  @apply text-brand-gold;
}

.nav-link-active::after {
  @apply w-full;
}

/* Mobile Navigation Links (dark glass menu) */
.mobile-nav-link {
  @apply flex items-center gap-3 px-3 py-3 text-base font-medium
         text-neutral-200/85 rounded-md
         transition-all duration-200
         hover:text-brand-gold hover:bg-white/5;
}

.mobile-nav-link-active {
  @apply text-brand-gold bg-white/5;
}

/* Keep your transition classes for menu enter/leave */
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

/* Focus states for accessibility (gold ring) */
.nav-link:focus,
.mobile-nav-link:focus {
  @apply outline-none ring-2 ring-brand-gold/40 ring-offset-2 ring-offset-transparent;
}

/* Hover micro-lift */
.nav-link:hover {
  transform: translateY(-1px);
}

/* Logo hover effect (kept) */
.group:hover .w-10 {
  transform: rotate(5deg) scale(1.05);
}
</style>
