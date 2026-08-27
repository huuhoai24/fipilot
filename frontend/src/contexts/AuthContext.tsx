import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import {
  onAuthStateChanged,
  signInWithPopup,
  signOut,
  type User,
} from 'firebase/auth'
import { firebaseAuth, googleAuthProvider, isFirebaseConfigured } from '@/lib/firebase'

interface LocalDevUser {
  uid: string
  email: string | null
  displayName: string | null
  photoURL: string | null
  isLocalDev: true
}

type AppUser = User | LocalDevUser

interface AuthContextValue {
  user: AppUser | null
  loading: boolean
  isLocalDev: boolean
  signInWithGoogle: () => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AppUser | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!firebaseAuth) {
      // Local development without Firebase: behave as the backend dev user so
      // the app is usable when AUTH_ENABLED=false.
      setUser({
        uid: 'local-development-user',
        email: null,
        displayName: 'Local Dev',
        photoURL: null,
        isLocalDev: true,
      })
      setLoading(false)
      return
    }
    return onAuthStateChanged(firebaseAuth, (nextUser) => {
      setUser(nextUser)
      setLoading(false)
    })
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      loading,
      isLocalDev: !isFirebaseConfigured,
      signInWithGoogle: async () => {
        if (!firebaseAuth || !googleAuthProvider) {
          throw new Error('Firebase authentication is not configured.')
        }
        await signInWithPopup(firebaseAuth, googleAuthProvider)
      },
      logout: async () => {
        if (firebaseAuth) await signOut(firebaseAuth)
        else setUser(null)
      },
    }),
    [loading, user]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
