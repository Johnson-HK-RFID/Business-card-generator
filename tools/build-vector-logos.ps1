Add-Type -AssemblyName PresentationCore

$projectRoot = Split-Path -Parent $PSScriptRoot
$tracer = Join-Path $PSScriptRoot 'vtracer-bin/vtracer.exe'
if (-not (Test-Path -LiteralPath $tracer)) { throw 'Download the VTracer Windows CLI into tools/vtracer-bin first.' }
$work = Join-Path $PSScriptRoot 'vtracer-work'
New-Item -ItemType Directory -Force -Path $work | Out-Null

function Write-ColorMask {
    param([string]$InputPath, [string]$OutputPath, [ValidateSet('yellow','other')][string]$Layer)
    $stream = [System.IO.File]::OpenRead($InputPath)
    try {
        $decoder = [System.Windows.Media.Imaging.BitmapDecoder]::Create($stream, [System.Windows.Media.Imaging.BitmapCreateOptions]::PreservePixelFormat, [System.Windows.Media.Imaging.BitmapCacheOption]::OnLoad)
        $source = $decoder.Frames[0]
    } finally { $stream.Dispose() }
    $converted = New-Object System.Windows.Media.Imaging.FormatConvertedBitmap
    $converted.BeginInit(); $converted.Source = $source; $converted.DestinationFormat = [System.Windows.Media.PixelFormats]::Bgra32; $converted.EndInit()
    $width = $converted.PixelWidth; $height = $converted.PixelHeight; $stride = $width * 4
    $pixels = New-Object byte[] ($stride * $height); $converted.CopyPixels($pixels, $stride, 0)
    for ($i = 0; $i -lt $pixels.Length; $i += 4) {
        $b=[int]$pixels[$i]; $g=[int]$pixels[$i+1]; $r=[int]$pixels[$i+2]; $a=[int]$pixels[$i+3]
        $isYellow = ($r -gt 150 -and $g -gt 80 -and $b -lt 100 -and ($r-$b) -gt 90)
        $selected = $a -gt 72 -and (($Layer -eq 'yellow' -and $isYellow) -or ($Layer -eq 'other' -and -not $isYellow))
        $value = if($selected){0}else{255}
        $pixels[$i]=[byte]$value; $pixels[$i+1]=[byte]$value; $pixels[$i+2]=[byte]$value; $pixels[$i+3]=255
    }
    $bitmap = [System.Windows.Media.Imaging.BitmapSource]::Create($width,$height,96,96,[System.Windows.Media.PixelFormats]::Bgra32,$null,$pixels,$stride)
    $encoder = New-Object System.Windows.Media.Imaging.PngBitmapEncoder
    $encoder.Frames.Add([System.Windows.Media.Imaging.BitmapFrame]::Create($bitmap))
    $output = [System.IO.File]::Create($OutputPath)
    try {$encoder.Save($output)} finally {$output.Dispose()}
    return @($width,$height)
}

function Trace-TwoColorLogo {
    param([string]$InputName,[string]$OutputName,[string]$BaseColor)
    $input = Join-Path $projectRoot ('assets/' + $InputName)
    $baseMask = Join-Path $work ($OutputName + '-base.png')
    $yellowMask = Join-Path $work ($OutputName + '-yellow.png')
    $dimensions = Write-ColorMask $input $baseMask 'other'
    Write-ColorMask $input $yellowMask 'yellow' | Out-Null
    $baseSvg = Join-Path $work ($OutputName + '-base.svg')
    $yellowSvg = Join-Path $work ($OutputName + '-yellow.svg')
    & $tracer $baseMask $baseSvg --clustering bw --mode spline --threshold 128 --filter-speckle 24 --simplify 1.8 --path-precision 2 --optimize 2
    if ($LASTEXITCODE -ne 0) { throw 'Base layer tracing failed.' }
    & $tracer $yellowMask $yellowSvg --clustering bw --mode spline --threshold 128 --filter-speckle 24 --simplify 1.8 --path-precision 2 --optimize 2
    if ($LASTEXITCODE -ne 0) { throw 'Yellow layer tracing failed.' }
    $base = [System.IO.File]::ReadAllText($baseSvg)
    $yellow = [System.IO.File]::ReadAllText($yellowSvg)
    $baseBody = [regex]::Match($base,'<svg[^>]*>(?<body>[\s\S]*?)</svg>').Groups['body'].Value -replace 'fill="#[0-9A-Fa-f]{6}"',('fill="'+$BaseColor+'"')
    $yellowBody = [regex]::Match($yellow,'<svg[^>]*>(?<body>[\s\S]*?)</svg>').Groups['body'].Value -replace 'fill="#[0-9A-Fa-f]{6}"','fill="#F7AD00"'
    $svg = '<?xml version="1.0" encoding="UTF-8"?>' + [Environment]::NewLine + '<svg xmlns="http://www.w3.org/2000/svg" width="' + $dimensions[0] + '" height="' + $dimensions[1] + '" viewBox="0 0 ' + $dimensions[0] + ' ' + $dimensions[1] + '">' + $baseBody + $yellowBody + '</svg>'
    [System.IO.File]::WriteAllText((Join-Path $projectRoot ('assets/' + $OutputName + '.svg')),$svg,(New-Object System.Text.UTF8Encoding($false)))
}

Trace-TwoColorLogo 'embuilded-logo.png' 'embuilded-logo' '#101820'
Trace-TwoColorLogo 'traci-logo-on-dark.png' 'traci-logo-on-dark' '#FFFFFF'
& (Join-Path $PSScriptRoot 'build-vector-resources.ps1')
