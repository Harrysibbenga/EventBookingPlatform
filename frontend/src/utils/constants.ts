/**
 * Application constants and configuration values.
 * Centralized location for all static data and settings.
 */

import { EventType, ContactType } from '../types/api'
import { PACKAGES } from './packages';

// ========================================
// BUSINESS INFORMATION (UK • Milton Keynes)
// ========================================

export const BUSINESS_INFO = {
  name: 'Roman Events',
  tagline: 'Milton Keynes Based Event Hire & Design Services',
  description:
    'Roman Events provides professional event hire and design services in Milton Keynes and surrounding areas. We specialise in 4FT LED number hire, custom balloon displays, shimmer walls, floral backdrops, neon signs, and complete themed packages for birthdays, weddings, baby showers, engagements, anniversaries, and more.',

  // Contact information
  email: 'romaneventsmk@gmail.com',
  phone: '+447921510264',
  address: {
    street: 'Bancroft Park',
    city: 'Milton Keynes',
    county: 'Buckinghamshire',
    postcode: 'MK13, 0RA',
    country: 'United Kingdom'
  },

  // Business hours
  hours: {
    monday: '9:00 AM - 6:00 PM',
    tuesday: '9:00 AM - 6:00 PM',
    wednesday: '9:00 AM - 6:00 PM',
    thursday: '9:00 AM - 6:00 PM',
    friday: '9:00 AM - 7:00 PM',
    saturday: '8:00 AM - 8:00 PM',
    sunday: '10:00 AM - 6:00 PM'
  },

  // Social media
  social: {
    instagram: 'https://www.instagram.com/romaneventsmk/',
    facebook: 'https://www.facebook.com/people/Roman-Events-MK/',
    // twitter: 'https://twitter.com/romaneventsmk',
    // linkedin: 'https://linkedin.com/company/romaneventsmk',
    // pinterest: 'https://pinterest.com/romaneventsmk'
  },

  // Founded year
  founded: 2018,

  // Service areas
  serviceAreas: [
    'Milton Keynes',
    'Buckinghamshire',
    'Bedfordshire',
    'Northamptonshire',
    'Oxfordshire',
    'Hertfordshire'
  ]
} as const

