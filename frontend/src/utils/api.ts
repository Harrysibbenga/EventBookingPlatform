/**
 * API client utility for communicating with the FastAPI backend.
 * Provides type-safe methods for all API endpoints with enhanced error handling.
 */

import type {
  BookingCreate,
  BookingResponse,
  BookingConfirmation,
  BookingFormOptions,
  ContactCreate,
  ContactResponse,
  ContactConfirmation,
  ContactFormOptions,
  ApiResponse,
  ApiError,
  HealthCheck,
  DetailedHealthCheck
} from '../types/api'

// Configuration
const API_BASE_URL = import.meta.env.PUBLIC_API_BASE_URL || 'http://localhost:8000'
const API_TIMEOUT = 30000 // 30 seconds

/**
 * HTTP client wrapper with error handling and type safety
 */
class HttpClient {
  private baseURL: string
  private timeout: number
  private headers: Record<string, string>

  constructor(baseURL: string, timeout: number = API_TIMEOUT) {
    this.baseURL = baseURL
    this.timeout = timeout
    this.headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  }

  /**
   * Set authorization header for admin requests
   */
  setAuthToken(token: string) {
    this.headers['Authorization'] = `Bearer ${token}`
  }

  /**
   * Remove authorization header
   */
  clearAuthToken() {
    delete this.headers['Authorization']
  }

  /**
   * Make HTTP request with enhanced error handling
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    
    // Create abort controller for timeout
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), this.timeout)

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          ...this.headers,
          ...options.headers
        },
        signal: controller.signal
      })

      clearTimeout(timeoutId)

      // Handle HTTP errors - preserve detailed error information
      if (!response.ok) {
        let errorData: any
        
        try {
          errorData = await response.json()
        } catch {
          errorData = {
            error: 'Unknown Error',
            message: `HTTP ${response.status}: ${response.statusText}`,
            status: response.status
          }
        }
        
        // For our enhanced error responses, preserve the full structure
        throw new ApiClientError(
          errorData.message || `Request failed with status ${response.status}`,
          response.status,
          errorData // This now contains the full error response
        )
      }

      // Handle empty responses
      const contentType = response.headers.get('content-type')
      if (!contentType?.includes('application/json')) {
        return {} as T
      }

      return await response.json()
      
    } catch (error) {
      clearTimeout(timeoutId)
      
      if (error instanceof ApiClientError) {
        throw error
      }
      
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          throw new ApiClientError('Request timeout', 408)
        }
        throw new ApiClientError(error.message, 0)
      }
      
      throw new ApiClientError('Unknown error occurred', 0)
    }
  }

  /**
   * GET request
   */
  async get<T>(endpoint: string, params?: Record<string, any>): Promise<T> {
    const url = new URL(endpoint, this.baseURL)
    
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          url.searchParams.append(key, String(value))
        }
      })
    }

    return this.request<T>(url.pathname + url.search)
  }

  /**
   * POST request
   */
  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  /**
   * PUT request
   */
  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  /**
   * DELETE request
   */
  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'DELETE'
    })
  }
}

/**
 * Custom error class for API client errors with enhanced error handling
 */
export class ApiClientError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: any // Enhanced to handle any error response structure
  ) {
    super(message)
    this.name = 'ApiClientError'
  }

  get isNetworkError(): boolean {
    return this.status === 0
  }

  get isTimeoutError(): boolean {
    return this.status === 408
  }

  get isServerError(): boolean {
    return this.status >= 500
  }

  get isClientError(): boolean {
    return this.status >= 400 && this.status < 500
  }

  get isValidationError(): boolean {
    return this.status === 422
  }

  get isDuplicateBooking(): boolean {
    return this.status === 409 && this.data?.error_code === 'DUPLICATE_BOOKING'
  }

  get isMinimumTimeframeError(): boolean {
    return this.status === 422 && this.data?.error_code === 'MINIMUM_TIMEFRAME_ERROR'
  }

  /**
   * Get user-friendly error message
   */
  get userMessage(): string {
    if (this.isDuplicateBooking) {
      return this.data?.message || 'A booking already exists for this date and email'
    }
    
    if (this.isMinimumTimeframeError) {
      return this.data?.message || 'This booking does not meet the minimum advance notice requirement'
    }
    
    if (this.isValidationError) {
      return this.data?.message || 'Please check your information and try again'
    }
    
    if (this.isNetworkError) {
      return 'Network error. Please check your internet connection and try again.'
    }
    
    if (this.isTimeoutError) {
      return 'Request timed out. Please try again.'
    }
    
    if (this.isServerError) {
      return 'Server error. Please try again later.'
    }
    
    return this.message || 'An unexpected error occurred'
  }
}

