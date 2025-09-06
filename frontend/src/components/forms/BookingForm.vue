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
                ? 'bg-brand-gold text-white shadow-lg' 
                : index === currentStep 
                  ? 'bg-brand-gold/20 text-brand-gold border-2 border-brand-gold' 
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

    <!-- Loading State - Remove this section -->

    <!-- Form -->
    <form @submit.prevent="handleSubmit" class="space-y-8">
      <!-- Error Alert -->
      <div v-if="globalError" class="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
        <AlertCircle class="w-5 h-5 text-red-600 mr-2 flex-shrink-0 mt-0.5" />
        <p class="text-red-700">{{ globalError }}</p>
      </div>

      <!-- Step 1: Event Details -->
      <div v-show="currentStep === 0" class="animate-fade-in-up">
        <div class="flex items-center mb-6">
          <div class="w-12 h-12 bg-brand-gold/10 rounded-full flex items-center justify-center mr-4">
            <Calendar class="w-6 h-6 text-brand-gold" />
          </div>
          <div>
            <h3 class="text-xl font-semibold text-neutral-900">Event Details</h3>
            <p class="text-sm text-neutral-600">Tell us about your special occasion</p>
          </div>
        </div>
        
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
                :title="eventType.description"
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
              Preferred Time
            </label>
            <select
              v-model="formData.event_time"
              class="form-select"
            >
              <option value="">Select time (optional)</option>
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
              :max="maxGuestCount"
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
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-neutral-700 mb-2">
              Event Duration (hours)
            </label>
            <input
              v-model.number="formData.duration_hours"
              type="number"
              min="1"
              max="24"
              placeholder="e.g., 6"
              class="form-input max-w-xs"
            />
            <p class="text-xs text-neutral-500 mt-1">How long do you expect your event to last?</p>
          </div>

          <!-- Event Type Suggestions -->
          <div v-if="selectedEventConfig" class="md:col-span-2 bg-brand-gold/5 rounded-lg p-4 border border-brand-gold/20">
            <div class="flex items-center mb-2">
              <span class="text-lg mr-2">{{ selectedEventConfig.icon }}</span>
              <h4 class="font-medium text-neutral-900">{{ selectedEventConfig.label }} Suggestions</h4>
            </div>
            <div class="text-sm text-neutral-600 space-y-1">
              <p><strong>Typical Duration:</strong> {{ selectedEventConfig.avgDuration }} hours</p>
              <p><strong>Guest Range:</strong> {{ selectedEventConfig.minGuests }} - {{ selectedEventConfig.maxGuests }} guests</p>
              <p v-if="suggestedServices.length > 0">
                <strong>Popular Services:</strong> {{ suggestedServices.join(', ') }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 2: Venue & Services -->
      <div v-show="currentStep === 1" class="animate-fade-in-up">
        <div class="flex items-center mb-6">
          <div class="w-12 h-12 bg-brand-gold/10 rounded-full flex items-center justify-center mr-4">
            <MapPin class="w-6 h-6 text-brand-gold" />
          </div>
          <div>
            <h3 class="text-xl font-semibold text-neutral-900">Venue & Services</h3>
            <p class="text-sm text-neutral-600">Location details and service requirements</p>
          </div>
        </div>
        
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
              placeholder="Full venue address (if known)"
              class="form-textarea"
            ></textarea>
          </div>

          <!-- Services Needed -->
          <div v-if="services.length > 0">
            <label class="block text-sm font-medium text-neutral-700 mb-3">
              Services Needed
            </label>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              <label
                v-for="service in services"
                :key="service.id"
                class="flex items-center space-x-2 cursor-pointer p-3 border border-neutral-200 rounded-lg hover:bg-neutral-50 transition-colors"
                :class="{ 'border-brand-gold bg-brand-gold/5': selectedServices.includes(service.name) }"
              >
                <input
                  type="checkbox"
                  :value="service.name"
                  v-model="selectedServices"
                  class="rounded border-neutral-300 text-brand-gold focus:ring-brand-gold"
                />
                <div class="flex-1 min-w-0">
                  <span class="text-sm font-medium text-neutral-700">{{ service.name }}</span>
                  <div v-if="service.description" class="text-xs text-neutral-500 mt-1">
                    {{ service.description }}
                  </div>
                  <div v-if="service.base_price" class="text-xs text-brand-gold font-medium mt-1">
                    From £{{ service.base_price }}
                    <span v-if="service.id === 'led-numbers'" class="text-neutral-500">per number (24hrs)</span>
                  </div>
                  <div v-if="service.is_popular" class="text-xs text-brand-gold font-bold mt-1">
                    ⭐ Popular Choice
                  </div>
                </div>
              </label>
            </div>
          </div>

          <!-- Budget Range -->
          <div>
            <label class="block text-sm font-medium text-neutral-700 mb-3">
              Budget Range (£)
            </label>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <input
                  v-model.number="formData.budget_min"
                  type="number"
                  min="0"
                  step="50"
                  placeholder="Minimum budget"
                  class="form-input"
                />
              </div>
              <div>
                <input
                  v-model.number="formData.budget_max"
                  type="number"
                  min="0"
                  step="50"
                  placeholder="Maximum budget"
                  class="form-input"
                  :class="{ 'border-red-500': errors.budget_max }"
                />
                <p v-if="errors.budget_max" class="text-red-500 text-sm mt-1">
                  {{ errors.budget_max }}
                </p>
              </div>
            </div>
            <div class="mt-2">
              <label class="flex items-center space-x-2">
                <input
                  v-model="formData.budget_flexible"
                  type="checkbox"
                  class="rounded border-neutral-300 text-brand-gold focus:ring-brand-gold"
                />
                <span class="text-sm text-neutral-600">Budget is flexible</span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 3: Contact & Details -->
      <div v-show="currentStep === 2" class="animate-fade-in-up">
        <div class="flex items-center mb-6">
          <div class="w-12 h-12 bg-brand-gold/10 rounded-full flex items-center justify-center mr-4">
            <User class="w-6 h-6 text-brand-gold" />
          </div>
          <div>
            <h3 class="text-xl font-semibold text-neutral-900">Contact Information</h3>
            <p class="text-sm text-neutral-600">How can we reach you?</p>
          </div>
        </div>
        
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
                placeholder="e.g., 07123 456789 or +44 1908 123456"
                class="form-input"
                :class="{ 'border-red-500': errors.contact_phone }"
              />
              <p v-if="errors.contact_phone" class="text-red-500 text-sm mt-1">
                {{ errors.contact_phone }}
              </p>
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
              <option value="Social Media - Instagram">Social Media - Instagram</option>
              <option value="Social Media - Facebook">Social Media - Facebook</option>
              <option value="Word of Mouth">Word of Mouth</option>
              <option value="Referral from Friend">Referral from Friend</option>
              <option value="Previous Client">Previous Client</option>
              <option value="Local Advertisement">Local Advertisement</option>
              <option value="Wedding Fair/Event">Wedding Fair/Event</option>
              <option value="Milton Keynes Local Directory">Milton Keynes Local Directory</option>
              <option value="Venue Recommendation">Venue Recommendation</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <!-- Previous Client Check -->
          <div>
            <label class="flex items-center space-x-2">
              <input
                v-model="formData.previous_client"
                type="checkbox"
                class="rounded border-neutral-300 text-brand-gold focus:ring-brand-gold"
              />
              <span class="text-sm text-neutral-600">I'm a returning client</span>
            </label>
          </div>

          <!-- Terms and Marketing -->
          <div class="space-y-3 pt-4 border-t border-neutral-200">
            <label class="flex items-start space-x-3">
              <input
                v-model="formData.terms_accepted"
                type="checkbox"
                required
                class="mt-1 rounded border-neutral-300 text-brand-gold focus:ring-brand-gold"
                :class="{ 'border-red-500': errors.terms_accepted }"
              />
              <span class="text-sm text-neutral-600">
                I agree to the 
                <a href="/terms" class="text-brand-gold hover:text-primary-700 underline" target="_blank">
                  Terms of Service
                </a> 
                and 
                <a href="/privacy" class="text-brand-gold hover:text-primary-700 underline" target="_blank">
                  Privacy Policy
                </a> *
              </span>
            </label>
            <p v-if="errors.terms_accepted" class="text-red-500 text-sm ml-6">
              {{ errors.terms_accepted }}
            </p>
            
            <label class="flex items-start space-x-3">
              <input
                v-model="formData.marketing_consent"
                type="checkbox"
                class="mt-1 rounded border-neutral-300 text-brand-gold focus:ring-brand-gold"
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
          class="flex items-center space-x-2 px-6 py-3 bg-brand-gold text-white rounded-lg hover:bg-brand-gold/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 hover:shadow-lg transform hover:-translate-y-0.5"
        >
          <span>Next</span>
          <ChevronRight class="w-4 h-4" />
        </button>
        
        <button
          v-else
          type="submit"
          :disabled="isSubmitting || !isFormValid"
          class="flex items-center space-x-2 px-8 py-3 bg-gradient-to-r from-brand-gold to-primary-600 text-white rounded-lg hover:from-brand-gold/90 hover:to-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 hover:shadow-lg transform hover:-translate-y-0.5"
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
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      @click="closeSuccess"
    >
      <div class="bg-white rounded-2xl p-8 max-w-md w-full text-center shadow-2xl transform scale-100 opacity-100 transition-all duration-300">
        <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <Check class="w-10 h-10 text-green-600" />
        </div>
        <h3 class="text-2xl font-bold text-neutral-900 mb-4">
          Booking Request Submitted!
        </h3>
        <div v-if="confirmationData" class="mb-6">
          <p class="text-neutral-600 mb-4">
            {{ confirmationData.message }}
          </p>
          <div class="bg-neutral-50 rounded-lg p-4 mb-4">
            <p class="text-sm text-neutral-700">
              <strong>Confirmation Number:</strong> {{ confirmationData.confirmation_number }}
            </p>
          </div>
          <div class="text-left">
            <h4 class="font-semibold text-neutral-900 mb-2">Next Steps:</h4>
            <ul class="text-sm text-neutral-600 space-y-1">
              <li v-for="(step, index) in confirmationData.next_steps" :key="index" class="flex items-start">
                <span class="flex-shrink-0 w-5 h-5 bg-brand-gold/20 text-brand-gold rounded-full flex items-center justify-center text-xs font-medium mr-2 mt-0.5">
                  {{ index + 1 }}
                </span>
                {{ step }}
              </li>
            </ul>
          </div>
        </div>
        <div class="space-y-3">
          <button
            @click="closeSuccess"
            class="w-full bg-brand-gold text-white px-6 py-3 rounded-lg hover:bg-brand-gold/90 transition-colors font-medium"
          >
            Close
          </button>
          <button
            @click="resetForm"
            class="w-full border border-neutral-300 text-neutral-700 px-6 py-3 rounded-lg hover:bg-neutral-50 transition-colors"
          >
            Submit Another Booking
          </button>
        </div>
      </div>
    </div>

    <!-- Enhanced Error Modal -->
    <div v-if="showErrorModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-8 max-w-md w-full shadow-2xl">
        <h3 class="text-xl font-bold mb-4" :class="{
          'text-red-600': errorModalOptions?.type === 'error',
          'text-amber-600': errorModalOptions?.type === 'warning',
          'text-blue-600': errorModalOptions?.type === 'info'
        }">
          {{ errorModalOptions?.title }}
        </h3>
        
        <div class="mb-6 text-gray-700 whitespace-pre-line">
          {{ errorModalOptions?.message }}
        </div>
        
        <div class="space-y-2">
          <button
            v-for="action in errorModalOptions?.actions"
            :key="action.text"
            @click="action.action(); closeErrorModal()"
            class="w-full px-4 py-2 rounded-lg font-medium transition-colors"
            :class="{
              'bg-brand-gold text-white hover:bg-brand-gold/90': action.is_primary,
              'border border-gray-300 text-gray-700 hover:bg-gray-50': !action.is_primary
            }"
          >
            {{ action.text }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch, onBeforeUnmount } from 'vue'
