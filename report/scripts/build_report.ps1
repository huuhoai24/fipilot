$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$reportRoot = Join-Path $repoRoot 'report'

& (Join-Path $PSScriptRoot 'render_diagrams.ps1')

function Resolve-MiKTeXTool([string]$name) {
  $command = Get-Command $name -ErrorAction SilentlyContinue
  if ($command) { return $command.Source }
  $candidate = Join-Path $env:LOCALAPPDATA "Programs\MiKTeX\miktex\bin\x64\$name.exe"
  if (Test-Path -LiteralPath $candidate) { return $candidate }
  throw "Required MiKTeX tool not found: $name"
}

$xelatex = Resolve-MiKTeXTool 'xelatex'
$biber = Resolve-MiKTeXTool 'biber'

Push-Location $reportRoot
try {
  & $xelatex --enable-installer -interaction=batchmode -halt-on-error Final_report.tex
  if ($LASTEXITCODE -ne 0) { throw 'Initial XeLaTeX pass failed.' }
  & $biber Final_report
  if ($LASTEXITCODE -ne 0) { throw 'Biber pass failed.' }
  & $xelatex --enable-installer -interaction=batchmode -halt-on-error Final_report.tex
  if ($LASTEXITCODE -ne 0) { throw 'Second XeLaTeX pass failed.' }
  & $xelatex --enable-installer -interaction=batchmode -halt-on-error Final_report.tex
  if ($LASTEXITCODE -ne 0) { throw 'Final XeLaTeX pass failed.' }

  $log = Get-Content -Raw -LiteralPath 'Final_report.log'
  $blocking = @(
    'undefined references', 'multiply-defined labels', 'Empty bibliography',
    'Citation .* undefined', 'Reference .* undefined',
    'LaTeX Error', 'Package .* Error'
  )
  foreach ($pattern in $blocking) {
    if ($log -match $pattern) { throw "Blocking LaTeX log pattern: $pattern" }
  }
  foreach ($match in [regex]::Matches($log, 'Overfull \\hbox \(([0-9.]+)pt')) {
    if ([double]$match.Groups[1].Value -gt 10.0) {
      throw "Major horizontal overflow: $($match.Groups[1].Value)pt"
    }
  }
  if (-not (Test-Path -LiteralPath 'Final_report.pdf')) {
    throw 'Final_report.pdf was not produced.'
  }
  $pdf = Get-Item -LiteralPath 'Final_report.pdf'
  Write-Host "Report build PASS: $($pdf.FullName) ($($pdf.Length) bytes)"
}
finally {
  Pop-Location
}
