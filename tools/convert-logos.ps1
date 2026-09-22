Add-Type -AssemblyName PresentationCore

function Convert-WhiteBackgroundToTransparent {
    param(
        [Parameter(Mandatory = $true)][string]$InputPath,
        [Parameter(Mandatory = $true)][string]$OutputPath,
        [switch]$MakeDarkPixelsWhite
    )

    $resolvedInput = (Resolve-Path -LiteralPath $InputPath).Path
    $stream = [System.IO.File]::OpenRead($resolvedInput)
    try {
        $decoder = [System.Windows.Media.Imaging.BitmapDecoder]::Create(
            $stream,
            [System.Windows.Media.Imaging.BitmapCreateOptions]::PreservePixelFormat,
            [System.Windows.Media.Imaging.BitmapCacheOption]::OnLoad
        )
        $source = $decoder.Frames[0]
    }
    finally {
        $stream.Dispose()
    }

    $converted = New-Object System.Windows.Media.Imaging.FormatConvertedBitmap
    $converted.BeginInit()
    $converted.Source = $source
    $converted.DestinationFormat = [System.Windows.Media.PixelFormats]::Bgra32
    $converted.EndInit()

    $width = $converted.PixelWidth
    $height = $converted.PixelHeight
    $stride = $width * 4
    $pixels = New-Object byte[] ($stride * $height)
    $converted.CopyPixels($pixels, $stride, 0)

    $minX = $width
    $minY = $height
    $maxX = -1
    $maxY = -1

    for ($y = 0; $y -lt $height; $y++) {
        for ($x = 0; $x -lt $width; $x++) {
            $i = ($y * $stride) + ($x * 4)
            $b = [int]$pixels[$i]
            $g = [int]$pixels[$i + 1]
            $r = [int]$pixels[$i + 2]

            # Recover antialiased artwork that was composited over white.
            $minimum = [Math]::Min($r, [Math]::Min($g, $b))
            $alpha = 255 - $minimum
            if ($alpha -lt 4) { $alpha = 0 }

            if ($alpha -gt 0) {
                $a = $alpha / 255.0
                $rr = [Math]::Max(0, [Math]::Min(255, [Math]::Round(($r - (255 * (1 - $a))) / $a)))
                $gg = [Math]::Max(0, [Math]::Min(255, [Math]::Round(($g - (255 * (1 - $a))) / $a)))
                $bb = [Math]::Max(0, [Math]::Min(255, [Math]::Round(($b - (255 * (1 - $a))) / $a)))

                $isYellow = ($rr -gt 145 -and $gg -gt 80 -and $bb -lt 90 -and ($rr - $bb) -gt 90)
                if ($isYellow) {
                    # Normalize JPEG colour noise without changing the source artwork geometry.
                    $rr = 247
                    $gg = 173
                    $bb = 0
                }
                elseif ($MakeDarkPixelsWhite) {
                    $rr = 255
                    $gg = 255
                    $bb = 255
                }
                else {
                    $average = [Math]::Round(($rr + $gg + $bb) / 3)
                    if ($average -lt 38) {
                        $rr = 16
                        $gg = 24
                        $bb = 32
                    }
                    else {
                        $rr = $average
                        $gg = $average
                        $bb = $average
                    }
                }

                $pixels[$i] = [byte]$bb
                $pixels[$i + 1] = [byte]$gg
                $pixels[$i + 2] = [byte]$rr
                $pixels[$i + 3] = [byte]$alpha

                if ($alpha -gt 12) {
                    if ($x -lt $minX) { $minX = $x }
                    if ($x -gt $maxX) { $maxX = $x }
                    if ($y -lt $minY) { $minY = $y }
                    if ($y -gt $maxY) { $maxY = $y }
                }
            }
            else {
                $pixels[$i] = 0
                $pixels[$i + 1] = 0
                $pixels[$i + 2] = 0
                $pixels[$i + 3] = 0
            }
        }
    }

    if ($maxX -lt $minX -or $maxY -lt $minY) { throw "No artwork found in $InputPath" }

    $padding = 4
    $minX = [Math]::Max(0, $minX - $padding)
    $minY = [Math]::Max(0, $minY - $padding)
    $maxX = [Math]::Min($width - 1, $maxX + $padding)
    $maxY = [Math]::Min($height - 1, $maxY + $padding)
    $cropWidth = $maxX - $minX + 1
    $cropHeight = $maxY - $minY + 1
    $cropStride = $cropWidth * 4
    $cropped = New-Object byte[] ($cropStride * $cropHeight)

    for ($row = 0; $row -lt $cropHeight; $row++) {
        [Array]::Copy($pixels, (($minY + $row) * $stride) + ($minX * 4), $cropped, $row * $cropStride, $cropStride)
    }

    $bitmap = [System.Windows.Media.Imaging.BitmapSource]::Create(
        $cropWidth,
        $cropHeight,
        96,
        96,
        [System.Windows.Media.PixelFormats]::Bgra32,
        $null,
        $cropped,
        $cropStride
    )

    $encoder = New-Object System.Windows.Media.Imaging.PngBitmapEncoder
    $encoder.Frames.Add([System.Windows.Media.Imaging.BitmapFrame]::Create($bitmap))
    $outputDirectory = Split-Path -Parent $OutputPath
    if (-not (Test-Path -LiteralPath $outputDirectory)) {
        New-Item -ItemType Directory -Path $outputDirectory | Out-Null
    }
    $output = [System.IO.File]::Create($OutputPath)
    try { $encoder.Save($output) } finally { $output.Dispose() }
}

$projectRoot = Split-Path -Parent $PSScriptRoot
$assetDirectory = Join-Path $projectRoot 'assets'

Convert-WhiteBackgroundToTransparent `
    -InputPath (Join-Path $projectRoot '793286DF-EA9E-4F52-B235-EC30A1CAAFA0.jpg') `
    -OutputPath (Join-Path $assetDirectory 'embuilded-logo.png')

Convert-WhiteBackgroundToTransparent `
    -InputPath (Join-Path $projectRoot 'FDF655E1-1CC3-4918-B33C-6FCEE3D227E3.jpg') `
    -OutputPath (Join-Path $assetDirectory 'traci-logo.png')

Convert-WhiteBackgroundToTransparent `
    -InputPath (Join-Path $projectRoot 'FDF655E1-1CC3-4918-B33C-6FCEE3D227E3.jpg') `
    -OutputPath (Join-Path $assetDirectory 'traci-logo-on-dark.png') `
    -MakeDarkPixelsWhite
