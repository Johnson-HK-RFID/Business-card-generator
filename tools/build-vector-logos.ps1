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
    & $tracer $baseMask $baseSvg --clustering bw --mode spline --threshold 128 --filter-speckle 32 --simplify 4 --path-precision 2 --optimize 2
    if ($LASTEXITCODE -ne 0) { throw 'Base layer tracing failed.' }
    & $tracer $yellowMask $yellowSvg --clustering bw --mode spline --threshold 128 --filter-speckle 32 --simplify 4 --path-precision 2 --optimize 2
    if ($LASTEXITCODE -ne 0) { throw 'Yellow layer tracing failed.' }
    $base = [System.IO.File]::ReadAllText($baseSvg)
    $yellow = [System.IO.File]::ReadAllText($yellowSvg)
    $baseBody = [regex]::Match($base,'<svg[^>]*>(?<body>[\s\S]*?)</svg>').Groups['body'].Value -replace 'fill="#[0-9A-Fa-f]{6}"',('fill="'+$BaseColor+'"')
    $yellowBody = [regex]::Match($yellow,'<svg[^>]*>(?<body>[\s\S]*?)</svg>').Groups['body'].Value -replace 'fill="#[0-9A-Fa-f]{6}"','fill="#F7AD00"'
    if ($OutputName -eq 'embuilded-logo') {
        # Rebuild every visible glyph with deliberate straight segments and smooth Bezier arcs.
        # This removes the small JPEG-pixel dents that remain even in an auto-traced SVG.
        $baseBody = '<g fill="#101820">' +
            '<circle cx="960" cy="174" r="25"/>' +
            '<path d="M610 150h50v65c22-18 55-21 78-6 25 16 38 44 35 74-3 43-32 72-72 72-17 0-32-6-43-18v15h-48V150Zm50 128c0 25 14 40 34 40 21 0 34-16 34-40s-13-39-34-39c-20 0-34 15-34 39Z"/>' +
            '<path d="M781 206h48v82c0 20 8 30 24 30 18 0 27-12 27-35v-77h48v146h-46l-1-16c-12 13-29 19-49 19-34 0-51-22-51-64V206Z"/>' +
            '<path d="M939 206h46v146h-46V206Z"/>' +
            '<path d="M996 150h44v202h-44V150Z"/>' +
            '<path d="M1163 150h50v202h-47l-1-15c-12 12-28 18-46 18-42 0-70-31-70-77 0-45 28-75 69-75 18 0 33 5 45 16v-69Zm-67 128c0 24 14 40 34 40 21 0 34-16 34-40s-13-39-34-39c-20 0-34 15-34 39Z"/>' +
            '<path d="M1305 202c48 0 80 32 80 80v11h-110c4 19 16 29 34 29 14 0 25-6 32-18l37 20c-14 22-38 33-70 33-50 0-84-31-84-77 0-45 34-78 81-78Zm-30 60h61c-4-17-15-27-30-27-16 0-27 10-31 27Z"/>' +
            '<path d="M1509 150h50v202h-49l-1-15c-12 12-28 18-46 18-42 0-70-31-70-77 0-45 28-75 69-75 18 0 34 5 46 16l1-69Zm-68 128c0 24 14 40 34 40 21 0 34-16 34-40s-13-39-34-39c-20 0-34 15-34 39Z"/>' +
            '</g>'
        $yellowBody = '<g fill="#F7AD00"><path d="M12 10H440v108q-25 10-50 0V59H60v311h79v48H12Z"/><path d="M176 136h153v44h-97v40h85v45h-85v43h98v44H176Z"/><path d="M345 206h51l1 16c11-13 26-20 45-20 21 0 36 8 45 24 12-16 29-24 50-24 38 0 57 25 57 75v75h-51v-79c0-23-8-34-23-34-17 0-25 13-25 39v74h-51v-79c0-23-8-34-23-34-17 0-25 13-25 39v74h-51V206Z"/></g>'
    }
    if ($OutputName -eq 'traci-logo-on-dark') {
        # Rebuild all glyphs as clean geometry; no traced JPEG edges remain in the main wordmark.
        $baseBody = '<g fill="#FFFFFF">' +
            '<path d="M79 10H324V40H220V208H182V40H79Z"/>' +
            '<path d="M379 10H548c43 0 68 20 68 54 0 39-29 59-82 59h-31l109 85h-64l-108-96c-8-7-4-17 8-17h88c27 0 40-10 40-30 0-17-13-25-40-25H379V10Zm0 85h37v113h-37V95Z"/>' +
            '<path d="M1278 10v30h-101c-87 0-130 23-130 69 0 47 43 69 130 69h101v30h-106c-109 0-163-33-163-99 0-66 54-99 163-99h106Z"/>' +
            '<path d="M1365 10h44v198h-44Z"/>' +
            '</g>'
        $yellowBody = '<g fill="#F7AD00"><path d="M644 208 785 27Q800 7 819 8q22 1 24 20 1 10-8 22L704 208Z"/><path d="M844 42q9-12 20 1l117 165h-61l-87-121q-15-22 11-45Z"/><rect x="786" y="156" width="52" height="52" rx="4"/></g>'
    }
    $svg = '<?xml version="1.0" encoding="UTF-8"?>' + [Environment]::NewLine + '<svg xmlns="http://www.w3.org/2000/svg" width="' + $dimensions[0] + '" height="' + $dimensions[1] + '" viewBox="0 0 ' + $dimensions[0] + ' ' + $dimensions[1] + '">' + $baseBody + $yellowBody + '</svg>'
    [System.IO.File]::WriteAllText((Join-Path $projectRoot ('assets/' + $OutputName + '.svg')),$svg,(New-Object System.Text.UTF8Encoding($false)))
}

Trace-TwoColorLogo 'embuilded-logo.png' 'embuilded-logo' '#101820'
Trace-TwoColorLogo 'traci-logo-on-dark.png' 'traci-logo-on-dark' '#FFFFFF'
& (Join-Path $PSScriptRoot 'build-vector-resources.ps1')