import { 
  Check, 
  ChevronRight, 
  ChevronLeft, 
  Calendar, 
  Loader,
  MapPin,
  User,
  AlertCircle
} from 'lucide-vue-next'
import { submitBooking } from '../../utils/api'
import type { BookingCreate, BookingConfirmation } from '../../types/api'
import { EventType, ContactMethod } from '../../types/api'
import { EVENT_TYPE_CONFIG, SERVICES, VALIDATION_RULES, BUSINESS_INFO } from '../../utils/constants'

const showErrorModal = ref(false)
const errorModalOptions = ref<any>(null)

const closeErrorModal = () => {
  showErrorModal.value = false
  errorModalOptions.value = null
  globalError.value = ''
}


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
const globalError = ref('')
const confirmationData = ref<BookingConfirmation | null>(null)

// Form options using constants directly (no API fetching needed)
const eventTypes = computed(() => 
  Object.values(EventType).map(eventType => ({
    value: eventType,
    label: EVENT_TYPE_CONFIG[eventType]?.label || eventType,
    description: EVENT_TYPE_CONFIG[eventType]?.description || ''
  }))
)

const services = computed(() => 
  SERVICES.map(service => ({
    id: service.id,
    name: service.name,
    description: service.description,
    base_price: service.basePrice || (service as any).price,
    is_popular: service.popular || false
  }))
)

