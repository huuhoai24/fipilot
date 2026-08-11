// THROWAWAY PROTOTYPE: isolated Vite entry point. Do not promote this config to production.
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const prototypeRoot = fileURLToPath(new URL('.', import.meta.url))

export default defineConfig({
  root: prototypeRoot,
  base: '/prototype/candidate-profile-review/',
  plugins: [react()],
  resolve: {
    alias: {
      '@prototype': path.resolve(prototypeRoot, './src'),
    },
  },
  server: {
    host: '127.0.0.1',
    port: 4173,
  },
})
