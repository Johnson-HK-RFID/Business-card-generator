$projectRoot = Split-Path -Parent $PSScriptRoot

function Read-VectorAsset {
    param([string]$RelativePath)
    $content = [System.IO.File]::ReadAllText((Join-Path $projectRoot $RelativePath))
    $match = [regex]::Match($content, '<svg[^>]*width="(?<width>[0-9.]+)"[^>]*height="(?<height>[0-9.]+)"[^>]*>(?<body>[\s\S]*?)</svg>')
    if (-not $match.Success) { throw "Unable to parse $RelativePath" }
    return @{
        width = [double]$match.Groups['width'].Value
        height = [double]$match.Groups['height'].Value
        body = $match.Groups['body'].Value.Trim()
    }
}

$resources = @{
    embuilded = Read-VectorAsset 'assets/embuilded-logo.svg'
    traci = Read-VectorAsset 'assets/traci-logo-on-dark.svg'
}
$json = ConvertTo-Json -InputObject $resources -Depth 5 -Compress
$output = 'window.CARD_VECTOR_RESOURCES = ' + $json + ';'
[System.IO.File]::WriteAllText(
    (Join-Path $projectRoot 'assets/vector-resources.js'),
    $output,
    (New-Object System.Text.UTF8Encoding($false))
)
