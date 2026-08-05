[CmdletBinding()]
param(
    [string]$BindHost = "127.0.0.1",
    [ValidateRange(1, 65535)]
    [int]$Port = 8000,
    [switch]$Reload
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$backendRoot = Join-Path $repoRoot "backend"
$envFile = if ($env:BACKEND_ENV_FILE) {
    $env:BACKEND_ENV_FILE
} else {
    Join-Path $backendRoot ".env.local"
}

if (-not (Test-Path -LiteralPath $envFile -PathType Leaf)) {
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
    $name = $parts[0].Trim().TrimStart([char]0xFEFF)
    $value = $parts[1].Trim().Trim('"').Trim("'")
    [Environment]::SetEnvironmentVariable($name, $value, "Process")
}

$python = @(
    (Join-Path $backendRoot ".venv\Scripts\python.exe"),
    (Join-Path $backendRoot "venv\Scripts\python.exe")
) | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1

if (-not $python) {
    throw "Backend virtual environment not found. Create backend/.venv first."
}

$listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
    Select-Object -First 1
if ($listener) {
    throw "Port $Port is already in use by process $($listener.OwningProcess). Stop it or run with -Port <another-port>."
}

$uvicornArgs = @(
    "-m", "uvicorn",
    "gateway.main:app",
    "--host", $BindHost,
    "--port", $Port.ToString()
)
if ($Reload) {
    $uvicornArgs += @("--reload", "--reload-dir", $backendRoot)
}

Write-Host "Starting Fipilot backend"
Write-Host "  Python: $python"
Write-Host "  Env:    $envFile"
Write-Host "  URL:    http://${BindHost}:$Port"
Write-Host "  Reload: $Reload"

Push-Location $backendRoot
try {
    & $python @uvicornArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Backend exited with code $LASTEXITCODE."
    }
} finally {
    Pop-Location
}
