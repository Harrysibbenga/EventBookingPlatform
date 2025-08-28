// src/utils/serviceAreas.ts - Optional utility file for managing service area data
export interface ServiceArea {
    id: string
    name: string
    county: string
    icon: string
    isPrimary: boolean
    deliveryFee: number
    setupTime: string
    coverage: string
    description: string
    highlights: string[]
    areas?: string[]
    postcodes?: string[]
    popularVenues: string[]
  }
  
  export const SERVICE_AREAS: ServiceArea[] = [
    {
      id: 'milton-keynes',
      name: 'Milton Keynes',
      county: 'Buckinghamshire',
      icon: '🏢',
      isPrimary: true,
      deliveryFee: 0,
      setupTime: '30-45 minutes',
      popularVenues: ['The Hub MK', 'Stadium MK', 'Xscape Milton Keynes', 'Open University', 'Milton Keynes Theatre'],
      coverage: 'Complete coverage',
      description: 'Our home base with same-day availability and free delivery for all bookings.',
      highlights: ['Free delivery', 'Same-day service', 'Priority booking', 'Extended hours available'],
      postcodes: ['MK1', 'MK2', 'MK3', 'MK4', 'MK5', 'MK6', 'MK7', 'MK8', 'MK9', 'MK10', 'MK11', 'MK12', 'MK13', 'MK14', 'MK15', 'MK16', 'MK17', 'MK18', 'MK19']
    },
    {
      id: 'buckinghamshire',
      name: 'Buckinghamshire',
      county: 'Buckinghamshire',
      icon: '🌳',
      isPrimary: true,
      deliveryFee: 15,
      setupTime: '45-60 minutes',
      popularVenues: ['Waddesdon Manor', 'Stoke Park', 'The Bell at Weston Turville', 'Hartwell House', 'Danesfield House'],
      coverage: 'Full county coverage',
      description: 'Comprehensive coverage across beautiful Buckinghamshire towns and villages.',
      highlights: ['Historic venues', 'Country estates', 'Village celebrations', 'Wedding specialists'],
      areas: ['Aylesbury', 'High Wycombe', 'Beaconsfield', 'Chesham', 'Amersham', 'Marlow', 'Bourne End', 'Gerrards Cross', 'Wendover', 'Princes Risborough']
    },
    {
      id: 'bedfordshire',
      name: 'Bedfordshire',
      county: 'Bedfordshire',
      icon: '🏰',
      isPrimary: false,
      deliveryFee: 20,
      setupTime: '60-75 minutes',
      popularVenues: ['Woburn Abbey', 'Luton Hoo Hotel', 'The Bedford Lodge Hotel', 'Wrest Park', 'De Parys Avenue'],
      coverage: 'Major towns and cities',
      description: 'Serving Bedford, Luton, and surrounding areas with professional event decoration.',
      highlights: ['Historic properties', 'Corporate events', 'Large venues', 'Airport proximity'],
      areas: ['Bedford', 'Luton', 'Dunstable', 'Leighton Buzzard', 'Biggleswade', 'Flitwick', 'Sandy', 'Ampthill', 'Cranfield', 'Woburn']
    },
    {
      id: 'northamptonshire',
      name: 'Northamptonshire',
      county: 'Northamptonshire',
      icon: '⚡',
      isPrimary: false,
      deliveryFee: 25,
      setupTime: '60-75 minutes',
      popularVenues: ['Silverstone Circuit', 'Althorp House', 'Kelmarsh Hall', 'Fawsley Hall', 'Rushton Hall'],
      coverage: 'Northampton and surrounding areas',
      description: 'Home to Silverstone Circuit and beautiful countryside venues across Northamptonshire.',
      highlights: ['Motorsport venues', 'Historic halls', 'Corporate hospitality', 'Countryside events'],
      areas: ['Northampton', 'Kettering', 'Corby', 'Wellingborough', 'Daventry', 'Rushden', 'Brackley', 'Towcester', 'Silverstone', 'Oundle']
    },
    {
      id: 'oxfordshire',
      name: 'Oxfordshire',
      county: 'Oxfordshire',
      icon: '🎓',
      isPrimary: false,
      deliveryFee: 30,
      setupTime: '75-90 minutes',
      popularVenues: ['University of Oxford', 'Blenheim Palace', 'The Randolph Hotel', 'Le Manoir aux Quat Saisons', 'Oxford Town Hall'],
      coverage: 'Oxford and major towns',
      description: 'University city and surrounding historic Oxfordshire locations.',
      highlights: ['University events', 'Historic venues', 'Academic celebrations', 'Prestigious locations'],
      areas: ['Oxford', 'Banbury', 'Bicester', 'Witney', 'Abingdon', 'Didcot', 'Thame', 'Chipping Norton', 'Faringdon', 'Wallingford']
    },
    {
      id: 'hertfordshire',
      name: 'Hertfordshire',
      county: 'Hertfordshire',
      icon: '🌹',
      isPrimary: false,
      deliveryFee: 25,
      setupTime: '60-75 minutes',
      popularVenues: ['Hatfield House', 'Grove Hotel', 'Brocket Hall', 'Hanbury Manor', 'The Saracens Head'],
      coverage: 'St Albans and surrounding areas',
      description: 'Beautiful Hertfordshire venues from historic houses to modern event spaces.',
      highlights: ['Garden parties', 'Historic houses', 'Corporate retreats', 'London proximity'],
      areas: ['St Albans', 'Watford', 'Hemel Hempstead', 'Stevenage', 'Hatfield', 'Berkhamsted', 'Tring', 'Rickmansworth', 'Bushey', 'Hertford']
    }
  ]
  
  // Utility functions for working with service areas
  export const getPrimaryAreas = () => SERVICE_AREAS.filter(area => area.isPrimary)
  export const getExtendedAreas = () => SERVICE_AREAS.filter(area => !area.isPrimary)
  export const getAreaById = (id: string) => SERVICE_AREAS.find(area => area.id === id)
  export const getAreasByDeliveryFee = (maxFee: number) => SERVICE_AREAS.filter(area => area.deliveryFee <= maxFee)
  
  // Service details for delivery information component
  export const SERVICE_DETAILS = {
    standardDelivery: {
      time: '2-4 hour window',
      notification: '1 hour advance call',
      included: 'Setup and styling included'
    },
    collection: {
      time: 'Next day collection',
      window: '2-4 hour window',
      flexibility: 'Flexible timing available'
    },
    coverage: {
      primary: 'Free delivery within 10 miles of Milton Keynes',
      extended: 'Delivery charges apply beyond primary area',
      quote: 'Custom quotes for areas outside standard coverage'
    }
  }
  
  // Popular venues across all areas - useful for search/filtering
  export const ALL_POPULAR_VENUES = SERVICE_AREAS.flatMap(area => 
    area.popularVenues.map(venue => ({
      name: venue,
      area: area.name,
      county: area.county,
      deliveryFee: area.deliveryFee
    }))
  )
  
  // Coverage statistics
  export const COVERAGE_STATS = {
    totalCounties: SERVICE_AREAS.length,
    primaryAreas: getPrimaryAreas().length,
    extendedAreas: getExtendedAreas().length,
    freeDeliveryAreas: getAreasByDeliveryFee(0).length,
    totalVenues: SERVICE_AREAS.reduce((total, area) => total + area.popularVenues.length, 0),
    totalTowns: SERVICE_AREAS.reduce((total, area) => total + (area.areas?.length || 0), 0),
    totalPostcodes: SERVICE_AREAS.reduce((total, area) => total + (area.postcodes?.length || 0), 0)
  }
  
  // Helper function to calculate delivery fee for a given area
  export const calculateDeliveryFee = (areaId: string): number => {
    const area = getAreaById(areaId)
    return area ? area.deliveryFee : 0
  }
  
  // Helper function to get setup time for a given area
  export const getSetupTime = (areaId: string): string => {
    const area = getAreaById(areaId)
    return area ? area.setupTime : 'Contact for details'
  }
  
  // Search function for finding areas by name or town
  export const searchAreas = (query: string): ServiceArea[] => {
    const searchTerm = query.toLowerCase()
    return SERVICE_AREAS.filter(area => 
      area.name.toLowerCase().includes(searchTerm) ||
      area.county.toLowerCase().includes(searchTerm) ||
      area.areas?.some(town => town.toLowerCase().includes(searchTerm)) ||
      area.postcodes?.some(postcode => postcode.toLowerCase().includes(searchTerm))
    )
  }
  
  // Function to get the nearest area based on postcode (simplified example)
  export const findNearestArea = (postcode: string): ServiceArea | null => {
    // This would typically integrate with a postcode lookup service
    // For now, simple prefix matching with Milton Keynes postcodes
    if (postcode.toUpperCase().startsWith('MK')) {
      return getAreaById('milton-keynes')
    }
    
    // Could extend with more sophisticated postcode matching
    // HP = Buckinghamshire, LU = Bedfordshire, etc.
    const postcodePrefix = postcode.substring(0, 2).toUpperCase()
    const prefixMap: Record<string, string> = {
      'HP': 'buckinghamshire',
      'LU': 'bedfordshire',
      'NN': 'northamptonshire',
      'OX': 'oxfordshire',
      'AL': 'hertfordshire',
      'WD': 'hertfordshire',
      'EN': 'hertfordshire'
    }
    
    const areaId = prefixMap[postcodePrefix]
    return areaId ? getAreaById(areaId) : null
  }
  
  // Export default configuration
  export default {
    areas: SERVICE_AREAS,
    serviceDetails: SERVICE_DETAILS,
    stats: COVERAGE_STATS
  }