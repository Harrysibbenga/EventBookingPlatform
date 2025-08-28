// src/components/legal/TableOfContents.vue
<template>
  <div class="bg-white rounded-2xl shadow-sm border border-neutral-200 p-6 sticky top-24">
    <h3 class="text-lg font-bold text-neutral-900 mb-4 flex items-center">
      <span class="mr-2">📋</span>
      Table of Contents
    </h3>

    <nav class="space-y-1">
      <a
        v-for="section in sections"
        :key="section.id"
        :href="`#${section.id}`"
        :class="[
          'block px-3 py-2 rounded-lg text-sm transition-colors duration-200',
          activeSection === section.id
            ? 'bg-primary-50 text-primary-700 font-medium'
            : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
        ]"
        @click="handleClick(section.id, $event)"
      >
        {{ section.title }}
      </a>
    </nav>

    <!-- Progress Indicator -->
    <div class="mt-6 pt-4 border-t border-neutral-200">
      <div class="flex items-center justify-between text-xs text-neutral-500 mb-2">
        <span>Reading Progress</span>
        <span>{{ Math.round(scrollProgress) }}%</span>
      </div>
      <div class="w-full bg-neutral-200 rounded-full h-2">
        <div 
          class="bg-gradient-to-r from-primary-500 to-orange-500 h-2 rounded-full transition-all duration-300"
          :style="{ width: `${scrollProgress}%` }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Section {
  id: string
  title: string
}

defineProps<{
  sections: Section[]
}>()

const activeSection = ref('')
const scrollProgress = ref(0)

const handleClick = (sectionId: string, event: Event) => {
  event.preventDefault()
  const element = document.getElementById(sectionId)
  if (element) {
    const headerOffset = 100
    const elementPosition = element.getBoundingClientRect().top
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    })
  }
}

const updateActiveSection = () => {
  const sections = document.querySelectorAll('[id^=""]')
  const scrollPos = window.scrollY + 150

  sections.forEach((section) => {
    const element = section as HTMLElement
    const sectionTop = element.offsetTop
    const sectionHeight = element.offsetHeight

    if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
      activeSection.value = element.id
    }
  })

  // Calculate scroll progress
  const docHeight = document.documentElement.scrollHeight - window.innerHeight
  const scrolled = window.scrollY
  scrollProgress.value = Math.min((scrolled / docHeight) * 100, 100)
}

onMounted(() => {
  window.addEventListener('scroll', updateActiveSection)
  updateActiveSection()
})

onUnmounted(() => {
  window.removeEventListener('scroll', updateActiveSection)
})
</script>