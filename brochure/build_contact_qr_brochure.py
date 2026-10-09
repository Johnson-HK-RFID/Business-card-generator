from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "brochure/svg/TRACI_HNAG1000_Data_Sheet_Master_2026-10.svg"
QR = ROOT / "brochure/assets/website-qr-code.svg"
BRAND = ROOT / "logo-svg/building-embuilded-horizontal-refined.svg"
OUT = ROOT / "brochure/svg/TRACI_HNAG1000_Data_Sheet_Contact_QR.svg"

def inline_svg(path, x, y, width, height, group_id):
    source = path.read_text(encoding="utf-8")
    match = re.search(r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*)</svg>', source, re.S)
    if not match:
        raise ValueError(f"Invalid SVG: {path}")
    min_x, min_y, sw, sh = map(float, match.group(1).split())
    scale = min(width / sw, height / sh)
    tx = x + (width - sw * scale) / 2 - min_x * scale
    ty = y + (height - sh * scale) / 2 - min_y * scale
    content = re.sub(r'<title>.*?</title>', '', match.group(2), flags=re.S)
    return f'<g id="{group_id}" transform="translate({tx:.3f} {ty:.3f}) scale({scale:.7f})">{content}</g>'

svg = BASE.read_text(encoding="utf-8")
svg = svg.replace('height="1754" viewBox="0 0 1240 1754"', 'height="1950" viewBox="0 0 1240 1950"', 1)

brand = inline_svg(BRAND, 62, 1780, 390, 110, "embuilded-company-logo")
qr = inline_svg(QR, 1010, 1770, 150, 153, "website-qr-code")

footer = f'''
<g id="company-contact-footer">
  <rect x="0" y="1754" width="1240" height="196" fill="#F1F4F6"/>
  <rect x="0" y="1754" width="1240" height="7" fill="#F5B218"/>
  {brand}
  <line x1="474" y1="1783" x2="474" y2="1918" stroke="#CBD4D9" stroke-width="2"/>
  <text x="510" y="1805" fill="#F5B218" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="700" letter-spacing="1.5">CONTACT</text>
  <text x="510" y="1840" fill="#0F2937" font-family="Arial, Helvetica, sans-serif" font-size="18">info@embuilded.com</text>
  <text x="510" y="1872" fill="#0F2937" font-family="Arial, Helvetica, sans-serif" font-size="18">+852 0000 0000 <tspan fill="#6B7C87" font-size="13">(placeholder)</tspan></text>
  <text x="510" y="1904" fill="#0F2937" font-family="Arial, Helvetica, sans-serif" font-size="18">www.embuilded.com</text>
  <rect x="998" y="1768" width="174" height="160" rx="5" fill="#FFFFFF"/>
  <text x="1085" y="1934" text-anchor="middle" fill="#0F2937" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="700">SCAN TO VISIT OUR WEBSITE</text>
  {qr}
</g>
'''
svg = svg.replace('</svg>', footer + '</svg>', 1)
OUT.write_text(svg, encoding="utf-8")
print(OUT)
