/**
 * TypeScript types for API integration.
 * Updated for UK event hire business packages.
 */

// Enums matching backend models
export enum EventType {
  WEDDING = 'wedding',
  BIRTHDAY = 'birthday',
  CORPORATE = 'corporate',
  ANNIVERSARY = 'anniversary',
  GRADUATION = 'graduation',
  BABY_SHOWER = 'baby_shower',
  GENDER_REVEAL = 'gender_reveal', // ✅ added
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
  PACKAGE_INQUIRY = 'package_inquiry', // ✅ new
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

// Booking interfaces
export interface BookingCreate {
  // Event details
  event_type: EventType
  event_date: string // ISO date string
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
  service_package_id?: string // ✅ allows selecting one of your packages
  special_requirements?: string
  dietary_restrictions?: string
  accessibility_needs?: string

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

export interface BookingResponse extends BookingCreate {
  id: number
  status: BookingStatus
  is_priority: boolean
  is_archived: boolean
  requires_consultation: boolean
  created_at: string
  updated_at?: string
  contacted_at?: string
  quoted_at?: string
}

export interface BookingConfirmation {
  success: boolean
  booking_id: number
  message: string
  confirmation_number: string
  next_steps: string[]
}

// Pricing interfaces
export interface PricingTier {
  id: string
  name: string
  description: string
  price: number
  currency: 'GBP'
  features: string[]
  is_popular?: boolean
  is_custom?: boolean
}

export interface ServicePackage {
  id: string
  name: string
  description: string
  base_price: number
  currency: 'GBP' // ✅
  included_services: string[]
  optional_services: Array<{
    name: string
    price: number
    description?: string
  }>
  max_guests?: number
  duration_hours?: number
  category: string
}
