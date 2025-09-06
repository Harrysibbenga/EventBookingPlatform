/**
 * TypeScript types for API integration.
 * Only includes types required by the API client.
 */

// ==============================================
// ENUMS
// ==============================================

export enum EventType {
  WEDDING = 'wedding',
  BIRTHDAY = 'birthday',
  CORPORATE = 'corporate',
  ANNIVERSARY = 'anniversary',
  GRADUATION = 'graduation',
  BABY_SHOWER = 'baby_shower',
  GENDER_REVEAL = 'gender_reveal',
  ENGAGEMENT = 'engagement',
  RETIREMENT = 'retirement',
  HOLIDAY = 'holiday',
  OTHER = 'other'
}

export enum BookingStatus {
  PENDING = 'pending',
  REVIEWED = 'reviewed',
  CONTACTED = 'contacted',
  QUOTED = 'quoted',
  CONFIRMED = 'confirmed',
  CANCELLED = 'cancelled',
  COMPLETED = 'completed'
}

export enum ContactMethod {
  EMAIL = 'email',
  PHONE = 'phone',
  EITHER = 'either'
}

export enum ContactType {
  GENERAL = 'general',
  PRICING = 'pricing',
  AVAILABILITY = 'availability',
  SERVICES = 'services',
  PARTNERSHIP = 'partnership',
  FEEDBACK = 'feedback',
  COMPLAINT = 'complaint',
  OTHER = 'other'
}

export enum ContactStatus {
  NEW = 'new',
  READ = 'read',
  REPLIED = 'replied',
  RESOLVED = 'resolved',
  ARCHIVED = 'archived'
}

export enum ContactPriority {
  LOW = 'low',
  NORMAL = 'normal',
  HIGH = 'high',
  URGENT = 'urgent'
}

// ==============================================
// BOOKING INTERFACES
// ==============================================

export interface BookingCreate {
  // Event details
  event_type: EventType
  event_date: string
  event_time?: string
  duration_hours?: number
  guest_count: number

  // Venue information
  venue_name?: string
  venue_address?: string
  venue_type?: string

  // Budget information
  budget_min?: number
  budget_max?: number
  budget_flexible?: boolean

  // Services and requirements
  services_needed?: string
  service_package_id?: string
  special_requirements?: string


  // Contact information
  contact_name: string
  contact_email: string
  contact_phone?: string
  preferred_contact: ContactMethod

  // Additional information
  how_heard_about_us?: string
  previous_client?: boolean

  // Terms and consent
  marketing_consent?: boolean
  terms_accepted: boolean
}

export interface BookingResponse extends Omit<BookingCreate, 'terms_accepted' | 'marketing_consent'> {
  id: number
  status: BookingStatus
  is_priority: boolean
  is_archived: boolean
  requires_consultation: boolean
  created_at: string
  updated_at?: string
  contacted_at?: string
  quoted_at?: string
  admin_notes?: string
  estimated_quote?: number
  follow_up_date?: string
}

export interface BookingConfirmation {
  success: boolean
  booking_id: number
  message: string
  confirmation_number: string
  next_steps: string[]
}

export interface BookingFormOptions {
  event_types: Array<{
    value: string
    label: string
    description?: string
  }>
  services: Array<{
    id: string
    name: string
    description?: string
    base_price?: number
    is_popular: boolean
  }>
  contact_methods: Array<{
    value: string
    label: string
  }>
  venue_types: string[]
  time_slots: string[]
  max_guest_count: number
  min_advance_days: number
}

// ==============================================
// CONTACT INTERFACES
// ==============================================

export interface ContactCreate {
  contact_name: string
  contact_email: string
  contact_phone?: string
  preferred_contact?: ContactMethod
  contact_type: ContactType
  subject: string
  message: string
  company_name?: string
  website?: string
  event_date?: string
  estimated_guest_count?: number
  estimated_budget?: number
  preferred_response_time?: string
  timezone?: string
  source?: string
  marketing_consent?: boolean
  urgent?: boolean
}

export interface ContactResponse extends ContactCreate {
  id: number
  status: ContactStatus
  priority: ContactPriority
  is_spam: boolean
  requires_follow_up: boolean
  created_at: string
  updated_at?: string
  replied_at?: string
  resolved_at?: string
  admin_notes?: string
  assigned_to?: string
  tags?: string[]
  follow_up_date?: string
  response_time_hours?: number
}

export interface ContactConfirmation {
  success: boolean
  contact_id: number
  message: string
  reference_number: string
  estimated_response_time: string
}

export interface ContactFormOptions {
  contact_types: Array<{
    value: string
    label: string
    description: string
  }>
  sources: string[]
  timezones: Array<{
    value: string
    label: string
  }>
  preferred_times: string[]
  max_message_length: number
}

// ==============================================
// HEALTH CHECK INTERFACES
// ==============================================

export interface HealthCheck {
  healthy: boolean
  timestamp: string
}

export interface DetailedHealthCheck {
  healthy: boolean
  timestamp: string
  database: boolean
  email: boolean
  version?: string
  uptime?: number
}

// ==============================================
// API RESPONSE INTERFACES
// ==============================================

export interface ApiResponse<T> {
  data?: T
  error?: string
  message?: string
}

export interface ApiError {
  error: string
  message: string
  details?: {
    validation_errors?: Array<{
      field: string
      message: string
    }>
  }
}