from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "brochure/svg/TRACI_HNAG1000_Data_Sheet_Integrated_Footer.svg"
OUT = ROOT / "brochure/svg/TRACI_HNAG1000_Data_Sheet_A4_Print.svg"

SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)

source_root = ET.parse(SOURCE).getroot()
source_outer = list(source_root)[0]
source_defs = list(source_root)[1]
source_main = list(source_outer)[1]
main_parts = list(source_main)
outer_parts = list(source_outer)


def node(tag, attrs=None, parent=None, text=None):
    item = ET.Element(f"{{{SVG}}}{tag}", attrs or {})
    if text is not None:
        item.text = text
    if parent is not None:
        parent.append(item)
    return item


def text(parent, x, y, value, size, weight="400", fill="#0F2937", **extra):
    attrs = {
        "x": str(x), "y": str(y), "fill": fill,
        "font-family": "Arial, Helvetica, sans-serif",
        "font-size": str(size), "font-weight": str(weight),
    }
    attrs.update({k.replace("_", "-"): str(v) for k, v in extra.items()})
    return node("text", attrs, parent, value)


page = node("svg", {
    "width": "210mm", "height": "297mm", "viewBox": "0 0 1240 1754",
    "fill": "none",
})
node("title", parent=page, text="HNAG1000-4-STX A4 Product Data Sheet")
node("desc", parent=page, text=(
    "Native A4 product data sheet with editable typography. Original TRACI and "
    "Embuilded vector artwork is preserved without path changes."
))
page.append(deepcopy(source_defs))
node("rect", {"width": "1240", "height": "1754", "fill": "white"}, page)
node("rect", {"width": "1240", "height": "14", "fill": "#F5B218"}, page)

# Original TRACI vector paths, grouped and only uniformly resized.
traci = node("g", {"id": "traci-original-logo", "transform": "translate(30 -5) scale(.78)"}, page)
for part in main_parts[57:65]:
    traci.append(deepcopy(part))

text(page, 1010, 50, "PRODUCT DATA SHEET", 13, "700", text_anchor="middle", letter_spacing=".7")
text(page, 1010, 76, "HNAG1000-4-STX", 19, "700", text_anchor="middle")
node("line", {"x1": "62", "y1": "182", "x2": "1178", "y2": "182", "stroke": "#6B7C87", "stroke-width": "2"}, page)

text(page, 62, 232, "Portable Online Four Gas Detector", 37, "700")
text(page, 64, 265, "Continuous monitoring of EX, O2, CO and H2S", 16, "400", fill="#324955")

# Preserve the source product artwork and embedded photo data. Moving these
# elements does not alter the actual image or vector geometry.
products = node("g", {"id": "original-product-images", "transform": "translate(0 -120)"}, page)
for part in main_parts[7:11]:
    products.append(deepcopy(part))

# Clear, editable feature summary.
node("rect", {"x": "62", "y": "700", "width": "1116", "height": "132", "rx": "8", "fill": "#F1F4F6"}, page)
text(page, 90, 738, "24-HOUR CONNECTED MONITORING", 18, "700", fill="#F5A91B")
text(page, 90, 770, "2.5-inch colour display, local audible and visual alarms, temperature and humidity sensing,", 16)
text(page, 90, 795, "remote data transmission and multiple wireless communication options.", 16)
text(page, 90, 822, "EX | O2 | CO | H2S", 22, "700")

text(page, 62, 875, "Technical data", 25, "700")
table_x, table_y, table_w = 62, 895, 1116
label_w, header_h, row_h = 252, 42, 43
node("rect", {"x": str(table_x), "y": str(table_y), "width": str(table_w), "height": str(header_h), "fill": "#0F2937"}, page)
text(page, 78, 922, "PARAMETER", 14, "700", fill="white")
text(page, 332, 922, "SPECIFICATION", 14, "700", fill="white")

rows = [
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

for index, (label, value) in enumerate(rows):
    y = table_y + header_h + index * row_h
    fill = "#FFFFFF" if index % 2 == 0 else "#F7F4EA"
    node("rect", {"x": str(table_x), "y": str(y), "width": str(table_w), "height": str(row_h), "fill": fill}, page)
    baseline = y + 27
    text(page, 78, baseline, label, 16, "700")
    text(page, 332, baseline, value, 16, "400")

table_bottom = table_y + header_h + len(rows) * row_h
node("line", {"x1": "312", "y1": str(table_y + header_h), "x2": "312", "y2": str(table_bottom), "stroke": "#D8DEE2", "stroke-width": "1"}, page)

# Applications bridges product information and company details.
apps_y = 1428
node("rect", {"x": "0", "y": str(apps_y), "width": "1240", "height": "72", "fill": "#0F2937"}, page)
text(page, 88, apps_y + 29, "APPLICATIONS", 15, "700", fill="#F5B218")
text(page, 88, apps_y + 54, "Oil & gas  •  Chemical processing  •  Steel  •  Power  •  Wastewater  •  Tunnels  •  Hazardous-area safety", 13, fill="white")
node("rect", {"x": "0", "y": "1498", "width": "1240", "height": "5", "fill": "#F5B218"}, page)

# Footer background and exact Embuilded logo paths from the supplied master.
node("rect", {"x": "0", "y": "1503", "width": "1240", "height": "251", "fill": "#F1F4F6"}, page)
brand = node("g", {"id": "embuilded-original-logo", "transform": "translate(34 1535) scale(.92) translate(0 -1788)"}, page)
for part in outer_parts[13:67]:
    brand.append(deepcopy(part))

node("line", {"x1": "500", "y1": "1550", "x2": "500", "y2": "1718", "stroke": "#CBD4D9", "stroke-width": "2"}, page)
text(page, 536, 1582, "CONTACT", 17, "700", fill="#F5B218")
text(page, 536, 1620, "info@embuilded.com", 16)
text(page, 536, 1653, "+852 0000 0000", 16)
text(page, 536, 1686, "www.embuilded.com", 16)
text(page, 656, 1653, "(placeholder)", 11, fill="#6B7C87")

# Exact QR modules from the supplied source; only uniformly repositioned.
qr = node("g", {"id": "product-page-qr-original", "transform": "translate(48 1532) scale(.96) translate(0 -1768)"}, page)
for part in outer_parts[10:13]:
    qr.append(deepcopy(part))

ET.indent(page, space="  ")
OUT.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(page, encoding="unicode"), encoding="utf-8")
print(OUT)
