/**
 * Application constants and configuration values.
 * Centralized location for all static data and settings.
 */

import { EventType, ContactType } from '../types/api'

// ========================================
// BUSINESS INFORMATION
// ========================================

export const BUSINESS_INFO = {
  name: 'Elite Event Productions',
  tagline: 'Creating Unforgettable Moments',
  description: 'Professional event planning and production services for weddings, corporate events, and special celebrations.',
  
  // Contact information
  email: 'hello@eliteeventproductions.com',
  phone: '+1 (555) 123-4567',
  address: {
    street: '123 Event Plaza',
    city: 'Los Angeles',
    state: 'CA',
    zip: '90210',
    country: 'United States'
  },
  
  // Business hours
  hours: {
    monday: '9:00 AM - 6:00 PM',
    tuesday: '9:00 AM - 6:00 PM',
    wednesday: '9:00 AM - 6:00 PM',
    thursday: '9:00 AM - 6:00 PM',
    friday: '9:00 AM - 6:00 PM',
    saturday: '10:00 AM - 4:00 PM',
    sunday: 'By Appointment Only'
  },
  
  // Social media
  social: {
    instagram: 'https://instagram.com/eliteeventproductions',
    facebook: 'https://facebook.com/eliteeventproductions',
    twitter: 'https://twitter.com/eliteeventprod',
    linkedin: 'https://linkedin.com/company/elite-event-productions',
    pinterest: 'https://pinterest.com/eliteeventprod'
  },
  
  // Founded year
  founded: 2015,
  
  // Service areas
  serviceAreas: [
    'Los Angeles County',
    'Orange County',
    'Ventura County',
    'Riverside County',
    'San Bernardino County'
  ]
} as const

// ========================================
// EVENT TYPES CONFIGURATION
// ========================================

export const EVENT_TYPE_CONFIG = {
  [EventType.WEDDING]: {
    label: 'Wedding',
    description: 'Ceremonies, receptions, and wedding celebrations',
    icon: '💒',
    color: 'primary',
    minGuests: 20,
    maxGuests: 500,
    avgDuration: 8,
    basePrice: 2500,
    popular: true
  },
  [EventType.CORPORATE]: {
    label: 'Corporate Event',
    description: 'Business meetings, conferences, and company events',
    icon: '🏢',
    color: 'secondary',
    minGuests: 10,
    maxGuests: 1000,
    avgDuration: 6,
    basePrice: 1800,
    popular: true
  },
  [EventType.BIRTHDAY]: {
    label: 'Birthday Party',
    description: 'Birthday celebrations and milestone parties',
    icon: '🎂',
    color: 'accent',
    minGuests: 5,
    maxGuests: 200,
    avgDuration: 4,
    basePrice: 800,
    popular: true
  },
  [EventType.ANNIVERSARY]: {
    label: 'Anniversary',
    description: 'Wedding anniversaries and milestone celebrations',
    icon: '💕',
    color: 'primary',
    minGuests: 10,
    maxGuests: 150,
    avgDuration: 5,
    basePrice: 1200,
    popular: false
  },
  [EventType.GRADUATION]: {
    label: 'Graduation',
    description: 'Graduation parties and academic celebrations',
    icon: '🎓',
    color: 'secondary',
    minGuests: 15,
    maxGuests: 300,
    avgDuration: 4,
    basePrice: 1000,
    popular: false
  },
  [EventType.BABY_SHOWER]: {
    label: 'Baby Shower',
    description: 'Baby showers and gender reveal parties',
    icon: '👶',
    color: 'accent',
    minGuests: 10,
    maxGuests: 100,
    avgDuration: 3,
    basePrice: 600,
    popular: false
  },
  [EventType.ENGAGEMENT]: {
    label: 'Engagement Party',
    description: 'Engagement celebrations and proposal parties',
    icon: '💍',
    color: 'primary',
    minGuests: 15,
    maxGuests: 200,
    avgDuration: 4,
    basePrice: 1000,
    popular: false
  },
  [EventType.RETIREMENT]: {
    label: 'Retirement Party',
    description: 'Retirement celebrations and farewell events',
    icon: '🎉',
    color: 'secondary',
    minGuests: 20,
    maxGuests: 250,
    avgDuration: 4,
    basePrice: 1200,
    popular: false
  },
  [EventType.HOLIDAY]: {
    label: 'Holiday Event',
    description: 'Holiday parties and seasonal celebrations',
    icon: '🎄',
    color: 'accent',
    minGuests: 25,
    maxGuests: 400,
    avgDuration: 5,
    basePrice: 1500,
    popular: false
  },
  [EventType.OTHER]: {
    label: 'Other',
    description: 'Custom events and special occasions',
    icon: '🎪',
    color: 'neutral',
    minGuests: 1,
    maxGuests: 1000,
    avgDuration: 4,
    basePrice: 800,
    popular: false
  }
} as const

