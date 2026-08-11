import { readFileSync, readdirSync } from 'node:fs'
import { resolve } from 'node:path'

function readEnvFile(path) {
  const values = {}
  for (const line of readFileSync(path, 'utf8').split(/\r?\n/)) {
    const trimmed = line.trim()
    if (!trimmed || trimmed.startsWith('#')) continue
    const separator = trimmed.indexOf('=')
    if (separator < 1) continue
    const key = trimmed.slice(0, separator).trim()
    const rawValue = trimmed.slice(separator + 1).trim()
    values[key] = rawValue.replace(/^(['"])(.*)\1$/, '$2')
  }
  return values
}

const frontendRoot = resolve(import.meta.dirname, '..')
const productionEnv = readEnvFile(resolve(frontendRoot, '.env.production'))
const expectedApiBaseUrl = productionEnv.VITE_API_BASE_URL

if (!expectedApiBaseUrl?.startsWith('https://')) {
  throw new Error('Production API base URL must be configured with HTTPS.')
}

const assetsDirectory = resolve(frontendRoot, 'dist', 'assets')
const javascriptAsset = readdirSync(assetsDirectory).find(
  (fileName) => /^index-.*\.js$/.test(fileName),
)
if (!javascriptAsset) throw new Error('Production JavaScript asset was not found.')

const bundle = readFileSync(resolve(assetsDirectory, javascriptAsset), 'utf8')
if (!bundle.includes(expectedApiBaseUrl)) {
  throw new Error(`Production bundle does not contain the configured API base URL: ${expectedApiBaseUrl}`)
}
if (/https?:\/\/(?:localhost|127\.0\.0\.1):8000/.test(bundle)) {
  throw new Error('Production bundle contains a localhost backend URL.')
}

console.log(`Production bundle API URL verified: ${expectedApiBaseUrl}`)