// ========================================
// EVENT TYPES CONFIGURATION
// (unchanged labels; UK-agnostic)
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
    basePrice: 250,
    popular: false
  },
  [EventType.GENDER_REVEAL]: {
    label: 'Gender Reveal',
    description: 'Baby showers and gender reveal parties',
    icon: '👶',
    color: 'accent',
    minGuests: 10,
    maxGuests: 100,
    avgDuration: 3,
    basePrice: 230,
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
  [EventType.PROPOSAL]: {
    label: 'Proposal',
    description: 'Romantic proposals and engagement celebrations',
    icon: '💍',
    color: 'primary',
    minGuests: 0,
    maxGuests: 50,
    avgDuration: 2,
    basePrice: 300,
    popular: false
  },
  [EventType.THEME]: {
    label: 'Themed Package',
    description: 'Custom themed parties and special events',
    icon: '🎭',
    color: 'accent',
    minGuests: 10,
    maxGuests: 300,
    avgDuration: 4,
    basePrice: 300,
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
// CONTACT TYPES (unchanged)
// ========================================

export const CONTACT_TYPE_CONFIG = {
  [ContactType.GENERAL]: { label: 'General Inquiry', description: 'General questions and information', icon: '💬', priority: 'normal' },
  [ContactType.PRICING]: { label: 'Pricing Information', description: 'Questions about pricing and packages', icon: '💰', priority: 'normal' },
  [ContactType.AVAILABILITY]: { label: 'Availability Check', description: 'Check availability for specific dates', icon: '📅', priority: 'high' },
  [ContactType.SERVICES]: { label: 'Services Information', description: 'Questions about our services', icon: '🎯', priority: 'normal' },
  [ContactType.PARTNERSHIP]: { label: 'Partnership Opportunity', description: 'Business partnership inquiries', icon: '🤝', priority: 'high' },
  [ContactType.FEEDBACK]: { label: 'Feedback', description: 'Customer feedback and testimonials', icon: '⭐', priority: 'low' },
  [ContactType.COMPLAINT]: { label: 'Complaint', description: 'Service complaints or issues', icon: '⚠️', priority: 'urgent' },
  [ContactType.OTHER]: { label: 'Other', description: 'Other inquiries not listed above', icon: '📝', priority: 'normal' }
} as const

// ========================================
// ROMAN EVENTS - SERVICES & PACKAGES (UK)
// ========================================

export const SERVICES = [
  {
    id: 'led-numbers',
    name: '4FT LED Number Hire',
    description:
      'Illuminated LED numbers for birthdays, anniversaries, and celebrations.',
    image: PACKAGES.numberPackage.src,
    alt: PACKAGES.numberPackage.alt,
    basePrice: 50,
    priceUnit: 'per number (24 hrs)',
    category: 'numbers',
    popular: true,
    options: [
      '1 Number (24 hours) - £50',
      '2 Numbers (24 hours) - £80',
      'With Balloon Display (any colour theme) - from £120'
    ]
  },
  {
    id: 'birthday-package',
    name: 'Birthday Package',
    description:
      'Complete birthday setup with LED numbers, balloon arch, shimmer wall, neon sign and more.',
    image: PACKAGES.birthdayPackage.src,
    alt: PACKAGES.birthdayPackage.alt,
    basePrice: 230,
    category: 'packages',
    popular: true,
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'LED Numbers',
      'LED Neon Sign',
      'Balloon Arch'
    ]
  },
  {
    id: 'baby-shower-package',
    name: 'Baby Shower Package',
    description:
      'Celebrate new arrivals with a magical themed display including BABY balloon boxes and teddy.',
    image: PACKAGES.babyShowerPackage.src,
    alt: PACKAGES.babyShowerPackage.alt,
    basePrice: 250,
    category: 'packages',
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'BABY Boxes (Balloon Filled)',
      'LED Neon Sign',
      'Giant Teddy Bear',
      'Balloon Arch'
    ]
  },
  {
    id: 'gender-reveal-package',
    name: 'Gender Reveal Package',
    description:
      'Stylish setup for gender reveal parties with backdrop, neon sign and balloons.',
    image: PACKAGES.genderRevealPackage.src,
    alt: PACKAGES.genderRevealPackage.alt,
    basePrice: 230,
    category: 'packages',
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'LED Neon Sign',
      'Balloon Arch'
    ]
  },
  {
    id: 'christening-package',
    name: 'Christening Package',
    description:
      'Elegant setup for christening celebrations with a soft, welcoming theme including balloons, florals and a personalised display.',
    image: PACKAGES.christeningPackage.src,
    alt: PACKAGES.christeningPackage.alt,
    basePrice: 180,
    category: 'packages',
    features: [
      'Custom Christening Backdrop with Stand',
      'Balloon Garland in Pastel & Neutral Tones',
      'Artificial Florals & Greenery Decoration',
      'Personalised Wooden / Acrylic Christening Sign'
    ]
  },
  {
    id: 'wedding-package',
    name: 'Wedding Package',
    description:
      'Elegant wedding package with floral displays, shimmer walls, neon sign and balloon arch.',
    image: PACKAGES.weddingPackage.src,
    alt: PACKAGES.weddingPackage.alt,
    basePrice: 250,
    category: 'packages',
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'LED Neon Sign',
      'Artificial Flowers',
      'Balloon Arch'
    ]
  },
  {
    id: 'engagement-package',
    name: 'Engagement Package',
    description:
      'Celebrate engagements with a romantic backdrop, neon lighting, flowers and balloons.',
    image: PACKAGES.engagementPackage.src,
    alt: PACKAGES.engagementPackage.alt,
    basePrice: 250,
    category: 'packages',
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'LED Neon Sign',
      'Artificial Flowers',
      'Balloon Arch'
    ]
  },
  {
    id: 'retirement-package',
    name: 'Retirement Package',
    description:
      'Send off in style with a full event backdrop, neon lighting, flowers and balloons.',
    image: PACKAGES.retirementPackage.src,
    alt: PACKAGES.retirementPackage.alt,
    basePrice: 250,
    category: 'packages',
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'LED Neon Sign',
      'Artificial Flowers',
      'Balloon Arch'
    ]
  },
  {
    id: 'anniversary-package',
    name: 'Anniversary Package',
    description:
      'Celebrate anniversaries with LED numbers, balloons, flowers and a neon backdrop.',
    image: PACKAGES.anniversaryPackage.src,
    alt: PACKAGES.anniversaryPackage.alt,
    basePrice: 250,
    category: 'packages',
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'LED Neon Sign',
      'Numbers',
      'Artificial Flowers',
      'Balloon Arch'
    ]
  },
  {
    id: 'proposal-package',
    name: 'Proposal Package',
    description:
      'Romantic proposal setup with balloons, floral decorations, and a neon sign.',
    image: PACKAGES.proposalPackage.src,
    alt: PACKAGES.proposalPackage.alt,
    basePrice: 300,
    category: 'packages',
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'LED Neon Sign',
      'Artificial Flowers',
      'Balloon Arch'
    ]
  },
  {    
    id: 'theme-package',
    name: 'Theme Party Package',
    description:
      'Custom themed party setup with decorations, balloons, and lighting to match your vision.',
    image: PACKAGES.themePackage.src,
    alt: PACKAGES.themePackage.alt,
    basePrice: 300,
    category: 'packages',
    features: [
      'Kids themed displays',
      'Shimmer wall',
      'Neon light',
      'Light up number',
      'Balloon display',
      'Props'
    ]
  },
  {
    id: 'custom-signs',
    name: 'Customised Wooden Signs',
    description:
      'Personalised wooden signs created with precision laser cutting technology.',
    image: PACKAGES.customWoodSign.src,
    alt: PACKAGES.customWoodSign.alt,
    basePrice: 30,
    category: 'custom',
    features: [
      'Custom text and design',
      'Laser cut for precision',
      'Available in various finishes'
    ]
  }
] as const;


