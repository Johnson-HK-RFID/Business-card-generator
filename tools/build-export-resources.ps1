# Bundle local resources so file:// export never fetches local images from an iframe.
$projectRoot = Split-Path -Parent $PSScriptRoot
$resources = @{
    css = [System.IO.File]::ReadAllText((Join-Path $projectRoot 'styles.css'))
    images = @{}
}
foreach ($name in @('embuilded-logo.png', 'traci-logo-on-dark.png')) {
    $bytes = [System.IO.File]::ReadAllBytes((Join-Path $projectRoot ('assets/' + $name)))
    $resources.images['assets/' + $name] = 'data:image/png;base64,' + [Convert]::ToBase64String($bytes)
}
$svgBytes = [System.IO.File]::ReadAllBytes((Join-Path $projectRoot 'assets/embuilded-logo.svg'))
$resources.images['assets/embuilded-logo.svg'] = 'data:image/svg+xml;base64,' + [Convert]::ToBase64String($svgBytes)
$json = ConvertTo-Json -InputObject $resources -Depth 4 -Compress
[System.IO.File]::WriteAllText((Join-Path $projectRoot 'assets/export-resources.js'), 'window.CARD_EXPORT_RESOURCES = ' + $json + ';', (New-Object System.Text.UTF8Encoding($false)))
