$ErrorActionPreference = 'Stop'

$repositoryRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$architectureRoot = Join-Path $repositoryRoot 'docs\architecture'
$diagramRoot = Join-Path $architectureRoot 'diagrams'
$errors = [System.Collections.Generic.List[string]]::new()

$files = @(Get-ChildItem -LiteralPath $diagramRoot -Filter '*.mmd' | Sort-Object Name)
if ($files.Count -ne 95) {
    $errors.Add("Expected 95 standalone Mermaid files; found $($files.Count).")
}

$expectedNumbers = 1..95 | ForEach-Object { $_.ToString('00') }
$actualNumbers = @($files | ForEach-Object { $_.BaseName.Substring(0, 2) })
foreach ($number in $expectedNumbers) {
    if ($number -notin $actualNumbers) {
        $errors.Add("Missing diagram number $number.")
    }
}

$allowedDeclarations = 'flowchart', 'sequenceDiagram', 'stateDiagram-v2', 'classDiagram', 'erDiagram'
$titles = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
$typeCounts = @{}

foreach ($file in $files) {
    $content = Get-Content -LiteralPath $file.FullName -Raw
    $lines = @($content -split "`r?`n")
    $declaration = $lines | Where-Object { $_.Trim() -and -not $_.Trim().StartsWith('%%') } | Select-Object -First 1
    $declarationType = if ($declaration) { ($declaration.Trim() -split '\s+')[0] } else { '' }

    if ($declarationType -notin $allowedDeclarations) {
        $errors.Add("$($file.Name): unsupported or missing Mermaid declaration '$declarationType'.")
    } else {
        $typeCounts[$declarationType] = 1 + [int]$typeCounts[$declarationType]
    }
    if ($lines.Count -lt 3 -or -not $lines[0].StartsWith('%% ')) {
        $errors.Add("$($file.Name): missing title comment.")
    } elseif (-not $titles.Add($lines[0])) {
        $errors.Add("$($file.Name): duplicate title '$($lines[0])'.")
    }
    if ($content -notmatch '(?m)^%% Status: .*(IMPLEMENTED|PARTIAL|SPEC-PENDING|UNKNOWN)') {
        $errors.Add("$($file.Name): missing recognized status label.")
    }
    if ($content -notmatch '(?m)^%% Evidence: \S') {
        $errors.Add("$($file.Name): missing source evidence.")
    }
    if ($content.Contains('```') -or $content -match '<\/?[a-zA-Z][^>]*>') {
        $errors.Add("$($file.Name): standalone source contains a Markdown fence or HTML tag.")
    }
    $delimiterPairs = @(@('(', ')'), @('[', ']'))
    if ($declarationType -ne 'erDiagram') {
        $delimiterPairs += ,@('{', '}')
    }
    foreach ($pair in $delimiterPairs) {
        $left = ([regex]::Matches($content, [regex]::Escape($pair[0]))).Count
        $right = ([regex]::Matches($content, [regex]::Escape($pair[1]))).Count
        if ($left -ne $right) {
            $errors.Add("$($file.Name): unbalanced $($pair[0])/$($pair[1]) delimiters ($left/$right).")
        }
    }
    $quoteCount = ([regex]::Matches($content, '"')).Count
    if (($quoteCount % 2) -ne 0) {
        $errors.Add("$($file.Name): unbalanced double quotes ($quoteCount).")
    }
}

$indexPath = Join-Path $architectureRoot 'DIAGRAM_INDEX.md'
$suitePath = Join-Path $architectureRoot 'DIAGRAMS.md'
$indexRows = @(Get-Content -LiteralPath $indexPath | Select-String '^\| [0-9]+ \|').Count
$suiteHeadings = @(Get-Content -LiteralPath $suitePath | Select-String '^## [0-9]+\. ').Count
$mermaidFences = @(Get-Content -LiteralPath $suitePath | Select-String '^```mermaid$').Count
$evidenceLines = @(Get-Content -LiteralPath $suitePath | Select-String '^- \*\*Code evidence:\*\* ').Count

if ($indexRows -ne 95) { $errors.Add("DIAGRAM_INDEX.md has $indexRows diagram rows; expected 95.") }
if ($suiteHeadings -ne 95) { $errors.Add("DIAGRAMS.md has $suiteHeadings numbered sections; expected 95.") }
if ($mermaidFences -ne 95) { $errors.Add("DIAGRAMS.md has $mermaidFences Mermaid fences; expected 95.") }
if ($evidenceLines -ne 95) { $errors.Add("DIAGRAMS.md has $evidenceLines evidence fields; expected 95.") }

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

[pscustomobject]@{
    Result = 'PASS'
    StandaloneDiagrams = $files.Count
    IndexedDiagrams = $indexRows
    NarrativeSections = $suiteHeadings
    MermaidBlocks = $mermaidFences
    EvidenceFields = $evidenceLines
    DiagramTypes = $typeCounts
    Check = 'Static manifest, declaration, delimiter, metadata, and coverage validation'
} | ConvertTo-Json -Depth 3