const contactMethods = ref([
  { value: ContactMethod.EMAIL, label: 'Email' },
  { value: ContactMethod.PHONE, label: 'Phone' },
  { value: ContactMethod.EITHER, label: 'Either Email or Phone' }
])

const venueTypes = ref([
  'Indoor Venue', 'Outdoor Venue', 'Garden', 'Marquee', 'Church', 'Village Hall', 
  'Hotel', 'Restaurant', 'Private Residence', 'Community Centre', 
  'Barn', 'Country House', 'Registry Office', 'Other'
])

const timeSlots = ref([
  '9:00 AM', '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM',
  '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM', '2:00 PM', '2:30 PM',
  '3:00 PM', '3:30 PM', '4:00 PM', '4:30 PM', '5:00 PM', '5:30 PM',
  '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM',
  '9:00 PM', '9:30 PM', '10:00 PM'
])

const maxGuestCount = ref(VALIDATION_RULES.guestCount.max)
const minAdvanceDays = ref(0)

// Selected services array
const selectedServices = ref<string[]>([])

// Form data with proper typing
const formData = reactive<Partial<BookingCreate>>({
  event_type: '' as any, // Use empty string instead of undefined
  event_date: '',
  event_time: '',
  duration_hours: 6,
  guest_count: null as any,
  venue_name: '',
  venue_address: '',
  venue_type: '',
  budget_min: null as any,
  budget_max: null as any,
  budget_flexible: true,
  services_needed: '',
  special_requirements: '',
  contact_name: '',
  contact_email: '',
  contact_phone: '',
  preferred_contact: ContactMethod.EMAIL,
  how_heard_about_us: '',
  previous_client: false,
  marketing_consent: false,
  terms_accepted: false
})

