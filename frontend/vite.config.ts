import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

const productionVariables = [
  'VITE_API_BASE_URL',
  'VITE_FIREBASE_API_KEY',
  'VITE_FIREBASE_AUTH_DOMAIN',
  'VITE_FIREBASE_PROJECT_ID',
  'VITE_FIREBASE_APP_ID',
]

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  if (mode === 'production') {
    const localBuild = env.VITE_LOCAL_BUILD === 'true'
    const missing = productionVariables.filter((name) => !env[name]?.trim())
    if (missing.length) {
      throw new Error(`Missing production environment variables: ${missing.join(', ')}`)
    }
    if (!localBuild && !/^https:\/\//.test(env.VITE_API_BASE_URL)) {
      throw new Error('VITE_API_BASE_URL must use HTTPS in production')
    }
  }

  return {
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
      port: 5173,
    },
  }
})
