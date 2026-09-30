from base64 import b64encode
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "brochure" / "svg"
OUT.mkdir(parents=True, exist_ok=True)

def uri(path, mime):
    return f"data:{mime};base64,{b64encode(Path(path).read_bytes()).decode()}"

def inline_logo(path, x, y, width, height):
    source = Path(path).read_text(encoding="utf-8")
    match = re.search(r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*)</svg>', source, re.S)
    if not match:
        raise ValueError(path)
    _, _, sw, sh = map(float, match.group(1).split())
    scale = min(width / sw, height / sh)
    tx = x + (width - sw * scale) / 2
    ty = y + (height - sh * scale) / 2
    content = re.sub(r'<title>.*?</title>', '', match.group(2), flags=re.S)
    return f'<g id="replaceable-traci-logo" transform="translate({tx:.3f} {ty:.3f}) scale({scale:.6f})">{content}</g>'

PRODUCT = uri(ROOT / "brochure/assets/gas-detector-configurations.jpg", "image/jpeg")
VARIANTS = {
    "TRACI_HNAG1000_Data_Sheet_Portrait_Wordmark.svg": (ROOT / "logo-svg/traci-digital-wordmark.svg", "TRACI wordmark"),
    "TRACI_HNAG1000_Data_Sheet_Portrait_Circuit_Logo.svg": (ROOT / "logo-svg/traci-circuit-lockup.svg", "TRACI circuit logo"),
}

specs = [
    ("Target gases", "EX / O2 / CO / H2S"),
    ("Ranges", "EX 0–100 %LEL; O2 0–30 %vol; CO 0–500 ppm; H2S 0–100 ppm"),
    ("Resolution", "EX 0.1 %LEL; O2 0.1 %vol; CO 1 ppm; H2S 0.1 ppm"),
    ("Accuracy / response", "±2 % F.S. / T90 < 10 s"),
    ("Environment", "−30 to 50 °C; 0–95 %RH; 86–106 kPa"),
    ("Supply", "12–30 V DC; ≤50 mA"),
    ("Protection", "IP66 / Ex d IIC T6"),
    ("Wireless", "GPRS, 4G, Wi-Fi, LoRa and ZigBee"),
    ("Runtime", ">16 h single gas; >12 h four gas without pump"),
    ("Dimensions", "460 H × 340 W × 115 D mm"),
    ("Warranty", "1 year; expected service life 3–5 years"),
]

def build(logo_path, label):
    logo = inline_logo(logo_path, 62, 42, 510, 150)
    rows=[]
    for i,(name,value) in enumerate(specs):
        y=1048+i*48
        fill="#FFFFFF" if i%2==0 else "#F8F6EC"
        rows.append(f'<rect x="62" y="{y}" width="1116" height="48" fill="{fill}"/>')
        rows.append(f'<text x="78" y="{y+31}" class="body" font-size="16" font-weight="700">{escape(name)}</text>')
        rows.append(f'<text x="330" y="{y+31}" class="body" font-size="15">{escape(value)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1240" height="1754" viewBox="0 0 1240 1754" role="img" aria-label="Portrait HNAG1000 data sheet with {escape(label)}">
<title>HNAG1000-4-STX Portrait Product Data Sheet — {escape(label)}</title>
<desc>A4 portrait editable vector data sheet. Logo is embedded as native vector paths.</desc>
<style>.body{{font-family:Arial,Helvetica,sans-serif;fill:#0F2937}}.heading{{font-family:Arial,Helvetica,sans-serif;fill:#0F2937;font-weight:700}}.amber{{fill:#F5B218}}</style>
<rect width="1240" height="1754" fill="#FFFFFF"/><rect width="1240" height="18" fill="#F5B218"/>
{logo}
<text x="1178" y="70" text-anchor="end" class="body" font-size="17" font-weight="700">PRODUCT DATA SHEET</text>
<text x="1178" y="99" text-anchor="end" class="body" font-size="22" font-weight="700">HNAG1000-4-STX</text>
<line x1="62" y1="210" x2="1178" y2="210" stroke="#0F2937" stroke-width="2"/>
<text x="62" y="272" class="heading" font-size="43">Portable Online Four Gas Detector</text>
<text x="64" y="309" class="body" font-size="19">Continuous monitoring of EX, O2, CO and H2S</text>

<g id="product-image-with-label-masks">
  <defs><clipPath id="clean-product-clips"><path d="M175 345H520V825H175Z M720 345H1085V825H720Z"/></clipPath></defs>
  <!-- Two clean crop windows retain both devices while excluding the Chinese annotations. -->
  <image x="95" y="345" width="1050" height="480" preserveAspectRatio="xMidYMid meet" clip-path="url(#clean-product-clips)" href="{PRODUCT}" xlink:href="{PRODUCT}"/>
</g>

<rect x="62" y="846" width="1116" height="154" rx="7" fill="#EEF2F4"/>
<text x="94" y="892" class="heading amber" font-size="20">24-HOUR CONNECTED MONITORING</text>
<text x="94" y="928" class="body" font-size="17"><tspan x="94">2.5-inch colour display, local audible and visual alarms, temperature and humidity sensing,</tspan><tspan x="94" dy="26">remote data transmission and multiple wireless communication options.</tspan></text>
<text x="94" y="986" class="heading" font-size="24">EX  |  O2  |  CO  |  H2S</text>

<text x="62" y="1032" class="heading" font-size="27">Technical data</text>
<rect x="62" y="1048" width="1116" height="48" fill="#0F2937"/>
<text x="78" y="1079" fill="#FFFFFF" font-family="Arial" font-size="15" font-weight="700">PARAMETER</text>
<text x="330" y="1079" fill="#FFFFFF" font-family="Arial" font-size="15" font-weight="700">SPECIFICATION</text>
<g transform="translate(0 48)">{''.join(rows)}</g>
<line x1="312" y1="1096" x2="312" y2="1624" stroke="#D9D9D9"/>

<rect x="62" y="1643" width="1116" height="66" fill="#0F2937"/>
<text x="88" y="1670" fill="#F5B218" font-family="Arial" font-size="15" font-weight="700">APPLICATIONS</text>
<text x="88" y="1694" fill="#FFFFFF" font-family="Arial" font-size="14">Oil &amp; gas • Chemical processing • Steel • Power • Wastewater • Tunnels • Hazardous-area safety</text>
</svg>'''

for filename,(logo,label) in VARIANTS.items():
    target=OUT/filename
    target.write_text(build(logo,label),encoding="utf-8")
    print(target)