// ========================================
// CONTACT TYPES CONFIGURATION
// ========================================

export const CONTACT_TYPE_CONFIG = {
  [ContactType.GENERAL]: {
    label: 'General Inquiry',
    description: 'General questions and information',
    icon: '💬',
    priority: 'normal'
  },
  [ContactType.PRICING]: {
    label: 'Pricing Information',
    description: 'Questions about pricing and packages',
    icon: '💰',
    priority: 'normal'
  },
  [ContactType.AVAILABILITY]: {
    label: 'Availability Check',
    description: 'Check availability for specific dates',
    icon: '📅',
    priority: 'high'
  },
  [ContactType.SERVICES]: {
    label: 'Services Information',
    description: 'Questions about our services',
    icon: '🎯',
    priority: 'normal'
  },
  [ContactType.PARTNERSHIP]: {
    label: 'Partnership Opportunity',
    description: 'Business partnership inquiries',
    icon: '🤝',
    priority: 'high'
  },
  [ContactType.FEEDBACK]: {
    label: 'Feedback',
    description: 'Customer feedback and testimonials',
    icon: '⭐',
    priority: 'low'
  },
  [ContactType.COMPLAINT]: {
    label: 'Complaint',
    description: 'Service complaints or issues',
    icon: '⚠️',
    priority: 'urgent'
  },
  [ContactType.OTHER]: {
    label: 'Other',
    description: 'Other inquiries not listed above',
    icon: '📝',
    priority: 'normal'
  }
} as const

// ========================================
// SERVICES CONFIGURATION
// ========================================

export const SERVICES = [
  {
    id: 'event-planning',
    name: 'Full Event Planning',
    description: 'Complete event planning and coordination from concept to execution',
    icon: '📋',
    basePrice: 1000,
    category: 'planning',
    popular: true,
    features: [
      'Initial consultation and concept development',
      'Vendor sourcing and management',
      'Timeline and budget planning',
      'Day-of coordination',
      'Post-event cleanup coordination'
    ]
  },
  {
    id: 'catering',
    name: 'Catering Services',
    description: 'Professional catering with customizable menus',
    icon: '🍽️',
    basePrice: 25,
    priceUnit: 'per person',
    category: 'catering',
    popular: true,
    features: [
      'Custom menu planning',
      'Professional chef and staff',
      'Full service setup and cleanup',
      'Dietary restriction accommodations',
      'Bar service available'
    ]
  },
  {
    id: 'photography',
    name: 'Photography',
    description: 'Professional event photography and editing',
    icon: '📸',
    basePrice: 500,
    priceUnit: 'per event',
    category: 'documentation',
    popular: true,
    features: [
      'Pre-event consultation',
      '6-8 hours of coverage',
      'High-resolution edited photos',
      'Online gallery delivery',
      'Print release included'
    ]
  },
  {
    id: 'videography',
    name: 'Videography',
    description: 'Professional video production and editing',
    icon: '🎥',
    basePrice: 800,
    priceUnit: 'per event',
    category: 'documentation',
    popular: false,
    features: [
      'Multi-camera setup',
      'Professional editing',
      'Highlight reel included',
      'Raw footage available',
      'Custom music and graphics'
    ]
  },
  {
    id: 'decoration',
    name: 'Decoration & Design',
    description: 'Custom decoration and venue styling',
    icon: '🎨',
    basePrice: 300,
    category: 'decoration',
    popular: true,
    features: [
      'Custom theme development',
      'Centerpieces and linens',
      'Lighting design',
      'Setup and breakdown',
      'Floral arrangements'
    ]
  },
  {
    id: 'entertainment',
    name: 'Entertainment',
    description: 'DJ services and live entertainment',
    icon: '🎵',
    basePrice: 400,
    category: 'entertainment',
    popular: true,
    features: [
      'Professional DJ with equipment',
      'Custom playlist creation',
      'MC services',
      'Dance floor lighting',
      'Backup equipment included'
    ]
  }
] as const

// ========================================
// PRICING TIERS
// ========================================