// ========================================
// PRICING TIERS (Roman Events Packages)
// ========================================

export const PRICING_TIERS = [
  {
    id: 'led-numbers',
    name: 'LED Number Hire',
    description: '4FT LED illuminated numbers for birthdays, anniversaries, and celebrations.',
    price: 50,
    maxGuests: 50,
    duration: 1, // 24 hours
    popular: true,
    features: [
      '1 Number Hire (24 hrs) - £50',
      '2 Numbers Hire (24 hrs) - £80',
      'With Balloon Display (any colour theme) - from £120'
    ],
    notIncluded: [
      'Backdrop walls',
      'Neon signs',
      'Additional decorations'
    ]
  },
  {
    id: 'birthday-package',
    name: 'Birthday Package',
    description: 'Complete birthday setup including balloons, shimmer wall, LED numbers and neon sign.',
    price: 230,
    maxGuests: 100,
    duration: 1,
    popular: true,
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'LED Numbers',
      'LED Neon Sign',
      'Balloon Arch'
    ],
    notIncluded: [
      'Catering',
      'Photography',
      'Venue rental'
    ]
  },
  {
    id: 'baby-shower-package',
    name: 'Baby Shower Package',
    description: 'Celebrate new arrivals with themed displays including BABY boxes and a teddy bear.',
    price: 250,
    maxGuests: 100,
    duration: 1,
    popular: true,
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'BABY Boxes (Balloon Filled)',
      'LED Neon Sign',
      'Giant Teddy Bear',
      'Balloon Arch'
    ],
    notIncluded: [
      'Venue rental',
      'Photography',
      'Food & drinks'
    ]
  },
  {
    id: 'wedding-package',
    name: 'Wedding Package',
    description: 'Elegant wedding setup with flowers, shimmer wall, neon sign and balloon arch.',
    price: 250,
    maxGuests: 200,
    duration: 1,
    popular: false,
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'LED Neon Sign',
      'Artificial Flowers',
      'Balloon Arch'
    ],
    notIncluded: [
      'Venue rental',
      'Catering',
      'Entertainment'
    ]
  },
  {
    id: 'engagement-package',
    name: 'Engagement Package',
    description: 'Celebrate engagements with romantic backdrops, neon lights, and balloons.',
    price: 250,
    maxGuests: 150,
    duration: 1,
    popular: false,
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'LED Neon Sign',
      'Artificial Flowers',
      'Balloon Arch'
    ],
    notIncluded: [
      'Venue rental',
      'Photography',
      'Food & drinks'
    ]
  },
  {
    id: 'retirement-package',
    name: 'Retirement Package',
    description: 'Celebrate retirements in style with LED neon, flowers, and balloon displays.',
    price: 250,
    maxGuests: 150,
    duration: 1,
    popular: false,
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'LED Neon Sign',
      'Artificial Flowers',
      'Balloon Arch'
    ],
    notIncluded: [
      'Catering',
      'Photography',
      'Entertainment'
    ]
  },
  {
    id: 'anniversary-package',
    name: 'Anniversary Package',
    description: 'Mark special anniversaries with LED numbers, floral decor, balloons, and neon lights.',
    price: 250,
    maxGuests: 150,
    duration: 1,
    popular: false,
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'LED Neon Sign',
      'Numbers',
      'Artificial Flowers',
      'Balloon Arch'
    ],
    notIncluded: [
      'Venue rental',
      'Catering',
      'Photography'
    ]
  },
  {
    id: 'proposal-package',
    name: 'Proposal Package',
    description: 'Romantic proposal setup with balloons, floral decorations, and a neon sign.',
    price: 300,
    maxGuests: 0,
    duration: 1,
    popular: false,
    features: [
      'Floral / Grass / Shimmer Wall or Balloon Hoop',
      'LED Neon Sign',
      'Artificial Flowers',
      'Balloon Arch'
    ],
    notIncluded: [
      'Catering',
      'Photography',
      'Venue rental'
    ]
  },
  {
    id: 'custom-signs',
    name: 'Customised Wooden Signs',
    description: 'Laser-cut wooden signs for personalised messages and event branding.',
    price: 30,
    maxGuests: 0,
    duration: 0,
    popular: false,
    features: [
      'Custom text and design',
      'Laser cutting technology',
      'Available in multiple finishes'
    ],
    notIncluded: [
      'Delivery outside Milton Keynes',
      'Large-scale signage installation'
    ]
  }
] as const


