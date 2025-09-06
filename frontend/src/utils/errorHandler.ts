// utils/errorHandler.ts
/**
 * Enhanced error handling utility for booking form responses
 */

export interface UserAction {
    text: string
    action_type: 'email' | 'phone' | 'link' | 'retry'
    url?: string
    phone?: string
    email?: string
    is_primary: boolean
  }
  
  export interface ErrorModalOptions {
    title: string
    message: string
    type: 'error' | 'warning' | 'info'
    actions: Array<{
      text: string
      action: () => void
      is_primary?: boolean
      variant?: 'primary' | 'secondary' | 'danger'
    }>
  }
  
  export class BookingErrorHandler {
    
    /**
     * Handle booking form submission errors with appropriate user guidance
     */
    static handleBookingError(error: any): ErrorModalOptions {
      const errorData = error.response?.data || error
      
      // Handle different error types based on error_code
      switch (errorData.error_code) {
        case 'DUPLICATE_BOOKING':
          return this.handleDuplicateBooking(errorData)
        
        case 'MINIMUM_TIMEFRAME_ERROR':
          return this.handleMinimumTimeframe(errorData)
        
        case 'VALIDATION_ERROR':
          return this.handleValidationError(errorData)
        
        case 'SERVICE_ERROR':
        case 'SYSTEM_ERROR':
          return this.handleServiceError(errorData)
        
        default:
          return this.handleGenericError(errorData)
      }
    }
    
    /**
     * Handle duplicate booking errors with detailed guidance
     */
    private static handleDuplicateBooking(errorData: any): ErrorModalOptions {
      const existing = errorData.existing_booking
      const actions = []
      
      // Convert API user actions to modal actions
      if (errorData.user_actions) {
        for (const apiAction of errorData.user_actions) {
          actions.push({
            text: apiAction.text,
            action: () => this.executeUserAction(apiAction),
            is_primary: apiAction.is_primary,
            variant: apiAction.is_primary ? 'primary' : 'secondary'
          })
        }
      }
      
      // Add default actions if none provided
      if (actions.length === 0) {
        actions.push(
          {
            text: 'Check Email',
            action: () => window.open('mailto:', '_blank'),
            is_primary: true
          },
          {
            text: 'Contact Us',
            action: () => this.openContactInfo(errorData.contact_info),
            is_primary: false
          }
        )
      }
      
      return {
        title: 'Booking Already Exists',
        message: errorData.message,
        type: 'info',
        actions
      }
    }
    
    /**
     * Handle minimum timeframe errors (rush booking scenarios)
     */
    private static handleMinimumTimeframe(errorData: any): ErrorModalOptions {
      const actions = []
      
      // Convert API user actions
      if (errorData.user_actions) {
        for (const apiAction of errorData.user_actions) {
          actions.push({
            text: apiAction.text,
            action: () => this.executeUserAction(apiAction),
            is_primary: apiAction.is_primary,
            variant: apiAction.action_type === 'phone' ? 'primary' : 'secondary'
          })
        }
      }
      
      return {
        title: errorData.rush_booking_available ? 'Rush Booking Available' : 'Minimum Notice Required',
        message: errorData.message,
        type: 'warning',
        actions
      }
    }
    
    /**
     * Handle field validation errors
     */
    private static handleValidationError(errorData: any): ErrorModalOptions {
      let message = errorData.message || 'Please correct the following errors and try again:'
      
      // Add specific validation errors if available
      if (errorData.validation_errors && errorData.validation_errors.length > 0) {
        const errorList = errorData.validation_errors
          .map((err: any) => `• ${err.message}`)
          .join('\n')
        message += '\n\n' + errorList
      }
      
      return {
        title: 'Please Check Your Information',
        message,
        type: 'error',
        actions: [
          {
            text: 'Review Form',
            action: () => {
              // Scroll to first error or top of form
              const firstError = document.querySelector('.border-red-500')
              if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' })
              }
            },
            is_primary: true
          }
        ]
      }
    }
    
    /**
     * Handle service/system errors
     */
    private static handleServiceError(errorData: any): ErrorModalOptions {
      const actions = [
        {
          text: 'Try Again',
          action: () => {
            // Trigger form resubmission
            const submitButton = document.querySelector('[type="submit"]') as HTMLButtonElement
            if (submitButton) {
              submitButton.click()
            }
          },
          is_primary: true
        }
      ]
      
      // Add contact options if available
      if (errorData.contact_info) {
        if (errorData.contact_info.email) {
          actions.push({
            text: 'Email Support',
            action: () => window.open(`mailto:${errorData.contact_info.email}?subject=Booking Error - Reference: ${errorData.reference_id}`, '_blank'),
            is_primary: false
          })
        }
        
        if (errorData.contact_info.phone) {
          actions.push({
            text: 'Call Support',
            action: () => window.open(`tel:${errorData.contact_info.phone}`, '_blank'),
            is_primary: false
          })
        }
      }
      
      return {
        title: 'Technical Issue',
        message: errorData.message + (errorData.reference_id ? `\n\nReference ID: ${errorData.reference_id}` : ''),
        type: 'error',
        actions
      }
    }
    
    /**
     * Handle generic/unknown errors
     */
    private static handleGenericError(errorData: any): ErrorModalOptions {
      return {
        title: 'Booking Submission Error',
        message: errorData.message || 'An unexpected error occurred. Please try again or contact us directly.',
        type: 'error',
        actions: [
          {
            text: 'Try Again',
            action: () => window.location.reload(),
            is_primary: true
          },
          {
            text: 'Contact Support',
            action: () => window.open('mailto:info@business.com', '_blank'),
            is_primary: false
          }
        ]
      }
    }
    
    /**
     * Execute user action from API response
     */
    private static executeUserAction(action: UserAction): void {
      switch (action.action_type) {
        case 'email':
          if (action.email) {
            window.open(`mailto:${action.email}`, '_blank')
          } else {
            window.open('mailto:', '_blank')
          }
          break
          
        case 'phone':
          if (action.phone) {
            window.open(`tel:${action.phone}`, '_blank')
          }
          break
          
        case 'link':
          if (action.url) {
            window.open(action.url, '_blank')
          }
          break
          
        case 'retry':
          // Reset form to step 1 or reload page
          const event = new CustomEvent('booking-form-reset')
          document.dispatchEvent(event)
          break
          
        default:
          console.warn('Unknown action type:', action.action_type)
      }
    }
    
    /**
     * Open contact information modal or redirect
     */
    private static openContactInfo(contactInfo: any): void {
      if (contactInfo?.phone) {
        const userChoice = confirm(
          `Contact us:\n\nPhone: ${contactInfo.phone}\nEmail: ${contactInfo.email || 'info@business.com'}\n\nClick OK to call, Cancel to email`
        )
        
        if (userChoice && contactInfo.phone) {
          window.open(`tel:${contactInfo.phone}`, '_blank')
        } else if (contactInfo.email) {
          window.open(`mailto:${contactInfo.email}`, '_blank')
        }
      } else if (contactInfo?.email) {
        window.open(`mailto:${contactInfo.email}`, '_blank')
      }
    }
    
    /**
     * Create a user-friendly error message for display
     */
    static createErrorMessage(error: any): string {
      const errorData = error.response?.data || error
      
      // Extract the main message
      let message = errorData.message || 'An error occurred while submitting your booking.'
      
      // Add recommendations if available
      if (errorData.recommendations && errorData.recommendations.length > 0) {
        message += '\n\nRecommendations:\n' + 
          errorData.recommendations.map((rec: string) => `• ${rec}`).join('\n')
      }
      
      return message
    }
    
    /**
     * Check if error is a duplicate booking
     */
    static isDuplicateBooking(error: any): boolean {
      return error.response?.data?.error_code === 'DUPLICATE_BOOKING'
    }
    
    /**
     * Check if error is a timeframe issue
     */
    static isTimeframeError(error: any): boolean {
      return error.response?.data?.error_code === 'MINIMUM_TIMEFRAME_ERROR'
    }
    
    /**
     * Extract reference number from error (if available)
     */
    static getErrorReference(error: any): string | null {
      const errorData = error.response?.data || error
      return errorData.reference_id || 
             errorData.existing_booking?.reference_number || 
             null
    }
  }
  
  // Vue composable for booking error handling
  export function useBookingErrorHandler() {
    const showErrorModal = ref(false)
    const errorModalOptions = ref<ErrorModalOptions | null>(null)
    
    const handleError = (error: any) => {
      errorModalOptions.value = BookingErrorHandler.handleBookingError(error)
      showErrorModal.value = true
    }
    
    const closeErrorModal = () => {
      showErrorModal.value = false
      errorModalOptions.value = null
    }
    
    return {
      showErrorModal,
      errorModalOptions,
      handleError,
      closeErrorModal
    }
  }