$ErrorActionPreference = "Stop"
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$backendRoot = Join-Path $repoRoot "backend"
$envFile = if ($env:BACKEND_ENV_FILE) {
    $env:BACKEND_ENV_FILE
} else {
    Join-Path $backendRoot ".env.local"
}

if (-not (Test-Path -LiteralPath $envFile)) {
    throw "Missing $envFile. Copy backend/.env.local.example to backend/.env.local first."
}

foreach ($line in Get-Content -LiteralPath $envFile) {
    $trimmed = $line.Trim()
    if (-not $trimmed -or $trimmed.StartsWith("#")) {
        continue
    }
    $parts = $trimmed.Split("=", 2)
    if ($parts.Count -ne 2) {
        throw "Invalid environment entry in ${envFile}: $trimmed"
    }
    $name = $parts[0].Trim()
    $value = $parts[1].Trim().Trim('"').Trim("'")
    [Environment]::SetEnvironmentVariable($name, $value, "Process")
}

$activate = @(
    (Join-Path $backendRoot ".venv\Scripts\Activate.ps1"),
    (Join-Path $backendRoot "venv\Scripts\Activate.ps1")
) | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1

if (-not $activate) {
    throw "Backend virtual environment not found. Create backend/.venv first."
}

Set-Location $backendRoot
. $activate
python -m uvicorn gateway.main:app --reload --host 0.0.0.0 --port 8000
