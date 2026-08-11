// THROWAWAY RENDER HARNESS: never use this config in production.
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const harnessRoot = fileURLToPath(new URL('.', import.meta.url))
const frontendRoot = path.resolve(harnessRoot, '../..')

export default defineConfig({
  root: harnessRoot,
  plugins: [react()],
  css: {
    postcss: path.resolve(frontendRoot, 'postcss.config.js'),
  },
  resolve: {
    alias: [
      {
        find: '@/lib/api',
        replacement: path.resolve(harnessRoot, 'src/mockApi.ts'),
      },
      {
        find: '@/contexts/AuthContext',
        replacement: path.resolve(harnessRoot, 'src/mockAuth.ts'),
      },
      {
        find: '@',
        replacement: path.resolve(frontendRoot, 'src'),
      },
    ],
  },
  server: {
    host: '127.0.0.1',
    port: 4174,
  },
})
