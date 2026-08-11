export interface AuthFailureMessage {
  kind: 'cancelled' | 'error'
  message: string
}

function asRecord(value: unknown): Record<string, unknown> | null {
  return typeof value === 'object' && value !== null
    ? value as Record<string, unknown>
    : null
}

function errorCode(error: unknown): string {
  const record = asRecord(error)
  if (typeof record?.code === 'string') return record.code.toLowerCase()

  const message = error instanceof Error
    ? error.message
    : typeof record?.message === 'string'
      ? record.message
      : ''
  return message.match(/auth\/[a-z-]+/i)?.[0]?.toLowerCase() ?? ''
}

function isNetworkFailure(error: unknown): boolean {
  const record = asRecord(error)
  const message = error instanceof Error
    ? error.message
    : typeof record?.message === 'string'
      ? record.message
      : ''
  return (
    error instanceof TypeError
    || /failed to fetch|network(?: request)? failed|load failed|networkerror/i.test(message)
  )
}

export function getAuthFailureMessage(error: unknown): AuthFailureMessage {
  const code = errorCode(error)

  if (code === 'auth/popup-closed-by-user' || code === 'auth/cancelled-popup-request') {
    return {
      kind: 'cancelled',
      message: 'Sign-in was cancelled. You can try again when you are ready.',
    }
  }
  if (code === 'auth/popup-blocked') {
    return {
      kind: 'error',
      message: 'Your browser blocked the sign-in window. Allow pop-ups and try again.',
    }
  }
  if (code === 'auth/network-request-failed' || isNetworkFailure(error)) {
    return {
      kind: 'error',
      message: 'We could not connect to Google. Check your connection and try again.',
    }
  }
  return {
    kind: 'error',
    message: 'Sign-in is temporarily unavailable. Please try again.',
  }
}

export function getUserFacingError(
  error: unknown,
  fallback: string,
  networkFallback = 'We could not connect to the service. Check your connection and try again.',
): string {
  const record = asRecord(error)
  const message = error instanceof Error
    ? error.message
    : typeof record?.message === 'string'
      ? record.message
      : ''
  if (record?.category === 'BACKEND_UNREACHABLE') {
    return 'Backend service is unavailable. Please check the API connection.'
  }
  if (record?.category === 'AUTH_FAILURE') {
    return 'Your session could not be verified. Please sign in again.'
  }
  if (record?.category === 'CORS_OR_NETWORK') {
    return 'The browser could not reach the API. Check your connection and allowed origin.'
  }
  if (record?.category === 'SERVER_ERROR') {
    return fallback
  }
  if (record?.category === 'UPLOAD_VALIDATION_ERROR') {
    return message && message !== 'Request failed'
      ? message
      : 'Unable to process this resume file.'
  }
  if (isNetworkFailure(error)) return networkFallback

  const isApiError = error instanceof Error && typeof record?.status === 'number'
  const looksTechnical = (
    !message
    || message === 'Request failed'
    || /^firebase:/i.test(message)
    || /cannot read properties|is not a function|internal server error|econn[a-z]+/i.test(message)
  )

  if (isApiError && message && message !== 'Request failed') return message
  if (error instanceof Error && !looksTechnical) return message
  return fallback
}

export function getInterviewAnswerError(error: unknown): string {
  const record = asRecord(error)
  if (
    record?.category === 'BACKEND_UNREACHABLE'
    || record?.category === 'CORS_OR_NETWORK'
    || isNetworkFailure(error)
  ) {
    return 'Your answer could not be submitted. Check your connection and try again.'
  }
  if (record?.category === 'AUTH_FAILURE') {
    return 'Your session could not be verified. Sign in again before retrying your answer.'
  }
  return 'Your answer could not be submitted. Please try again.'
}

export function getResumeUploadError(error: unknown): string {
  const record = asRecord(error)
  if (record?.category === 'SERVER_ERROR') {
    return 'The server encountered an error while analyzing the resume.'
  }
  return getUserFacingError(error, 'Resume analysis failed. Please try again.')
}
