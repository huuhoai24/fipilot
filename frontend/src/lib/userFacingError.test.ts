import { describe, expect, it } from 'vitest'
import {
  getAuthFailureMessage,
  getResumeUploadError,
  getUserFacingError,
} from '@/lib/userFacingError'

describe('user-facing error messages', () => {
  it('replaces browser network details with an actionable message', () => {
    expect(getUserFacingError(new TypeError('Failed to fetch'), 'Something went wrong.')).toBe(
      'We could not connect to the service. Check your connection and try again.',
    )
  })

  it('preserves a structured API message intended for the candidate', () => {
    const error = Object.assign(new Error('This document does not appear to be a resume.'), {
      status: 422,
    })

    expect(getUserFacingError(error, 'Resume analysis failed.')).toBe(
      'This document does not appear to be a resume.',
    )
  })

  it('does not expose implementation failures', () => {
    expect(getUserFacingError(
      new Error("Cannot read properties of undefined (reading 'profile')"),
      'Something went wrong. Please try again.',
    )).toBe('Something went wrong. Please try again.')
  })

  it('maps classified connectivity, authentication, validation, and server failures', () => {
    expect(getResumeUploadError(Object.assign(new Error('Request failed'), {
      category: 'BACKEND_UNREACHABLE',
    }))).toBe('Backend service is unavailable. Please check the API connection.')
    expect(getResumeUploadError(Object.assign(new Error('Request failed'), {
      category: 'AUTH_FAILURE',
    }))).toBe('Your session could not be verified. Please sign in again.')
    expect(getResumeUploadError(Object.assign(new Error('Request failed'), {
      category: 'UPLOAD_VALIDATION_ERROR',
    }))).toBe('Unable to process this resume file.')
    expect(getResumeUploadError(Object.assign(new Error('internal stack'), {
      category: 'SERVER_ERROR',
    }))).toBe('The server encountered an error while analyzing the resume.')
  })

  it('treats closing the Google popup as cancellation', () => {
    expect(getAuthFailureMessage({ code: 'auth/popup-closed-by-user' })).toEqual({
      kind: 'cancelled',
      message: 'Sign-in was cancelled. You can try again when you are ready.',
    })
  })
})