/**
 * API client class with typed methods for all endpoints
 */
export class ApiClient {
  private http: HttpClient

  constructor(baseURL: string = API_BASE_URL) {
    this.http = new HttpClient(baseURL)
  }

  /**
   * Set authentication token for admin requests
   */
  setAuthToken(token: string) {
    this.http.setAuthToken(token)
  }

  /**
   * Clear authentication token
   */
  clearAuthToken() {
    this.http.clearAuthToken()
  }

  // ========================================
  // HEALTH CHECK ENDPOINTS
  // ========================================

  /**
   * Basic health check
   */
  async getHealth(): Promise<HealthCheck> {
    return this.http.get<HealthCheck>('/api/v1/health/')
  }

  /**
   * Detailed health check
   */
  async getDetailedHealth(): Promise<DetailedHealthCheck> {
    return this.http.get<DetailedHealthCheck>('/api/v1/health/detailed/')
  }

  // ========================================
  // BOOKING ENDPOINTS
  // ========================================

  /**
   * Submit a new booking inquiry
   */
  async createBooking(booking: BookingCreate): Promise<BookingConfirmation> {
    return this.http.post<BookingConfirmation>('/api/v1/bookings/', booking)
  }

  /**
   * Get booking form configuration options
   */
  async getBookingFormOptions(): Promise<BookingFormOptions> {
    return this.http.get<BookingFormOptions>('/api/v1/bookings/form/options/')
  }

  /**
   * Get specific booking by ID (admin)
   */
  async getBooking(id: number): Promise<BookingResponse> {
    return this.http.get<BookingResponse>(`/api/v1/bookings/${id}/`)
  }

  /**
   * Search bookings (admin)
   */
  async searchBookings(query: string): Promise<BookingResponse[]> {
    return this.http.get<BookingResponse[]>('/api/v1/bookings/search/inquiries/', { q: query })
  }

  // ========================================
  // CONTACT ENDPOINTS
  // ========================================

  /**
   * Submit a new contact inquiry
   */
  async createContact(contact: ContactCreate): Promise<ContactConfirmation> {
    return this.http.post<ContactConfirmation>('/api/v1/contact/', contact)
  }

  /**
   * Get contact form configuration options
   */
  async getContactFormOptions(): Promise<ContactFormOptions> {
    return this.http.get<ContactFormOptions>('/api/v1/contact/form/options/')
  }

  /**
   * Get specific contact by ID (admin)
   */
  async getContact(id: number): Promise<ContactResponse> {
    return this.http.get<ContactResponse>(`/api/v1/contact/${id}/`)
  }

  /**
   * Search contacts (admin)
   */
  async searchContacts(query: string): Promise<ContactResponse[]> {
    return this.http.get<ContactResponse[]>('/api/v1/contact/search/inquiries/', { q: query })
  }
}

// ========================================
// SINGLETON INSTANCE
// ========================================

export const apiClient = new ApiClient()

// ========================================
// ENHANCED CONVENIENCE FUNCTIONS
// ========================================

/**
 * Submit booking inquiry with enhanced error handling
 */
export async function submitBooking(booking: BookingCreate): Promise<ApiResponse<BookingConfirmation>> {
  try {
    const result = await apiClient.createBooking(booking)
    return { 
      data: result,
      message: 'Booking submitted successfully'
    }
  } catch (error) {
    if (error instanceof ApiClientError) {
      return { 
        error: error.message,
        message: error.userMessage,
        status: error.status,
        errorDetails: error.data // Preserve all error details including error_code, existing_booking, etc.
      }
    }
    return { 
      error: 'Unknown error',
      message: 'An unexpected error occurred. Please try again.',
      status: 0
    }
  }
}