// Computed property for event type suggestions
const selectedEventConfig = computed(() => {
  if (!formData.event_type || formData.event_type === '') return null
  
  // Make sure the event_type exists in the config
  const eventType = formData.event_type as EventType
  return EVENT_TYPE_CONFIG[eventType] || null
})

// Suggested services based on event type
const suggestedServices = computed(() => {
  if (!formData.event_type) return []
  
  const eventType = formData.event_type as EventType
  
  switch (eventType) {
    case EventType.BIRTHDAY:
      return ['4FT LED Number Hire', 'Birthday Package', 'Balloon Arch']
    case EventType.WEDDING:
      return ['Wedding Package', 'Shimmer Wall', 'LED Neon Signs', 'Artificial Florals']
    case EventType.BABY_SHOWER:
      return ['Baby Shower Package', 'Balloon Arch', 'LED Neon Signs']
      case EventType.GENDER_REVEAL:
      return ['Gender Reveal Package', 'Balloon Arch', 'LED Neon Signs']
    case EventType.ENGAGEMENT:
      return ['Engagement Package', 'LED Neon Signs', 'Artificial Florals']
    case EventType.ANNIVERSARY:
      return ['4FT LED Number Hire', 'Shimmer Wall', 'LED Neon Signs']
    case EventType.CORPORATE:
      return ['LED Neon Signs', 'Backdrop Decorations']
    default:
      return []
  }
})

