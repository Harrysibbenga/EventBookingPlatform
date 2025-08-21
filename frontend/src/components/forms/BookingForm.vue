<template>
    <div class="max-w-4xl mx-auto">
      <!-- Form Header -->
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-neutral-900 mb-4">Book Your Event</h2>
        <p class="text-lg text-neutral-600">
          Tell us about your event and we'll create something extraordinary together
        </p>
      </div>
  
      <!-- Progress Indicator -->
      <div class="mb-8">
        <div class="flex items-center justify-center space-x-4">
          <div
            v-for="(step, index) in steps"
            :key="step.id"
            class="flex items-center"
          >
            <div
              class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all duration-300"
              :class="[
                index < currentStep 
                  ? 'bg-primary-600 text-white' 
                  : index === currentStep 
                    ? 'bg-primary-100 text-primary-600 border-2 border-primary-600' 
                    : 'bg-neutral-200 text-neutral-500'
              ]"
            >
              <Check v-if="index < currentStep" class="w-4 h-4" />
              <span v-else>{{ index + 1 }}</span>
            </div>
            <span 
              class="ml-2 text-sm font-medium"
              :class="index <= currentStep ? 'text-neutral-900' : 'text-neutral-500'"
            >
              {{ step.title }}
            </span>
            <ChevronRight 
              v-if="index < steps.length - 1" 
              class="w-4 h-4 text-neutral-400 mx-4" 
            />
          </div>
        </div>
      </div>
  
      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="space-y-8">
        <!-- Step 1: Event Details -->
        <div v-show="currentStep === 0" class="animate-fade-in-up">
          <h3 class="text-xl font-semibold text-neutral-900 mb-6">Event Details</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Event Type -->
            <div>
              <label class="block text-sm font-medium text-neutral-700 mb-2">
                Event Type *
              </label>
              <select
                v-model="formData.event_type"
                required
                class="form-select"
                :class="{ 'border-red-500': errors.event_type }"
              >
                <option value="">Select event type</option>
                <option
                  v-for="eventType in eventTypes"
                  :key="eventType.value"
                  :value="eventType.value"
                >
                  {{ eventType.label }}
                </option>
              </select>
              <p v-if="errors.event_type" class="text-red-500 text-sm mt-1">
                {{ errors.event_type }}
              </p>
            </div>
  
            <!-- Event Date -->
            <div>
              <label class="block text-sm font-medium text-neutral-700 mb-2">
                Event Date *
              </label>
              <input
                v-model="formData.event_date"
                type="date"
                required
                :min="minDate"
                class="form-input"
                :class="{ 'border-red-500': errors.event_date }"
              />
              <p v-if="errors.event_date" class="text-red-500 text-sm mt-1">
                {{ errors.event_date }}
              </p>
            </div>
  
            <!-- Event Time -->
            <div>
              <label class="block text-sm font-medium text-neutral-700 mb-2">
                Event Time
              </label>
              <select
                v-model="formData.event_time"
                class="form-select"
              >
                <option value="">Select time</option>
                <option
                  v-for="time in timeSlots"
                  :key="time"
                  :value="time"
                >
                  {{ time }}
                </option>
              </select>
            </div>
  
            <!-- Guest Count -->
            <div>
              <label class="block text-sm font-medium text-neutral-700 mb-2">
                Number of Guests *
              </label>
              <input
                v-model.number="formData.guest_count"
                type="number"
                min="1"
                max="1000"
                required
                placeholder="e.g., 100"
                class="form-input"
                :class="{ 'border-red-500': errors.guest_count }"
              />
              <p v-if="errors.guest_count" class="text-red-500 text-sm mt-1">
                {{ errors.guest_count }}
              </p>
            </div>
  
            <!-- Duration -->
            <div>
              <label class="block text-sm font-medium text-neutral-700 mb-2">
                Event Duration (hours)
              </label>
              <input
                v-model.number="formData.duration_hours"
                type="number"
                min="1"
                max="24"
                placeholder="e.g., 6"
                class="form-input"
              />
            </div>
          </div>
        </div>
  
        <!-- Step 2: Venue & Services -->
        <div v-show="currentStep === 1" class="animate-fade-in-up">
          <h3 class="text-xl font-semibold text-neutral-900 mb-6">Venue & Services</h3>
          
          <div class="space-y-6">
            <!-- Venue Information -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-neutral-700 mb-2">
                  Venue Name
                </label>
                <input
                  v-model="formData.venue_name"
                  type="text"
                  placeholder="e.g., Grand Ballroom"
                  class="form-input"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-neutral-700 mb-2">
                  Venue Type
                </label>
                <select v-model="formData.venue_type" class="form-select">
                  <option value="">Select venue type</option>
                  <option
                    v-for="venueType in venueTypes"
                    :key="venueType"
                    :value="venueType"
                  >
                    {{ venueType }}
                  </option>
                </select>
              </div>
            </div>
  
            <div>
              <label class="block text-sm font-medium text-neutral-700 mb-2">
                Venue Address
              </label>
              <textarea
                v-model="formData.venue_address"
                rows="2"
                placeholder="Full venue address"
                class="form-textarea"
              ></textarea>
            </div>
  
            <!-- Services Needed -->
            <div>
              <label class="block text-sm font-medium text-neutral-700 mb-3">
                Services Needed
              </label>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <label
                  v-for="service in services"
                  :key="service.id"
                  class="flex items-center space-x-2 cursor-pointer"
                >
                  <input
                    type="checkbox"
                    :value="service.name"
                    v-model="selectedServices"
                    class="rounded border-neutral-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span class="text-sm text-neutral-700">{{ service.name }}</span>
                </label>
              </div>
            </div>
  
            <!-- Budget Range -->
            <div>
              <label class="block text-sm font-medium text-neutral-700 mb-3">
                Budget Range
              </label>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <input
                    v-model.number="formData.budget_min"
                    type="number"
                    min="0"
                    placeholder="Minimum budget"
                    class="form-input"
                  />
                </div>
                <div>
                  <input
                    v-model.number="formData.budget_max"
                    type="number"
                    min="0"
                    placeholder="Maximum budget"
                    class="form-input"
                  />
                </div>
              </div>
              <div class="mt-2">
                <label class="flex items-center space-x-2">
                  <input
                    v-model="formData.budget_flexible"
                    type="checkbox"
                    class="rounded border-neutral-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span class="text-sm text-neutral-600">Budget is flexible</span>
                </label>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Step 3: Contact & Details -->
        <div v-show="currentStep === 2" class="animate-fade-in-up">
          <h3 class="text-xl font-semibold text-neutral-900 mb-6">Contact Information</h3>
          
          <div class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Contact Name -->
              <div>
                <label class="block text-sm font-medium text-neutral-700 mb-2">
                  Full Name *
                </label>
                <input
                  v-model="formData.contact_name"
                  type="text"
                  required
                  placeholder="Your full name"
                  class="form-input"
                  :class="{ 'border-red-500': errors.contact_name }"
                />
                <p v-if="errors.contact_name" class="text-red-500 text-sm mt-1">
                  {{ errors.contact_name }}
                </p>
              </div>
  
              <!-- Email -->
              <div>
                <label class="block text-sm font-medium text-neutral-700 mb-2">
                  Email Address *
                </label>
                <input
                  v-model="formData.contact_email"
                  type="email"
                  required
                  placeholder="your@email.com"
                  class="form-input"
                  :class="{ 'border-red-500': errors.contact_email }"
                />
                <p v-if="errors.contact_email" class="text-red-500 text-sm mt-1">
                  {{ errors.contact_email }}
                </p>
              </div>
  
              <!-- Phone -->
              <div>
                <label class="block text-sm font-medium text-neutral-700 mb-2">
                  Phone Number
                </label>
                <input
                  v-model="formData.contact_phone"
                  type="tel"
                  placeholder="(555) 123-4567"
                  class="form-input"
                />
              </div>
  
              <!-- Preferred Contact -->
              <div>
                <label class="block text-sm font-medium text-neutral-700 mb-2">
                  Preferred Contact Method
                </label>
                <select v-model="formData.preferred_contact" class="form-select">
                  <option
                    v-for="method in contactMethods"
                    :key="method.value"
                    :value="method.value"
                  >
                    {{ method.label }}
                  </option>
                </select>
              </div>
            </div>
  
            <!-- Special Requirements -->
            <div>
              <label class="block text-sm font-medium text-neutral-700 mb-2">
                Special Requirements or Notes
              </label>
              <textarea
                v-model="formData.special_requirements"
                rows="4"
                placeholder="Any special requests, dietary restrictions, accessibility needs, or additional details..."
                class="form-textarea"
              ></textarea>
            </div>
  
            <!-- How did you hear about us -->
            <div>
              <label class="block text-sm font-medium text-neutral-700 mb-2">
                How did you hear about us?
              </label>
              <select v-model="formData.how_heard_about_us" class="form-select">
                <option value="">Select source</option>
                <option value="Google Search">Google Search</option>
                <option value="Social Media">Social Media</option>
                <option value="Word of Mouth">Word of Mouth</option>
                <option value="Referral">Referral from Friend</option>
                <option value="Previous Client">Previous Client</option>
                <option value="Advertisement">Advertisement</option>
                <option value="Other">Other</option>
              </select>
            </div>
  
            <!-- Terms and Marketing -->
            <div class="space-y-3">
              <label class="flex items-start space-x-3">
                <input
                  v-model="formData.terms_accepted"
                  type="checkbox"
                  required
                  class="mt-1 rounded border-neutral-300 text-primary-600 focus:ring-primary-500"
                />
                <span class="text-sm text-neutral-600">
                  I agree to the 
                  <a href="/terms" class="text-primary-600 hover:text-primary-700 underline" target="_blank">
                    Terms of Service
                  </a> 
                  and 
                  <a href="/privacy" class="text-primary-600 hover:text-primary-700 underline" target="_blank">
                    Privacy Policy
                  </a> *
                </span>
              </label>
              
              <label class="flex items-start space-x-3">
                <input
                  v-model="formData.marketing_consent"
                  type="checkbox"
                  class="mt-1 rounded border-neutral-300 text-primary-600 focus:ring-primary-500"
                />
                <span class="text-sm text-neutral-600">
                  I would like to receive marketing communications and event planning tips
                </span>
              </label>
            </div>
          </div>
        </div>
  
        <!-- Form Navigation -->
        <div class="flex justify-between items-center pt-8 border-t border-neutral-200">
          <button
            v-if="currentStep > 0"
            type="button"
            @click="previousStep"
            class="flex items-center space-x-2 px-6 py-3 border border-neutral-300 rounded-lg text-neutral-700 hover:bg-neutral-50 transition-colors"
          >
            <ChevronLeft class="w-4 h-4" />
            <span>Previous</span>
          </button>
          <div v-else></div>
  
          <button
            v-if="currentStep < steps.length - 1"
            type="button"
            @click="nextStep"
            :disabled="!isStepValid(currentStep)"
            class="flex items-center space-x-2 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <span>Next</span>
            <ChevronRight class="w-4 h-4" />
          </button>
          
          <button
            v-else
            type="submit"
            :disabled="isSubmitting || !isFormValid"
            class="flex items-center space-x-2 px-8 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 hover:shadow-lg"
          >
            <Loader v-if="isSubmitting" class="w-4 h-4 animate-spin" />
            <Calendar v-else class="w-4 h-4" />
            <span>{{ isSubmitting ? 'Submitting...' : 'Submit Booking Request' }}</span>
          </button>
        </div>
      </form>
  
      <!-- Success Message -->
      <div
        v-if="showSuccess"
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
        @click="showSuccess = false"
      >
        <div class="bg-white rounded-lg p-8 max-w-md mx-4 text-center">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Check class="w-8 h-8 text-green-600" />
          </div>
          <h3 class="text-xl font-semibold text-neutral-900 mb-2">
            Booking Request Submitted!
          </h3>
          <p class="text-neutral-600 mb-4">
            {{ successMessage }}
          </p>
          <button
            @click="showSuccess = false"
            class="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, reactive, computed, onMounted } from 'vue'
  import { 
    Check, 
    ChevronRight, 
    ChevronLeft, 
    Calendar, 
    Loader 
  } from 'lucide-vue-next'
  import { submitBooking, getBookingFormOptions } from '../../utils/api'
  import type { BookingCreate, BookingFormOptions } from '../../types/api'
  import { EventType, ContactMethod } from '../../types/api'
  
  // Form steps configuration
  const steps = [
    { id: 'details', title: 'Event Details' },
    { id: 'venue', title: 'Venue & Services' },
    { id: 'contact', title: 'Contact Info' }
  ]
  
  // Reactive state
  const currentStep = ref(0)
  const isSubmitting = ref(false)
  const showSuccess = ref(false)
  const successMessage = ref('')
  
  // Form options from API
  const eventTypes = ref([])
  const services = ref([])
  const contactMethods = ref([])
  const venueTypes = ref([])
  const timeSlots = ref([])
  
  // Selected services array
  const selectedServices = ref<string[]>([])
  
  // Form data
  const formData = reactive<BookingCreate>({
    event_type: '' as EventType,
    event_date: '',
    event_time: '',
    duration_hours: 6,
    guest_count: 0,
    venue_name: '',
    venue_address: '',
    venue_type: '',
    budget_min: undefined,
    budget_max: undefined,
    budget_flexible: true,
    services_needed: '',
    special_requirements: '',
    dietary_restrictions: '',
    accessibility_needs: '',
    contact_name: '',
    contact_email: '',
    contact_phone: '',
    preferred_contact: ContactMethod.EMAIL,
    how_heard_about_us: '',
    previous_client: false,
    marketing_consent: false,
    terms_accepted: false
  })
  
  // Form errors
  const errors = reactive({
    event_type: '',
    event_date: '',
    guest_count: '',
    contact_name: '',
    contact_email: ''
  })
  
  // Computed properties
  const minDate = computed(() => {
    const today = new Date()
    today.setDate(today.getDate() + 7) // Minimum 7 days advance
    return today.toISOString().split('T')[0]
  })
  
  const isFormValid = computed(() => {
    return formData.event_type && 
           formData.event_date && 
           formData.guest_count > 0 && 
           formData.contact_name && 
           formData.contact_email && 
           formData.terms_accepted
  })
  
  // Step validation
  const isStepValid = (step: number): boolean => {
    switch (step) {
      case 0:
        return !!(formData.event_type && formData.event_date && formData.guest_count > 0)
      case 1:
        return true // Venue & services are optional
      case 2:
        return !!(formData.contact_name && formData.contact_email && formData.terms_accepted)
      default:
        return false
    }
  }
  
  // Navigation methods
  const nextStep = () => {
    if (currentStep.value < steps.length - 1 && isStepValid(currentStep.value)) {
      currentStep.value++
    }
  }
  
  const previousStep = () => {
    if (currentStep.value > 0) {
      currentStep.value--
    }
  }
  
  // Form submission
  const handleSubmit = async () => {
    // Clear previous errors
    Object.keys(errors).forEach(key => {
      errors[key] = ''
    })
  
    // Update services string
    formData.services_needed = selectedServices.value.join(', ')
  
    // Validate form
    if (!validateForm()) {
      return
    }
  
    isSubmitting.value = true
  
    try {
      const response = await submitBooking(formData)
      
      if (response.data) {
        successMessage.value = response.data.message
        showSuccess.value = true
        resetForm()
      } else if (response.error) {
        alert(response.message || 'Failed to submit booking request')
      }
    } catch (error) {
      console.error('Submission error:', error)
      alert('An unexpected error occurred. Please try again.')
    } finally {
      isSubmitting.value = false
    }
  }
  
  // Form validation
  const validateForm = (): boolean => {
    let isValid = true
  
    if (!formData.event_type) {
      errors.event_type = 'Please select an event type'
      isValid = false
    }
  
    if (!formData.event_date) {
      errors.event_date = 'Please select an event date'
      isValid = false
    }
  
    if (!formData.guest_count || formData.guest_count < 1) {
      errors.guest_count = 'Please enter the number of guests'
      isValid = false
    }
  
    if (!formData.contact_name || formData.contact_name.length < 2) {
      errors.contact_name = 'Please enter your full name'
      isValid = false
    }
  
    if (!formData.contact_email || !/\S+@\S+\.\S+/.test(formData.contact_email)) {
      errors.contact_email = 'Please enter a valid email address'
      isValid = false
    }
  
    return isValid
  }
  
  // Reset form
  const resetForm = () => {
    currentStep.value = 0
    selectedServices.value = []
    Object.assign(formData, {
      event_type: '' as EventType,
      event_date: '',
      event_time: '',
      duration_hours: 6,
      guest_count: 0,
      venue_name: '',
      venue_address: '',
      venue_type: '',
      budget_min: undefined,
      budget_max: undefined,
      budget_flexible: true,
      services_needed: '',
      special_requirements: '',
      dietary_restrictions: '',
      accessibility_needs: '',
      contact_name: '',
      contact_email: '',
      contact_phone: '',
      preferred_contact: ContactMethod.EMAIL,
      how_heard_about_us: '',
      previous_client: false,
      marketing_consent: false,
      terms_accepted: false
    })
  }
  
  // Load form options
  const loadFormOptions = async () => {
    try {
      const options = await getBookingFormOptions()
      eventTypes.value = options.event_types
      services.value = options.services
      contactMethods.value = options.contact_methods
      venueTypes.value = options.venue_types
      timeSlots.value = options.time_slots
    } catch (error) {
      console.error('Failed to load form options:', error)
      // Use fallback data if API fails
      eventTypes.value = [
        { value: 'wedding', label: 'Wedding' },
        { value: 'corporate', label: 'Corporate Event' },
        { value: 'birthday', label: 'Birthday Party' },
        { value: 'other', label: 'Other' }
      ]
      contactMethods.value = [
        { value: 'email', label: 'Email' },
        { value: 'phone', label: 'Phone' },
        { value: 'either', label: 'Either' }
      ]
    }
  }
  
  // Lifecycle
  onMounted(() => {
    loadFormOptions()
  })
  </script>
  
  <style scoped>
  /* Form Input Styles */
  .form-input {
    @apply block w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors;
  }
  
  .form-select {
    @apply block w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors;
  }
  
  .form-textarea {
    @apply block w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors resize-none;
  }
  
  /* Validation States */
  .form-input:invalid,
  .form-select:invalid,
  .form-textarea:invalid {
    @apply border-red-300 focus:border-red-500 focus:ring-red-500;
  }
  
  .form-input:valid,
  .form-select:valid,
  .form-textarea:valid {
    @apply border-green-300 focus:border-green-500 focus:ring-green-500;
  }
  
  /* Animation Classes */
  .animate-fade-in-up {
    animation: fadeInUp 0.5s ease-out;
  }
  
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  /* Step Transition Effects */
  .step-enter-active,
  .step-leave-active {
    transition: all 0.3s ease;
  }
  
  .step-enter-from {
    opacity: 0;
    transform: translateX(30px);
  }
  
  .step-leave-to {
    opacity: 0;
    transform: translateX(-30px);
  }
  
  /* Progress Indicator Enhancements */
  .progress-step {
    transition: all 0.3s ease;
  }
  
  .progress-step.completed {
    transform: scale(1.1);
  }
  
  /* Button Hover Effects */
  button:hover:not(:disabled) {
    transform: translateY(-1px);
  }
  
  button:active:not(:disabled) {
    transform: translateY(0);
  }
  
  /* Checkbox and Radio Custom Styling */
  input[type="checkbox"]:checked {
    background-color: theme('colors.primary.600');
    border-color: theme('colors.primary.600');
  }
  
  input[type="checkbox"]:focus {
    ring-color: theme('colors.primary.500');
  }
  
  /* Error State Animations */
  .error-shake {
    animation: shake 0.5s ease-in-out;
  }
  
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
  }
  
  /* Success Modal Backdrop */
  .modal-backdrop {
    backdrop-filter: blur(4px);
  }
  
  /* Form Section Spacing */
  .form-section {
    margin-bottom: 2rem;
  }
  
  .form-section:last-child {
    margin-bottom: 0;
  }
  
  /* Loading State */
  .loading-overlay {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(2px);
  }
  
  /* Responsive Adjustments */
  @media (max-width: 768px) {
    .progress-indicator {
      overflow-x: auto;
      padding-bottom: 0.5rem;
    }
    
    .form-grid {
      grid-template-columns: 1fr;
    }
  }
  
  /* High Contrast Mode Support */
  @media (prefers-contrast: high) {
    .form-input,
    .form-select,
    .form-textarea {
      border-width: 2px;
    }
    
    .form-input:focus,
    .form-select:focus,
    .form-textarea:focus {
      outline: 2px solid;
      outline-offset: 2px;
    }
  }
  
  /* Reduced Motion Support */
  @media (prefers-reduced-motion: reduce) {
    .animate-fade-in-up,
    .step-enter-active,
    .step-leave-active,
    .progress-step {
      animation: none;
      transition: none;
    }
  }
  
  /* Print Styles */
  @media print {
    .form-navigation,
    .progress-indicator {
      display: none;
    }
    
    .form-input,
    .form-select,
    .form-textarea {
      border: 1px solid #000;
      background: white;
    }
  }
  </style>