/**
 * Submit contact inquiry with enhanced error handling
 */
export async function submitContact(contact: ContactCreate): Promise<ApiResponse<ContactConfirmation>> {
  try {
    const result = await apiClient.createContact(contact)
    return { 
      data: result,
      message: 'Contact submitted successfully'
    }
  } catch (error) {
    if (error instanceof ApiClientError) {
      return { 
        error: error.message,
        message: error.userMessage,
        status: error.status,
        errorDetails: error.data
      }
    }
    return { 
      error: 'Unknown error',
      message: 'An unexpected error occurred. Please try again.',
      status: 0
    }
  }
}

/**
 * Get booking form options with caching
 */
let bookingOptionsCache: BookingFormOptions | null = null
let bookingOptionsCacheTime = 0
const CACHE_DURATION = 5 * 60 * 1000 // 5 minutes

export async function getBookingFormOptions(): Promise<BookingFormOptions> {
  const now = Date.now()
  
  if (bookingOptionsCache && (now - bookingOptionsCacheTime) < CACHE_DURATION) {
    return bookingOptionsCache
  }
  
  try {
    const options = await apiClient.getBookingFormOptions()
    bookingOptionsCache = options
    bookingOptionsCacheTime = now
    return options
  } catch (error) {
    // Return cached data if available, otherwise throw
    if (bookingOptionsCache) {
      return bookingOptionsCache
    }
    throw error
  }
}

/**
 * Get contact form options with caching
 */
let contactOptionsCache: ContactFormOptions | null = null
let contactOptionsCacheTime = 0

export async function getContactFormOptions(): Promise<ContactFormOptions> {
  const now = Date.now()
  
  if (contactOptionsCache && (now - contactOptionsCacheTime) < CACHE_DURATION) {
    return contactOptionsCache
  }
  
  try {
    const options = await apiClient.getContactFormOptions()
    contactOptionsCache = options
    contactOptionsCacheTime = now
    return options
  } catch (error) {
    // Return cached data if available, otherwise throw
    if (contactOptionsCache) {
      return contactOptionsCache
    }
    throw error
  }
}

/**
 * Check API health
 */
export async function checkApiHealth(): Promise<boolean> {
  try {
    await apiClient.getHealth()
    return true
  } catch (error) {
    console.warn('API health check failed:', error)
    return false
  }
}

/**
 * Retry wrapper for API calls
 */
export async function withRetry<T>(
  operation: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> {
  let lastError: Error

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await operation()
    } catch (error) {
      lastError = error as Error
      
      // Don't retry client errors (4xx) - these are usually validation or duplicate errors
      if (error instanceof ApiClientError && error.isClientError) {
        throw error
      }
      
      // Don't retry on last attempt
      if (attempt === maxRetries) {
        break
      }
      
      // Wait before retrying
      await new Promise(resolve => setTimeout(resolve, delay * attempt))
    }
  }
  
  throw lastError!
}

/**
 * Format API errors for user display with enhanced error handling
 */
export function formatApiError(error: unknown): string {
  if (error instanceof ApiClientError) {
    return error.userMessage
  }
  
  if (error instanceof Error) {
    return error.message
  }
  
  return 'An unexpected error occurred. Please try again.'
}

/**
 * Check if error is a duplicate booking error
 */
export function isDuplicateBookingError(error: unknown): boolean {
  return error instanceof ApiClientError && error.isDuplicateBooking
}

/**
 * Check if error is a validation error
 */
export function isValidationError(error: unknown): boolean {
  return error instanceof ApiClientError && error.isValidationError
}

/**
 * Extract duplicate booking details from error
 */
export function getDuplicateBookingDetails(error: unknown): any | null {
  if (error instanceof ApiClientError && error.isDuplicateBookingError) {
    return {
      message: error.data?.message,
      existingBooking: error.data?.existing_booking,
      contactInfo: error.data?.contact_info,
      recommendations: error.data?.recommendations,
      userActions: error.data?.user_actions
    }
  }
  return null
}