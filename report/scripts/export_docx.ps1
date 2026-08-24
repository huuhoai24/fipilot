$ErrorActionPreference = 'Stop'

$reportRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$exporter = Join-Path $PSScriptRoot 'export_docx.py'

python $exporter
if ($LASTEXITCODE -ne 0) {
  throw 'DOCX export failed.'
}

$output = Join-Path $reportRoot 'Final_report.docx'
if (-not (Test-Path -LiteralPath $output)) {
  throw "DOCX output was not created: $output"
}

Write-Host "DOCX export PASS: $output ($((Get-Item -LiteralPath $output).Length) bytes)"
