// src/components/legal/LegalSection.vue
<template>
  <section 
    :id="id"
    :class="[
      'scroll-mt-24 mb-12',
      highlight ? 'bg-gradient-to-r from-neutral-50 to-white rounded-2xl p-8 border border-neutral-200' : ''
    ]"
  >
    <!-- Section Header -->
    <div class="flex items-start mb-6">
      <div class="flex-shrink-0 mr-4">
        <div 
          :class="[
            'w-12 h-12 rounded-full flex items-center justify-center text-xl',
            highlight 
              ? 'bg-gradient-to-r from-primary-500 to-orange-500 text-white shadow-lg' 
              : 'bg-neutral-100 text-neutral-600'
          ]"
        >
          {{ icon }}
        </div>
      </div>
      <div class="flex-grow">
        <h2 
          :class="[
            'text-2xl font-bold mb-2',
            highlight ? 'text-primary-900' : 'text-neutral-900'
          ]"
        >
          {{ title }}
        </h2>
        <div class="h-1 bg-gradient-to-r from-primary-500 to-orange-500 rounded-full w-16"></div>
      </div>
    </div>

    <!-- Section Content -->
    <div class="prose prose-lg prose-neutral max-w-none">
      <slot />
    </div>

    <!-- Section Divider -->
    <div class="mt-8 pt-8 border-t border-neutral-200"></div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  id: string
  title: string
  icon: string
  highlight?: boolean
}>()
</script>

<style scoped>
/* Custom prose styling for legal content */
:deep(.prose) {
  @apply text-neutral-700;
}

:deep(.prose h3) {
  @apply text-lg font-semibold text-neutral-900 mt-6 mb-3;
}

:deep(.prose h4) {
  @apply text-base font-semibold text-neutral-800 mt-4 mb-2;
}

:deep(.prose ul) {
  @apply space-y-2;
}

:deep(.prose li) {
  @apply leading-relaxed;
}

:deep(.prose strong) {
  @apply text-neutral-900 font-semibold;
}

:deep(.prose a) {
  @apply text-primary-600 hover:text-primary-700 font-medium no-underline hover:underline transition-colors;
}

:deep(.prose p) {
  @apply leading-relaxed mb-4;
}
</style>