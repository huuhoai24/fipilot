[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectId,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^https://[^/]+/?$')]
    [string]$FrontendOrigin,

    [string]$Region = 'asia-southeast1',
    [string]$ArtifactRepository = 'ai-interview',
    [string]$ImageName = 'backend',
    [string]$ServiceName = 'ai-interview-backend',
    [string]$ServiceAccount = '',
    [string]$ImageTag = '',
    [string]$GeminiSimpleModel = 'gemini-2.5-flash',
    [string]$GeminiComplexModel = 'gemini-2.5-flash',
    [int]$TimeoutSeconds = 300,
    [int]$MaxInstances = 5,
    [int]$MinInstances = 0,
    [int]$Concurrency = 20,
    [string]$Memory = '1Gi',
    [int]$Cpu = 1,
    [switch]$SkipApiEnable,
    [switch]$SkipFirestoreProvision,
    [switch]$SkipBuild
)

$ErrorActionPreference = 'Stop'
$backendDirectory = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not $ServiceAccount) {
    $ServiceAccount = "ai-interview-runtime@$ProjectId.iam.gserviceaccount.com"
}
if (-not $ImageTag) {
    $ImageTag = (Get-Date).ToUniversalTime().ToString('yyyyMMdd-HHmmss')
}
$imageReference = "$Region-docker.pkg.dev/$ProjectId/$ArtifactRepository/${ImageName}:$ImageTag"
$serviceAccountName = $ServiceAccount.Split('@')[0]

function Invoke-Gcloud {
    & gcloud @args
    if ($LASTEXITCODE -ne 0) {
        throw "gcloud command failed: gcloud $($args -join ' ')"
    }
}

function Test-GcloudResource([string[]]$CommandArguments) {
    $previousErrorPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'SilentlyContinue'
        & gcloud @CommandArguments *> $null
        return $LASTEXITCODE -eq 0
    }
    finally {
        $ErrorActionPreference = $previousErrorPreference
    }
}

function ConvertTo-YamlValue([string]$Value) {
    return "'" + $Value.Replace("'", "''") + "'"
}

Invoke-Gcloud config set project $ProjectId

if (-not $SkipApiEnable) {
    Invoke-Gcloud services enable `
        run.googleapis.com `
        artifactregistry.googleapis.com `
        cloudbuild.googleapis.com `
        aiplatform.googleapis.com `
        firestore.googleapis.com `
        firebase.googleapis.com `
        identitytoolkit.googleapis.com `
        --project=$ProjectId
}

if (-not (Test-GcloudResource @(
    'artifacts', 'repositories', 'describe', $ArtifactRepository,
    "--location=$Region", "--project=$ProjectId"
))) {
    Invoke-Gcloud artifacts repositories create $ArtifactRepository `
        --repository-format=docker `
        --location=$Region `
        --description='AI Interview production images' `
        --project=$ProjectId
}

if (-not (Test-GcloudResource @(
    'iam', 'service-accounts', 'describe', $ServiceAccount, "--project=$ProjectId"
))) {
    Invoke-Gcloud iam service-accounts create $serviceAccountName `
        --display-name='AI Interview Cloud Run runtime' `
        --project=$ProjectId
}

foreach ($role in @(
    'roles/aiplatform.user',
    'roles/datastore.user',
    'roles/firebaseauth.viewer',
    'roles/logging.logWriter'
)) {
    Invoke-Gcloud projects add-iam-policy-binding $ProjectId `
        --member="serviceAccount:$ServiceAccount" `
        --role=$role `
        --format=none `
        --quiet
}

$buildServiceAccount = & gcloud builds get-default-service-account `
    --project=$ProjectId `
    --format='value(serviceAccountEmail)'
if ($LASTEXITCODE -ne 0 -or -not $buildServiceAccount) {
    throw 'Cloud Build default service account could not be determined.'
}
Invoke-Gcloud projects add-iam-policy-binding $ProjectId `
    --member="serviceAccount:$buildServiceAccount" `
    --role='roles/cloudbuild.builds.builder' `
    --format=none `
    --quiet

