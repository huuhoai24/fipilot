$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$diagramRoot = Join-Path $repoRoot 'report\diagrams'
$outputRoot = Join-Path $repoRoot 'report\figures'
New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null

$figures = @(
  '01-system-context', '02-runtime-pipeline', '03-resume-processing',
  '04-candidate-profile', '05-lexical-retrieval', '06-agent-flow',
  '07-answer-processing', '08-text-interview', '09-voice-interview',
  '10-persistence-model', '11-security-boundary', '12-frontend-flow',
  '13-test-layers'
)

foreach ($name in $figures) {
  $source = Join-Path $diagramRoot ($name + '.mmd')
  $target = Join-Path $outputRoot ($name + '.png')
  if (-not (Test-Path -LiteralPath $source)) { throw "Missing diagram source: $source" }
  & npx --yes '@mermaid-js/mermaid-cli@11.12.0' -i $source -o $target -b white -w 2200 -s 3
  if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $target)) {
    throw "Mermaid render failed: $name"
  }
}

Write-Host "Rendered $($figures.Count) as-built diagrams to $outputRoot"