// ========================================
// GALLERY CATEGORIES (unchanged)
// ========================================

export const GALLERY_CATEGORIES = [
  { id: 'all', name: 'All Events', count: 0 },
  { id: 'weddings', name: 'Weddings', count: 0 },
  { id: 'corporate', name: 'Corporate', count: 0 },
  { id: 'parties', name: 'Parties', count: 0 },
  { id: 'decorations', name: 'Decorations', count: 0 }
] as const

// ========================================
// FORM VALIDATION RULES (unchanged)
// ========================================

export const VALIDATION_RULES = {
  name: { minLength: 2, maxLength: 100, pattern: /^[a-zA-Z\s\-'\.]+$/ },
  email: { pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, maxLength: 255 },
  phone: { pattern: /^[\+]?[1-9][\d\s\-\(\)]{7,15}$/, maxLength: 20 },
  message: { minLength: 10, maxLength: 2000 },
  subject: { minLength: 5, maxLength: 200 },
  guestCount: { min: 1, max: 1000 },
  budget: { min: 0, max: 100000 }
} as const

// ========================================
// ANIMATION / BREAKPOINTS (unchanged)
// ========================================

export const ANIMATIONS = {
  durations: { fast: 200, normal: 300, slow: 500 },
  easings: {
    easeOut: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
  },
  delays: { stagger: 100, pageTransition: 150 }
} as const

export const BREAKPOINTS = {
  sm: '640px', md: '768px', lg: '1024px', xl: '1280px', '2xl': '1536px'
} as const

// ========================================
// SEO CONFIGURATION (MK‑targeted keywords)
// ========================================

export const SEO_CONFIG = {
  defaultTitle: `${BUSINESS_INFO.name} - ${BUSINESS_INFO.tagline}`,
  titleTemplate: `%s | ${BUSINESS_INFO.name}`,
  defaultDescription: BUSINESS_INFO.description,
  siteUrl: 'https://your-event-booking-site.com', // TODO: replace with real domain
  author: BUSINESS_INFO.name,
  image: '/images/logo.png', // ✅ make sure this matches your public/images/logo.jpg
  twitterHandle: '@romaneventsmk', // update if you set up social media
  facebookAppId: '123456789', // replace with real if available
  keywords: [
    'LED number hire Milton Keynes',
    'balloon displays Milton Keynes',
    'shimmer wall hire Milton Keynes',
    'event hire Milton Keynes',
    'baby shower decorations Milton Keynes',
    'birthday balloon displays UK',
    'wedding decoration hire Milton Keynes',
    'engagement party hire Milton Keynes',
    'anniversary event hire Milton Keynes',
    'retirement party decorations Milton Keynes',
    'gender reveal balloon arch Milton Keynes',
    'custom wooden signs Milton Keynes',
    'event design Buckinghamshire',
    'event hire Bedfordshire',
    'event services Northamptonshire'
  ]
} as const

// ========================================
// API CONFIG / FEATURES (unchanged)
// ========================================

export const API_CONFIG = {
  timeout: 30000, retryAttempts: 3, retryDelay: 1000, cacheTimeout: 5 * 60 * 1000,
  endpoints: { health: '/api/v1/health', bookings: '/api/v1/bookings', contact: '/api/v1/contact' }
} as const

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
