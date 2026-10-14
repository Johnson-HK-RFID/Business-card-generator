$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$source = Join-Path $PSScriptRoot 'svg\TRACI_HNAG1000_Gas_Sensor_Case_Master_A4.svg'
$casePng = Join-Path $PSScriptRoot 'assets\gas-detector-case-original.png'
$output = Join-Path $PSScriptRoot 'svg\TRACI_HNAG1000_Gas_Sensor_Case_Contact_A4.svg'

$svg = Get-Content -LiteralPath $source -Raw
$caseBase64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($casePng))

$overlay = @"
<!-- Non-destructive brochure update. The original master remains below this group. -->
<g id="case-and-contact-update-v1">
  <!-- Product presentation area: field unit plus transport-case configuration. -->
  <rect x="39.75" y="167" width="714.25" height="265" fill="white"/>
  <line x1="397" y1="184" x2="397" y2="416" stroke="#D5DCE0" stroke-width="1"/>
  <use href="#image0_194_889" xlink:href="#image0_194_889" transform="translate(43 205) scale(0.36)"/>
  <!-- Reapply the source master's cleanup masks after scaling the original image. -->
  <rect x="176.5" y="209" width="89" height="47" fill="white"/>
  <rect x="44" y="273" width="24" height="89" fill="white"/>
  <rect x="374" y="248" width="26" height="120" fill="white"/>
  <image id="protective-case-photo" x="409" y="187" width="334" height="232" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,$caseBase64"/>

  <!-- Testing option sits with the technical information, not the contact block. -->
  <text x="513" y="561" fill="#B77D00" font-family="Arial, Helvetica, sans-serif" font-size="7.2" font-weight="700" letter-spacing="0.35">CNAS TEST REPORT OPTION / ON REQUEST</text>

  <!-- Replace only the central contact panel; retain the master Embuilded logo and QR. -->
  <rect x="360" y="973" width="231" height="133" fill="#F1F4F6"/>
  <line x1="360" y1="987" x2="360" y2="1085" stroke="#CAD3D8" stroke-width="1"/>
  <text x="376" y="995" fill="#F5A91B" font-family="Arial, Helvetica, sans-serif" font-size="8.5" font-weight="700" letter-spacing="1.2">CONTACT</text>
  <text x="376" y="1018" fill="#1C2632" font-family="Arial, Helvetica, sans-serif" font-size="11.5" font-weight="700">Freddie Leung</text>
  <text x="376" y="1032" fill="#52636D" font-family="Arial, Helvetica, sans-serif" font-size="7.8" font-weight="700">BD Manager</text>
  <text x="376" y="1054" fill="#324955" font-family="Arial, Helvetica, sans-serif" font-size="7.9">freddie.leung@embuilded.com</text>
  <text x="376" y="1076" fill="#324955" font-family="Arial, Helvetica, sans-serif" font-size="8.6">+852 9385 5543</text>
</g>
"@

$svg = $svg -replace '</svg>\s*$', "$overlay`r`n</svg>`r`n"
[IO.File]::WriteAllText($output, $svg, [Text.UTF8Encoding]::new($false))
Write-Output $output
