param(
    [string]$ProjectId = "",
    [string]$Database = "(default)",
    [string]$Collection = "interview_knowledge_chunks",
    [string]$VectorField = "embedding",
    [ValidateRange(1, 2048)]
    [int]$Dimensions = 768
)

$ErrorActionPreference = "Stop"

if (-not $ProjectId) {
    $ProjectId = (gcloud config get-value project 2>$null).Trim()
}
if (-not $ProjectId) {
    throw "No Google Cloud project is configured. Pass -ProjectId explicitly."
}

$fieldConfig = "field-path=$VectorField,vector-config={dimension=$Dimensions,flat}"

Write-Host "Creating Firestore vector index"
Write-Host "Project: $ProjectId"
Write-Host "Database: $Database"
Write-Host "Collection: $Collection"
Write-Host "Field: $VectorField ($Dimensions dimensions)"

$existingJson = & gcloud firestore indexes composite list `
    --project=$ProjectId `
    --database=$Database `
    --format=json
if ($LASTEXITCODE -ne 0) {
    throw "Unable to list existing Firestore indexes."
}
$existingIndexes = $existingJson | ConvertFrom-Json
$matchingIndex = $existingIndexes | Where-Object {
    $_.name -match "/collectionGroups/$([regex]::Escape($Collection))/indexes/" -and
    ($_.fields | Where-Object {
        $_.fieldPath -eq $VectorField -and
        $_.vectorConfig.dimension -eq $Dimensions
    })
} | Select-Object -First 1
if ($matchingIndex) {
    $indexId = ($matchingIndex.name -split '/')[-1]
    Write-Host "Matching index already exists: $indexId ($($matchingIndex.state))"
    exit 0
}

& gcloud firestore indexes composite create `
    --project=$ProjectId `
    --database=$Database `
    --collection-group=$Collection `
    --query-scope=COLLECTION `
    --field-config=$fieldConfig `
    --async

if ($LASTEXITCODE -ne 0) {
    throw "Firestore vector index creation failed with exit code $LASTEXITCODE."
}
