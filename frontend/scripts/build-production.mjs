import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { spawnSync } from 'node:child_process'

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

function runNodeScript(script, args = []) {
  const result = spawnSync(process.execPath, [script, ...args], {
    cwd: frontendRoot,
    env: buildEnvironment,
    stdio: 'inherit',
  })
  if (result.status !== 0) process.exit(result.status ?? 1)
}

const frontendRoot = resolve(import.meta.dirname, '..')
const productionEnvironment = readEnvFile(resolve(frontendRoot, '.env.production'))
const requiredVariables = [
  'VITE_API_BASE_URL',
  'VITE_FIREBASE_API_KEY',
  'VITE_FIREBASE_AUTH_DOMAIN',
  'VITE_FIREBASE_PROJECT_ID',
  'VITE_FIREBASE_APP_ID',
]
const missingVariables = requiredVariables.filter(
  (name) => !productionEnvironment[name]?.trim(),
)
if (missingVariables.length > 0) {
  throw new Error(`Missing production environment variables: ${missingVariables.join(', ')}`)
}
if (!productionEnvironment.VITE_API_BASE_URL.startsWith('https://')) {
  throw new Error('VITE_API_BASE_URL must use HTTPS in production.')
}

const buildEnvironment = {
  ...process.env,
  ...productionEnvironment,
  VITE_LOCAL_BUILD: 'false',
}

runNodeScript(resolve(frontendRoot, 'node_modules', 'typescript', 'bin', 'tsc'), ['-b'])
runNodeScript(resolve(frontendRoot, 'node_modules', 'vite', 'bin', 'vite.js'), [
  'build',
  '--config',
  'vite.config.ts',
  '--mode',
  'production',
])
runNodeScript(resolve(frontendRoot, 'scripts', 'verify-production-build.mjs'))
