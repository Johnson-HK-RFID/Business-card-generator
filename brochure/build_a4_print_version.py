from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "brochure/svg/TRACI_HNAG1000_Data_Sheet_Integrated_Footer.svg"
OUT = ROOT / "brochure/svg/TRACI_HNAG1000_Data_Sheet_A4_Print.svg"

source = SOURCE.read_text(encoding="utf-8")
match = re.search(r'<svg[^>]*>(.*)</svg>\s*$', source, re.S)
if not match:
    raise RuntimeError("Could not read source SVG contents")

content = match.group(1)
page_width = 1240
page_height = 1754
source_width = 1240
source_height = 1950
scale = page_height / source_height
offset_x = (page_width - source_width * scale) / 2

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="210mm" height="297mm" viewBox="0 0 {page_width} {page_height}">
  <title>HNAG1000-4-STX A4 Product Data Sheet</title>
  <desc>ISO 216 A4 portrait print version, 210 by 297 millimetres. Source artwork is uniformly scaled and centred without distortion.</desc>
  <rect width="{page_width}" height="{page_height}" fill="#FFFFFF"/>
  <g id="a4-centred-artwork" transform="translate({offset_x:.4f} 0) scale({scale:.8f})">
    {content}
  </g>
</svg>
'''

OUT.write_text(svg, encoding="utf-8")
print(OUT)
