/**
 * TypeScript types for API integration.
 * Matches the backend Pydantic schemas for type safety.
 */

// Enums matching backend models
export enum EventType {
    WEDDING = 'wedding',
    BIRTHDAY = 'birthday',
    CORPORATE = 'corporate',
    ANNIVERSARY = 'anniversary',
    GRADUATION = 'graduation',
    BABY_SHOWER = 'baby_shower',
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
  
  export interface BookingResponse {
    id: number
    event_type: EventType
    event_date: string
    event_time?: string
    duration_hours?: number
    guest_count: number
    venue_name?: string
    venue_address?: string
    venue_type?: string
    budget_min?: number
    budget_max?: number
    budget_flexible?: boolean
    services_needed?: string
    special_requirements?: string
    dietary_restrictions?: string
    accessibility_needs?: string
    contact_name: string
    contact_email: string
    contact_phone?: string
    preferred_contact: ContactMethod
    how_heard_about_us?: string
    previous_client?: boolean
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
  
  // Contact interfaces
  export interface ContactCreate {
    // Contact information
    name: string
    email: string
    phone?: string
    company?: string
    website?: string
    
    // Inquiry details
    subject: string
    message: string
    contact_type: ContactType
    
    // Preferences
    preferred_contact_time?: string
    timezone?: string
    
    // Marketing and source tracking
    source?: string
    is_newsletter_signup?: boolean
    
    // Terms and consent
    terms_accepted: boolean
    privacy_consent: boolean
    
    // Metadata
    referrer_url?: string
    user_agent?: string
  }
  
  export interface ContactResponse {
    id: number
    name: string
    email: string
    phone?: string
    company?: string
    website?: string
    subject: string
    message: string
    contact_type: ContactType
    preferred_contact_time?: string
    timezone?: string
    source?: string
    is_newsletter_signup: boolean
    status: ContactStatus
    priority: ContactPriority
    requires_follow_up: boolean
    is_spam: boolean
    created_at: string
    updated_at?: string
    replied_at?: string
    read_at?: string
  }
  
  export interface ContactConfirmation {
    success: boolean
    contact_id: number
    message: string
    reference_number: string
    estimated_response_time: string
  }
  
  // Form options interfaces
  export interface EventTypeOption {
    value: string
    label: string
    description?: string
  }
  
  export interface ServiceOption {
    id: string
    name: string
    description?: string
    base_price?: number
    is_popular?: boolean
  }
  
  export interface BookingFormOptions {
    event_types: EventTypeOption[]
    services: ServiceOption[]
    contact_methods: Array<{ value: string; label: string }>
    venue_types: string[]
    time_slots: string[]
    max_guest_count: number
    min_advance_days: number
  }
  
  export interface ContactFormOptions {
    contact_types: Array<{
      value: string
      label: string
      description: string
    }>
    sources: string[]
    timezones: Array<{ value: string; label: string }>
    preferred_times: string[]
    max_message_length: number
  }
  
  // API response interfaces
  export interface ApiResponse<T> {
    data?: T
    error?: string
    message?: string
  }
  
  export interface PaginatedResponse<T> {
    items: T[]
    total: number
    page: number
    per_page: number
    pages: number
    has_next: boolean
    has_prev: boolean
  }
  
  export interface ApiError {
    error: string
    message: string
    error_code?: string
    details?: Record<string, any>
  }
  
  // Statistics interfaces
  export interface BookingStats {
    total_bookings: number
    pending_bookings: number
    this_month_bookings: number
    priority_bookings: number
    avg_guest_count: number
    popular_event_types: Array<{ type: string; count: number }>
    monthly_trends: Array<{ month: string; count: number }>
  }
  
  export interface ContactStats {
    total_contacts: number
    new_contacts: number
    pending_replies: number
    this_month_contacts: number
    avg_response_time_hours: number
    contact_types_breakdown: Array<{ type: string; count: number }>
    monthly_trends: Array<{ month: string; count: number }>
    top_sources: Array<{ source: string; count: number }>
  }
  
  // Health check interfaces
  export interface HealthCheck {
    status: 'healthy' | 'unhealthy'
    timestamp: string
    service?: string
    version?: string
  }
  
  export interface DetailedHealthCheck extends HealthCheck {
    environment: string
    dependencies: {
      database: {
        status: 'healthy' | 'unhealthy'
        details?: any
      }
      email: {
        status: 'healthy' | 'unhealthy'
        smtp_host?: string
        smtp_port?: number
      }
    }
    system?: {
      cpu_percent: number
      memory_percent: number
      disk_percent: number
      platform: string
      python_version: string
    }
  }
  
  // Form validation interfaces
  export interface ValidationError {
    field: string
    message: string
    code?: string
  }
  
  export interface FormState<T> {
    data: T
    errors: Record<string, string>
    isSubmitting: boolean
    isValid: boolean
    touched: Record<string, boolean>
  }
  
  // Utility types
  export type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>
  export type OptionalFields<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>
  
  // API client configuration
  export interface ApiClientConfig {
    baseURL: string
    timeout: number
    headers: Record<string, string>
  }
  
  // Event interfaces for analytics
  export interface AnalyticsEvent {
    name: string
    properties?: Record<string, any>
    timestamp?: string
  }
  
  // Gallery interfaces
  export interface GalleryImage {
    id: string
    src: string
    alt: string
    title?: string
    description?: string
    category?: string
    thumbnail?: string
    width?: number
    height?: number
  }
  
  export interface GalleryCategory {
    id: string
    name: string
    description?: string
    image_count: number
  }
  
  // Pricing interfaces
  export interface PricingTier {
    id: string
    name: string
    description: string
    price: number
    currency: string
    features: string[]
    is_popular?: boolean
    is_custom?: boolean
  }
  
  export interface ServicePackage {
    id: string
    name: string
    description: string
    base_price: number
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