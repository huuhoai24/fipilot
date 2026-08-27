import { getApp, getApps, initializeApp, type FirebaseApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider, type Auth } from 'firebase/auth'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
}

export const isFirebaseConfigured = Boolean(firebaseConfig.apiKey)

let firebaseApp: FirebaseApp | null = null
let firebaseAuth: Auth | null = null

if (isFirebaseConfigured) {
  firebaseApp = getApps().length ? getApp() : initializeApp(firebaseConfig)
  firebaseAuth = getAuth(firebaseApp)
}

export { firebaseApp, firebaseAuth }

export const googleAuthProvider = firebaseAuth ? new GoogleAuthProvider() : null
if (googleAuthProvider) {
  googleAuthProvider.setCustomParameters({ prompt: 'select_account' })
}