// Form errors
const errors = reactive<Record<string, string>>({})

// Watch selectedServices to update services_needed
watch(selectedServices, (newServices) => {
  formData.services_needed = newServices.join(', ')
}, { deep: true })

// Computed properties
const minDate = computed(() => {
  const today = new Date()
  today.setDate(today.getDate() + minAdvanceDays.value)
  return today.toISOString().split('T')[0]
})

const isFormValid = computed(() => {
  return formData.event_type && 
         formData.event_date && 
         formData.guest_count && 
         formData.guest_count > 0 && 
         formData.contact_name && 
         formData.contact_email && 
         formData.terms_accepted
})

// Step validation
const isStepValid = (step: number): boolean => {
  switch (step) {
    case 0:
      return !!(formData.event_type && formData.event_date && formData.guest_count && formData.guest_count > 0)
    case 1:
      return true // Venue & services are optional
    case 2:
      return !!(formData.contact_name && formData.contact_email && formData.terms_accepted)
    default:
      return false
  }
}

// Clear errors when fields change
const clearFieldError = (field: string) => {
  if (errors[field]) {
    delete errors[field]
  }
}

// Navigation methods
const nextStep = () => {
  clearErrors()
  if (validateCurrentStep() && currentStep.value < steps.length - 1) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// Validation methods
const validateCurrentStep = (): boolean => {
  switch (currentStep.value) {
    case 0:
      return validateEventDetails()
    case 1:
      return validateVenueServices()
    case 2:
      return validateContact()
    default:
      return true
  }
}

const validateEventDetails = (): boolean => {
  let isValid = true

  if (!formData.event_type) {
    errors.event_type = 'Please select an event type'
    isValid = false
  }

  if (!formData.event_date) {
    errors.event_date = 'Please select an event date'
    isValid = false
  } else {
    const eventDate = new Date(formData.event_date)
    const minDate = new Date()
    minDate.setDate(minDate.getDate() + minAdvanceDays.value)
    if (eventDate < minDate) {
      errors.event_date = `Event date must be at least ${minAdvanceDays.value} days in advance`
      isValid = false
    }
  }

  if (!formData.guest_count || formData.guest_count < VALIDATION_RULES.guestCount.min) {
    errors.guest_count = 'Please enter the number of guests'
    isValid = false
  } else if (formData.guest_count > maxGuestCount.value) {
    errors.guest_count = `Maximum guest count is ${maxGuestCount.value}`
    isValid = false
  }

  return isValid
}

const validateVenueServices = (): boolean => {
  let isValid = true

  // Budget validation using validation rules
  if (formData.budget_min && (formData.budget_min < VALIDATION_RULES.budget.min || formData.budget_min > VALIDATION_RULES.budget.max)) {
    errors.budget_min = `Budget must be between £${VALIDATION_RULES.budget.min} and £${VALIDATION_RULES.budget.max}`
    isValid = false
  }
  
  if (formData.budget_max && (formData.budget_max < VALIDATION_RULES.budget.min || formData.budget_max > VALIDATION_RULES.budget.max)) {
    errors.budget_max = `Budget must be between £${VALIDATION_RULES.budget.min} and £${VALIDATION_RULES.budget.max}`
    isValid = false
  }
  
  if (formData.budget_min && formData.budget_max) {
    if (formData.budget_max < formData.budget_min) {
      errors.budget_max = 'Maximum budget must be greater than minimum budget'
      isValid = false
    }
  }

  return isValid
}

const validateContact = (): boolean => {
  let isValid = true

  if (!formData.contact_name || formData.contact_name.length < VALIDATION_RULES.name.minLength) {
    errors.contact_name = `Name must be at least ${VALIDATION_RULES.name.minLength} characters`
    isValid = false
  } else if (formData.contact_name.length > VALIDATION_RULES.name.maxLength) {
    errors.contact_name = `Name must be less than ${VALIDATION_RULES.name.maxLength} characters`
    isValid = false
  } else if (!VALIDATION_RULES.name.pattern.test(formData.contact_name)) {
    errors.contact_name = 'Name can only contain letters, spaces, hyphens, apostrophes, and periods'
    isValid = false
  }

  if (!formData.contact_email) {
    errors.contact_email = 'Please enter your email address'
    isValid = false
  } else if (!VALIDATION_RULES.email.pattern.test(formData.contact_email)) {
    errors.contact_email = 'Please enter a valid email address'
    isValid = false
  }

  // Phone validation (if provided) using validation rules
  if (formData.contact_phone && formData.contact_phone.trim()) {
    if (!VALIDATION_RULES.phone.pattern.test(formData.contact_phone.replace(/\s/g, ''))) {
      errors.contact_phone = 'Please enter a valid phone number'
      isValid = false
    }
  }

  if (!formData.terms_accepted) {
    errors.terms_accepted = 'You must accept the terms and conditions'
    isValid = false
  }

  return isValid
}

const clearErrors = () => {
  Object.keys(errors).forEach(key => delete errors[key])
}

// Form submission
const handleSubmit = async () => {
  clearErrors()
  globalError.value = ''

  if (!validateContact()) {
    return
  }

  isSubmitting.value = true

  try {
    const bookingData: BookingCreate = {
      event_type: formData.event_type as EventType,
      event_date: formData.event_date!,
      event_time: formData.event_time || undefined,
      duration_hours: formData.duration_hours || 6,
      guest_count: formData.guest_count!,
      venue_name: formData.venue_name || undefined,
      venue_address: formData.venue_address || undefined,
      venue_type: formData.venue_type || undefined,
      budget_min: formData.budget_min || undefined,
      budget_max: formData.budget_max || undefined,
      budget_flexible: formData.budget_flexible ?? true,
      services_needed: formData.services_needed || undefined,
      special_requirements: formData.special_requirements || undefined,
      contact_name: formData.contact_name!.trim(),
      contact_email: formData.contact_email!.toLowerCase().trim(),
      contact_phone: formData.contact_phone?.trim() || undefined,
      preferred_contact: formData.preferred_contact as ContactMethod || ContactMethod.EMAIL,
      how_heard_about_us: formData.how_heard_about_us || undefined,
      previous_client: formData.previous_client ?? false,
      marketing_consent: formData.marketing_consent ?? false,
      terms_accepted: formData.terms_accepted!
    }

    console.log('Submitting booking data:', bookingData)

    const response = await submitBooking(bookingData)
    
    if (response.data) {
      confirmationData.value = response.data
      showSuccess.value = true
} else if (response.error) {
  // Check for duplicate booking
  const isDuplicate = 
    response.status === 409 || 
    response.errorDetails?.error_code === 'DUPLICATE_BOOKING' ||
    (response.errorDetails?.error_code === 'VALIDATION_ERROR' && 
      response.errorDetails?.message?.includes('booking inquiry from you for'))
  
  if (isDuplicate) {
    console.log('Setting duplicate modal via general error modal...')
    
    // Use the general error modal for duplicate bookings
    errorModalOptions.value = {
      title: 'Booking Already Exists',
      message: response.errorDetails['detail'].message,
      type: 'info',
      actions: [
        {
          text: 'Close',
          action: () => {
            // This will be handled by the modal's closeErrorModal()
          },
          is_primary: false
        }
      ]
    }
    showErrorModal.value = true
    
  } else {
    // Handle other errors with the general modal
    errorModalOptions.value = {
      title: 'Booking Error',
      message: response.errorDetails?.message || response.message,
      type: 'error',
      actions: [
        {
          text: 'Try Again',
          action: () => {
            // Retry the submission
            handleSubmit()
          },
          is_primary: true
        },
        {
          text: 'Close',
          action: () => {
            // This will be handled by closeErrorModal()
          },
          is_primary: false
        }
      ]
    }
    showErrorModal.value = true
  }
} else {
  globalError.value = response.message || 'An unknown error occurred. Please try again.'
}
  } catch (error: any) {
    console.error('Submission error:', error)
    
    // Handle network errors or unexpected errors
    if (error.response) {
      // This is an HTTP error response
      const errorData = error.response.data
      
      if (error.response.status === 409 && errorData?.error_code === 'DUPLICATE_BOOKING') {
        errorModalOptions.value.message = errorData.message
        showDuplicateModal.value = true
      } else {
        globalError.value = errorData?.message || error.message || 'An error occurred'
      }
    } else {
      // Network error or other unexpected error
      globalError.value = error.message || 'An unexpected error occurred. Please try again.'
    }
  } finally {
    isSubmitting.value = false
  }
}

// Add this listener for form reset events
onMounted(() => {
  document.addEventListener('booking-form-reset', resetForm)
})

onBeforeUnmount(() => {
  document.removeEventListener('booking-form-reset', resetForm)
})
// Success handling
const closeSuccess = () => {
  showSuccess.value = false
}

const resetForm = () => {
  showSuccess.value = false
  confirmationData.value = null
  currentStep.value = 0
  selectedServices.value = []
  clearErrors()
  globalError.value = ''
  
  // Reset form data with proper types
  Object.assign(formData, {
    event_type: '',
    event_date: '',
    event_time: '',
    duration_hours: 6,
    guest_count: null,
    venue_name: '',
    venue_address: '',
    venue_type: '',
    budget_min: null,
    budget_max: null,
    budget_flexible: true,
    services_needed: '',
    special_requirements: '',
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

// Watch for form field changes to clear errors
watch(() => formData.event_type, () => clearFieldError('event_type'))
watch(() => formData.event_date, () => clearFieldError('event_date'))
watch(() => formData.guest_count, () => clearFieldError('guest_count'))
watch(() => formData.contact_name, () => clearFieldError('contact_name'))
watch(() => formData.contact_email, () => clearFieldError('contact_email'))
watch(() => formData.contact_phone, () => clearFieldError('contact_phone'))
watch(() => formData.terms_accepted, () => clearFieldError('terms_accepted'))
watch(() => formData.budget_max, () => clearFieldError('budget_max'))
</script>

<style scoped>
/* Form Input Styles - Updated to use brand-gold instead of primary */
.form-input {
  @apply block w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-brand-gold focus:border-brand-gold transition-colors;
}

.form-select {
  @apply block w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-brand-gold focus:border-brand-gold transition-colors;
}

.form-textarea {
  @apply block w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-brand-gold focus:border-brand-gold transition-colors resize-none;
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

/* Button Hover Effects */
button:hover:not(:disabled) {
  transform: translateY(-1px);
}

button:active:not(:disabled) {
  transform: translateY(0);
}

/* Checkbox and Radio Custom Styling */
input[type="checkbox"]:checked {
  background-color: theme('colors.brand.gold');
  border-color: theme('colors.brand.gold');
}

input[type="checkbox"]:focus {
  ring-color: theme('colors.brand.gold');
}

/* Service selection cards */
.service-card {
  transition: all 0.2s ease;
}

.service-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Success modal animation */
.modal-enter-active {
  transition: all 0.3s ease;
}

.modal-enter-from {
  opacity: 0;
  transform: scale(0.9);
}

/* Loading overlay */
.loading-overlay {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
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
  button {
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

/* Brand gold color utilities */
.text-brand-gold {
  color: theme('colors.brand.gold');
}

.bg-brand-gold {
  background-color: theme('colors.brand.gold');
}

.border-brand-gold {
  border-color: theme('colors.brand.gold');
}

.ring-brand-gold {
  --tw-ring-color: theme('colors.brand.gold');
}

.focus\:ring-brand-gold:focus {
  --tw-ring-color: theme('colors.brand.gold');
}

.focus\:border-brand-gold:focus {
  border-color: theme('colors.brand.gold');
}
</style>
