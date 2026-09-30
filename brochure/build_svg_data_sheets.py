from base64 import b64encode
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "brochure" / "svg"
OUT.mkdir(parents=True, exist_ok=True)

def uri(path, mime):
    return f"data:{mime};base64,{b64encode(Path(path).read_bytes()).decode()}"

def inline_logo(path, x=70, y=48, width=510, height=145):
    source = Path(path).read_text(encoding="utf-8")
    match = re.search(r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*)</svg>', source, re.S)
    if not match:
        raise ValueError(f"Invalid SVG logo: {path}")
    _, _, source_width, source_height = map(float, match.group(1).split())
    scale = min(width / source_width, height / source_height)
    offset_x = x + (width - source_width * scale) / 2
    offset_y = y + (height - source_height * scale) / 2
    content = re.sub(r'<title>.*?</title>', '', match.group(2), flags=re.S)
    return f'<g id="replaceable-traci-logo" transform="translate({offset_x:.3f} {offset_y:.3f}) scale({scale:.6f})">{content}</g>'

product = uri(ROOT / "brochure/assets/gas-detector-configurations.jpg", "image/jpeg")
variants = {
    "TRACI_HNAG1000_Data_Sheet_Wordmark.svg": (ROOT / "logo-svg/traci-digital-wordmark.svg", "TRACI wordmark"),
    "TRACI_HNAG1000_Data_Sheet_Circuit_Logo.svg": (ROOT / "logo-svg/traci-circuit-lockup.svg", "TRACI circuit logo"),
}
specs = [
    ("Target gases", "EX / O2 / CO / H2S", "Measurement", "Electrochemical + catalytic combustion"),
    ("Ranges", "EX 0–100 %LEL; O2 0–30 %vol", "Additional ranges", "CO 0–500 ppm; H2S 0–100 ppm"),
    ("Resolution", "EX 0.1 %LEL; O2 0.1 %vol", "Additional resolution", "CO 1 ppm; H2S 0.1 ppm"),
    ("Accuracy", "±2 % F.S.", "Response time", "T90 &lt; 10 s"),
    ("Operating temperature", "−30 to 50 °C", "Humidity", "0–95 %RH"),
    ("Supply", "12–30 V DC; ≤50 mA", "Protection", "IP66 / Ex d IIC T6"),
    ("Wireless", "GPRS, 4G, Wi-Fi, LoRa, ZigBee", "Runtime", "&gt;16 h single gas; &gt;12 h four gas"),
    ("Dimensions", "460 H × 340 W × 115 D mm", "Warranty / life", "1 year / expected 3–5 years"),
]

def build(logo_path, label):
    logo = inline_logo(logo_path)
    rows=[]
    for i,row in enumerate(specs):
        y=669+i*45
        rows.append(f'<rect x="70" y="{y}" width="1460" height="45" fill="{"#fff" if i%2==0 else "#F8F6EC"}"/>')
        for x,val,bold in zip((82,267,800,985),row,(1,0,1,0)):
            rows.append(f'<text x="{x}" y="{y+29}" class="body" font-size="{16 if bold else 15}" font-weight="{700 if bold else 400}">{val}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1600" height="1100" viewBox="0 0 1600 1100" role="img" aria-label="HNAG1000 data sheet with {escape(label)}">
<title>HNAG1000-4-STX Portable Online Four Gas Detector — {escape(label)}</title>
<desc>Editable vector data sheet. The TRACI logo is embedded as native vector paths in the group replaceable-traci-logo.</desc>
<style>.body{{font-family:Arial,Helvetica,sans-serif;fill:#0F2937}}.heading{{font-family:Arial,Helvetica,sans-serif;fill:#0F2937;font-weight:700}}.amber{{fill:#F5B218}}</style>
<rect width="1600" height="1100" fill="#fff"/><rect width="1600" height="18" fill="#F5B218"/>
{logo}
<text x="1530" y="70" text-anchor="end" class="body" font-size="18" font-weight="700">PRODUCT DATA SHEET</text><text x="1530" y="98" text-anchor="end" class="body" font-size="21" font-weight="700">HNAG1000-4-STX</text>
<line x1="70" y1="210" x2="1530" y2="210" stroke="#0F2937" stroke-width="2"/>
<text x="70" y="266" class="heading" font-size="43">Portable Online Four Gas Detector</text><text x="72" y="301" class="body" font-size="20">Continuous monitoring of combustible gas, oxygen, carbon monoxide and hydrogen sulfide</text>
<image x="70" y="330" width="650" height="255" preserveAspectRatio="xMidYMid meet" href="{product}" xlink:href="{product}"/>
<rect x="760" y="330" width="770" height="255" rx="5" fill="#EEF2F4"/><text x="795" y="378" class="heading amber" font-size="20">24-HOUR CONNECTED MONITORING</text>
<text x="795" y="414" class="body" font-size="17"><tspan x="795">Continuous on-site measurement with a 2.5-inch colour display,</tspan><tspan x="795" dy="25">local audible and visual alarms, temperature and humidity sensing,</tspan><tspan x="795" dy="25">and remote data transmission.</tspan></text>
<text x="795" y="512" class="heading amber" font-size="18">TARGET GASES</text><text x="795" y="551" class="heading" font-size="27">EX | O2 | CO | H2S</text>
<text x="70" y="612" class="heading" font-size="25">Technical data</text><rect x="70" y="624" width="1460" height="45" fill="#0F2937"/>
<g fill="#fff" font-family="Arial" font-size="15" font-weight="700"><text x="82" y="653">PARAMETER</text><text x="267" y="653">SPECIFICATION</text><text x="800" y="653">PARAMETER</text><text x="985" y="653">SPECIFICATION</text></g>
{''.join(rows)}
<g stroke="#D9D9D9"><line x1="250" y1="669" x2="250" y2="1029"/><line x1="780" y1="669" x2="780" y2="1029"/><line x1="965" y1="669" x2="965" y2="1029"/></g>
<rect x="70" y="1042" width="1460" height="36" fill="#0F2937"/><text x="92" y="1066" fill="#fff" font-family="Arial" font-size="13">APPLICATIONS • Oil &amp; gas • Chemical processing • Steel • Power • Wastewater • Tunnels • Hazardous-area safety</text>
</svg>'''

for name,(logo,label) in variants.items():
    target=OUT/name
    target.write_text(build(logo,label),encoding="utf-8")
    print(target)