if (-not $SkipFirestoreProvision) {
    if (-not (Test-GcloudResource @(
        'firestore', 'databases', 'describe', '--database=(default)',
        "--project=$ProjectId"
    ))) {
        Invoke-Gcloud firestore databases create `
            --database='(default)' `
            --location=$Region `
            --type=firestore-native `
            --delete-protection `
            --project=$ProjectId `
            --quiet
    }
}

if (-not $SkipBuild) {
    Invoke-Gcloud builds submit $backendDirectory `
        --tag=$imageReference `
        --project=$ProjectId
}

$environmentFile = New-TemporaryFile
try {
    $environment = [ordered]@{
        APP_ENV = 'production'
        DEBUG = 'false'
        LOG_LEVEL = 'INFO'
        GOOGLE_CLOUD_PROJECT = $ProjectId
        GOOGLE_CLOUD_LOCATION = $Region
        GEMINI_SIMPLE_MODEL = $GeminiSimpleModel
        GEMINI_COMPLEX_MODEL = $GeminiComplexModel
        REPOSITORY_BACKEND = 'firestore'
        FIRESTORE_DATABASE = '(default)'
        FIRESTORE_USERS_COLLECTION = 'users'
        FIRESTORE_CANDIDATES_COLLECTION = 'candidates'
        FIRESTORE_INTERVIEWS_COLLECTION = 'interviews'
        AUTH_ENABLED = 'true'
        AUTH_PROVIDER = 'firebase'
        FIREBASE_PROJECT_ID = $ProjectId
        CORS_ALLOWED_ORIGINS = $FrontendOrigin.TrimEnd('/')
    }
    $lines = $environment.GetEnumerator() | ForEach-Object {
        "$($_.Key): $(ConvertTo-YamlValue ([string]$_.Value))"
    }
    [System.IO.File]::WriteAllLines($environmentFile.FullName, $lines)

    Invoke-Gcloud run deploy $ServiceName `
        --image=$imageReference `
        --region=$Region `
        --platform=managed `
        --service-account=$ServiceAccount `
        --execution-environment=gen2 `
        --port=8080 `
        --timeout="${TimeoutSeconds}s" `
        --max-instances=$MaxInstances `
        --min-instances=$MinInstances `
        --concurrency=$Concurrency `
        --memory=$Memory `
        --cpu=$Cpu `
        --env-vars-file=$($environmentFile.FullName) `
        --allow-unauthenticated `
        --project=$ProjectId `
        --quiet
}
finally {
    Remove-Item -LiteralPath $environmentFile.FullName -Force -ErrorAction SilentlyContinue
}

$serviceUrl = & gcloud run services describe $ServiceName `
    --region=$Region `
    --project=$ProjectId `
    --format='value(status.url)'
if ($LASTEXITCODE -ne 0 -or -not $serviceUrl) {
    throw 'Cloud Run deployed but its service URL could not be read.'
}

Write-Output "Image: $imageReference"
Write-Output "Service URL: $serviceUrl"
$venvPython = Join-Path $backendDirectory 'venv\Scripts\python.exe'
if (Test-Path -LiteralPath $venvPython) {
    $pythonCommand = $venvPython
}
else {
    $pythonCommand = (Get-Command python3 -CommandType Application -ErrorAction SilentlyContinue).Source
    if (-not $pythonCommand) {
        $pythonCommand = (Get-Command python -CommandType Application -ErrorAction SilentlyContinue).Source
    }
}
if (-not $pythonCommand) {
    throw 'Python is required to run the post-deployment smoke test.'
}
& $pythonCommand (Join-Path $PSScriptRoot 'smoke_test.py') $serviceUrl
if ($LASTEXITCODE -ne 0) {
    throw 'Post-deployment smoke test failed.'
}
