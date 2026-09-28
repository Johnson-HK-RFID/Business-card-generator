param(
  [string]$Workspace = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
$outputDirectory = Join-Path $Workspace 'service-label-variants'
$sourcePath = Join-Path $outputDirectory 'service-label-classic-traci.svg'
$logoDirectory = Join-Path $Workspace 'logo-svg'
$templateSvg = Get-Content -Raw -LiteralPath $sourcePath

function Get-SvgBody {
  param([string]$Path)
  $content = Get-Content -Raw -LiteralPath $Path
  $content = $content -replace '^\s*<\?xml[^>]*\?>\s*', ''
  if ($content -notmatch '(?s)^\s*<svg\b[^>]*>(.*)</svg>\s*$') {
    throw "Unable to read SVG body: $Path"
  }
  return $Matches[1].Trim()
}

function New-NestedLogo {
  param(
    [string]$Id,
    [string]$Label,
    [string]$LogoPath,
    [string]$ViewBox,
    [int]$X,
    [int]$Y,
    [int]$Width,
    [int]$Height
  )
  $body = Get-SvgBody -Path $LogoPath
  return @"
  <g id="$Id" aria-label="$Label">
    <svg x="$X" y="$Y" width="$Width" height="$Height" viewBox="$ViewBox"
         preserveAspectRatio="xMinYMin meet" overflow="visible">
      $body
    </svg>
  </g>
"@
}

function New-ServiceLabelVariant {
  param(
    [string]$OutputName,
    [string]$BrandFile,
    [string]$BrandViewBox,
    [int[]]$BrandBox,
    [string]$PartnerFile,
    [string]$PartnerViewBox,
    [int[]]$PartnerBox
  )

  $svg = $templateSvg
  $brand = New-NestedLogo -Id 'brand-logo' -Label 'Replaceable Embuilded logo' `
    -LogoPath (Join-Path $logoDirectory $BrandFile) -ViewBox $BrandViewBox `
    -X $BrandBox[0] -Y $BrandBox[1] -Width $BrandBox[2] -Height $BrandBox[3]
  $partner = New-NestedLogo -Id 'partner-logo' -Label 'Replaceable TRACI logo' `
    -LogoPath (Join-Path $logoDirectory $PartnerFile) -ViewBox $PartnerViewBox `
    -X $PartnerBox[0] -Y $PartnerBox[1] -Width $PartnerBox[2] -Height $PartnerBox[3]

  $svg = [regex]::Replace(
    $svg,
    '(?s)  <!-- Embedded replaceable vector logo\. -->\s*<g id="brand-logo".*?</g>\s*(?=\s*<g id="powered-lockup">)',
    "  <!-- Embedded replaceable vector logo. -->`r`n$brand`r`n",
    1
  )
  $svg = [regex]::Replace(
    $svg,
    '(?s)    <!-- Embedded replaceable partner logo\. -->\s*(?:<svg id="partner-logo".*?</svg>|<g id="partner-logo".*?</g>\s*(?=</g>))',
    "    <!-- Embedded replaceable partner logo. -->`r`n$partner",
    1
  )
  $svg = $svg -replace '<title>Editable EmbuilDed service label</title>', '<title>Editable Embuilded service label</title>'
  $svg = $svg -replace '#ffc400', '#F5B218'
  if (-not (Test-Path -LiteralPath $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory | Out-Null
  }
  $outputPath = Join-Path $outputDirectory $OutputName
  [System.IO.File]::WriteAllText($outputPath, $svg, [System.Text.UTF8Encoding]::new($false))
}

New-ServiceLabelVariant `
  -OutputName 'service-label-classic-traci.svg' `
  -BrandFile 'embuilded-horizontal-lockup.svg' -BrandViewBox '0 0 1200 360' -BrandBox @(70, 72, 900, 270) `
  -PartnerFile 'traci-digital-wordmark.svg' -PartnerViewBox '0 0 1065 220' -PartnerBox @(470, 315, 420, 87)

New-ServiceLabelVariant `
  -OutputName 'service-label-classic-traci-circuit.svg' `
  -BrandFile 'embuilded-horizontal-lockup.svg' -BrandViewBox '0 0 1200 360' -BrandBox @(70, 72, 900, 270) `
  -PartnerFile 'traci-circuit-lockup.svg' -PartnerViewBox '0 0 1400 400' -PartnerBox @(520, 300, 390, 111)

New-ServiceLabelVariant `
  -OutputName 'service-label-building-traci.svg' `
  -BrandFile 'building-embuilded-horizontal.svg' -BrandViewBox '0 0 1300 390' -BrandBox @(62, 63, 910, 273) `
  -PartnerFile 'traci-digital-wordmark.svg' -PartnerViewBox '0 0 1065 220' -PartnerBox @(470, 315, 420, 87)

New-ServiceLabelVariant `
  -OutputName 'service-label-building-traci-circuit.svg' `
  -BrandFile 'building-embuilded-horizontal.svg' -BrandViewBox '0 0 1300 390' -BrandBox @(62, 63, 910, 273) `
  -PartnerFile 'traci-circuit-lockup.svg' -PartnerViewBox '0 0 1400 400' -PartnerBox @(520, 300, 390, 111)