export const PRICING_TIERS = [
  {
    id: 'essential',
    name: 'Essential',
    description: 'Perfect for intimate gatherings and smaller events',
    price: 1200,
    maxGuests: 50,
    duration: 4,
    popular: false,
    features: [
      'Event planning consultation',
      'Basic decoration package',
      'Professional photography (4 hours)',
      'DJ services',
      'Event coordination',
      'Basic catering setup assistance'
    ],
    notIncluded: [
      'Catering',
      'Videography',
      'Premium decorations',
      'Extended coverage'
    ]
  },
  {
    id: 'premium',
    name: 'Premium',
    description: 'Comprehensive package for most celebrations',
    price: 3500,
    maxGuests: 150,
    duration: 6,
    popular: true,
    features: [
      'Full event planning and design',
      'Premium decoration package',
      'Professional photography (6 hours)',
      'Videography with highlight reel',
      'DJ and entertainment',
      'Full catering coordination',
      'Day-of event management',
      'Floral arrangements'
    ],
    notIncluded: [
      'Catering food costs',
      'Alcohol service',
      'Extended venue time'
    ]
  },
  {
    id: 'luxury',
    name: 'Luxury',
    description: 'Ultimate experience for grand celebrations',
    price: 7500,
    maxGuests: 300,
    duration: 8,
    popular: false,
    features: [
      'Luxury event design and planning',
      'Custom theme development',
      'Professional photography (8 hours)',
      'Cinematic videography',
      'Live entertainment coordination',
      'Premium catering management',
      'Dedicated event manager',
      'Custom floral and lighting design',
      'Transportation coordination',
      'Guest accommodation assistance'
    ],
    notIncluded: [
      'Venue rental',
      'Catering food costs',
      'Guest accommodations'
    ]
  }
] as const

// ========================================
// GALLERY CATEGORIES
// ========================================

export const GALLERY_CATEGORIES = [
  {
    id: 'all',
    name: 'All Events',
    count: 0
  },
  {
    id: 'weddings',
    name: 'Weddings',
    count: 0
  },
  {
    id: 'corporate',
    name: 'Corporate',
    count: 0
  },
  {
    id: 'parties',
    name: 'Parties',
    count: 0
  },
  {
    id: 'decorations',
    name: 'Decorations',
    count: 0
  }
] as const

// ========================================
// FORM VALIDATION RULES
// ========================================

export const VALIDATION_RULES = {
  name: {
    minLength: 2,
    maxLength: 100,
    pattern: /^[a-zA-Z\s\-'\.]+$/
  },
  email: {
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    maxLength: 255
  },
  phone: {
    pattern: /^[\+]?[1-9][\d\s\-\(\)]{7,15}$/,
    maxLength: 20
  },
  message: {
    minLength: 10,
    maxLength: 2000
  },
  subject: {
    minLength: 5,
    maxLength: 200
  },
  guestCount: {
    min: 1,
    max: 1000
  },
  budget: {
    min: 0,
    max: 100000
  }
} as const

// ========================================
// ANIMATION SETTINGS
// ========================================

export const ANIMATIONS = {
  durations: {
    fast: 200,
    normal: 300,
    slow: 500
  },
  easings: {
    easeOut: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
  },
  delays: {
    stagger: 100,
    pageTransition: 150
  }
} as const

// ========================================
// RESPONSIVE BREAKPOINTS
// ========================================

export const BREAKPOINTS = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px'
} as const

// ========================================
// SEO CONFIGURATION
// ========================================

export const SEO_CONFIG = {
  defaultTitle: `${BUSINESS_INFO.name} - ${BUSINESS_INFO.tagline}`,
  titleTemplate: `%s | ${BUSINESS_INFO.name}`,
  defaultDescription: BUSINESS_INFO.description,
  siteUrl: 'https://your-event-booking-site.com', // Update with actual domain
  author: BUSINESS_INFO.name,
  image: '/images/og-image.jpg',
  twitterHandle: '@eliteeventprod',
  facebookAppId: '123456789', // Update with actual ID
  keywords: [
    'event planning',
    'wedding planning',
    'corporate events',
    'party planning',
    'event coordination',
    'Los Angeles events',
    'professional event services'
  ]
} as const

// ========================================
// API CONFIGURATION
// ========================================

export const API_CONFIG = {
  timeout: 30000, // 30 seconds
  retryAttempts: 3,
  retryDelay: 1000,
  cacheTimeout: 5 * 60 * 1000, // 5 minutes
  endpoints: {
    health: '/api/v1/health',
    bookings: '/api/v1/bookings',
    contact: '/api/v1/contact'
  }
} as const

// ========================================
// FEATURE FLAGS
// ========================================

export const FEATURES = {
  enableGalleryLightbox: true,
  enableContactFormSpamProtection: true,
  enableAnalytics: true,
  enableChatWidget: false,
  enableBlogSection: false,
  enableTestimonialsCarousel: true,
  enableServicePackages: true,
  enableVirtualTours: false
} as const