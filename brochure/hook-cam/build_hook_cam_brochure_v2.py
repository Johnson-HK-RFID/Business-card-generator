from base64 import b64encode
from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BRAND = ROOT / "brochure/svg/TRACI_HNAG1000_Data_Sheet_A4_Print.svg"
PHOTO = HERE / "assets/recamera-pro-front.png"
OUT = HERE / "svg"
SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)


def e(tag, attrs=None, parent=None, value=None):
    n = ET.Element(f"{{{SVG}}}{tag}", attrs or {})
    if value is not None:
        n.text = value
    if parent is not None:
        parent.append(n)
    return n


def t(p, x, y, value, size=16, weight=400, fill="#101D26", **kw):
    a = {"x": str(x), "y": str(y), "font-family": "Arial, Helvetica, sans-serif",
         "font-size": str(size), "font-weight": str(weight), "fill": fill}
    a.update({k.replace("_", "-"): str(v) for k, v in kw.items()})
    return e("text", a, p, value)


def rule(p, x1, y1, x2, y2, colour="#AAB6BC", width=1):
    return e("line", {"x1": str(x1), "y1": str(y1), "x2": str(x2), "y2": str(y2),
                      "stroke": colour, "stroke-width": str(width)}, p)


def group(root, gid):
    for n in root.iter():
        if n.attrib.get("id") == gid:
            return n
    raise RuntimeError(gid)


brand = ET.parse(BRAND).getroot()
traci = group(brand, "traci-original-logo")
embuilded = group(brand, "embuilded-original-logo")
photo = "data:image/png;base64," + b64encode(PHOTO.read_bytes()).decode("ascii")


def base(doc_title, folio):
    p = e("svg", {"width": "210mm", "height": "297mm", "viewBox": "0 0 1240 1754"})
    e("title", parent=p, value=doc_title)
    e("rect", {"width": "1240", "height": "1754", "fill": "#FFFFFF"}, p)
    e("rect", {"width": "1240", "height": "10", "fill": "#F5B218"}, p)
    lg = deepcopy(traci); lg.attrib["transform"] = "translate(42 -15) scale(.43)"; p.append(lg)
    t(p, 1178, 50, "HOOK CAM / SYSTEM PROPOSAL", 12, 700, letter_spacing="1.6", text_anchor="end")
    t(p, 1178, 75, folio, 12, 400, "#657781", text_anchor="end")
    rule(p, 62, 120, 1178, 120, "#101D26", 2)
    return p


def brand_footer(p):
    rule(p, 62, 1687, 1178, 1687, "#101D26", 2)
    lg = deepcopy(embuilded); lg.attrib["transform"] = "translate(48 1696) scale(.36) translate(0 -1788)"; p.append(lg)
    t(p, 1178, 1724, "PRELIMINARY DESIGN — NOT FOR CONSTRUCTION", 11, 700, "#657781", text_anchor="end", letter_spacing="1")


def tech_box(p, x, y, w, h, code, title, detail, accent=False):
    e("rect", {"x": str(x), "y": str(y), "width": str(w), "height": str(h),
               "fill": "#101D26" if accent else "#FFFFFF", "stroke": "#101D26", "stroke-width": "2"}, p)
    c = "#FFFFFF" if accent else "#101D26"
    t(p, x + 16, y + 23, code, 10, 700, "#F5B218", letter_spacing="1")
    t(p, x + 16, y + 52, title, 17, 700, c)
    t(p, x + 16, y + 76, detail, 11, 400, "#CFD8DC" if accent else "#657781")


# PAGE 1 — editorial overview
p1 = base("Hook Cam — Industrial System Overview", "01 / 02")
e("rect", {"x": "62", "y": "170", "width": "8", "height": "205", "fill": "#F5B218"}, p1)
t(p1, 94, 220, "HOOK CAM", 58, 700)
t(p1, 96, 264, "PORTABLE EDGE-AI SITE MONITORING", 16, 700, "#F5B218", letter_spacing="1.8")
t(p1, 96, 310, "A field-deployable vision and height-sensing system", 20, 400, "#344A56")
t(p1, 96, 340, "with local alarm output and 4G backhaul.", 20, 400, "#344A56")

# Unframed product photograph, dominant but restrained.
e("image", {"x": "680", "y": "145", "width": "465", "height": "450",
            "preserveAspectRatio": "xMidYMid meet", f"{{{XLINK}}}href": photo}, p1)
t(p1, 695, 575, "SEEED STUDIO reCamera Pro 4GB", 12, 700, "#657781", letter_spacing=".7")

# Key facts — plain typographic strip, no cards.
rule(p1, 62, 420, 640, 420, "#101D26", 2)
facts = [("4K / 30", "VISION"), ("3 TOPS", "EDGE AI"), ("0.1–40 m", "HEIGHT SENSOR"), ("500–600 Wh", "ENERGY TARGET")]
for i, (v, k) in enumerate(facts):
    x = 62 + i * 150
    t(p1, x, 468, v, 23, 700)
    t(p1, x, 493, k, 10, 700, "#657781", letter_spacing="1")

t(p1, 62, 650, "SYSTEM ARCHITECTURE", 15, 700, "#F5B218", letter_spacing="1.8")
rule(p1, 62, 670, 1178, 670, "#101D26", 2)

# Engineering single-line diagram.
tech_box(p1, 62, 725, 180, 96, "P01", "BATTERY", "25.6 V / 500–600 Wh")
tech_box(p1, 286, 725, 190, 96, "P02", "POWER", "BMS / DC-DC / PoE")
tech_box(p1, 520, 705, 235, 136, "C01", "reCamera Pro", "4K vision / edge inference", True)
tech_box(p1, 799, 725, 178, 96, "N01", "4G ROUTER", "Ethernet / VPN")
tech_box(p1, 1021, 725, 157, 96, "R01", "REMOTE", "alerts / live view")
for a, b in [(242, 286), (476, 520), (755, 799), (977, 1021)]:
    rule(p1, a, 773, b, 773, "#F5B218", 5)

tech_box(p1, 410, 910, 205, 96, "S01", "TF02-Pro", "UART / I²C • ≤1 W")
tech_box(p1, 660, 910, 205, 96, "A01", "SIREN", "isolated relay output")
rule(p1, 512, 910, 590, 841, "#101D26", 3)
rule(p1, 763, 910, 690, 841, "#101D26", 3)
t(p1, 62, 1045, "Signal flow", 12, 700, "#657781")
t(p1, 165, 1045, "sensor → local inference → event decision → alarm + remote report", 15, 400)

rule(p1, 62, 1090, 1178, 1090, "#101D26", 2)
t(p1, 62, 1130, "FIELD OPERATION", 15, 700, "#F5B218", letter_spacing="1.8")
operation = [
    ("01", "INSTALL", "Mount the camera and LiDAR to the hook or lifting assembly; align the measurement axis."),
    ("02", "MONITOR", "Run local vision inference and height measurement continuously without cloud dependency."),
    ("03", "ALERT", "Trigger the site siren and transmit an event record over the industrial 4G connection."),
]
for i, (n, h, body) in enumerate(operation):
    x = 62 + i * 378
    if i:
        rule(p1, x - 24, 1160, x - 24, 1375, "#D3DBDF", 1)
    t(p1, x, 1198, n, 36, 700, "#F5B218")
    t(p1, x, 1235, h, 18, 700)
    words, lines, current = body.split(), [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if len(trial) > 42: lines.append(current); current = word
        else: current = trial
    lines.append(current)
    for j, ln in enumerate(lines[:4]): t(p1, x, 1270 + j*25, ln, 14, 400, "#344A56")

e("rect", {"x": "62", "y": "1420", "width": "1116", "height": "190", "fill": "#F2F5F6"}, p1)
t(p1, 88, 1460, "DESIGN STATUS", 13, 700, "#F5B218", letter_spacing="1.4")
t(p1, 88, 1500, "Confirmed", 15, 700)
t(p1, 220, 1500, "reCamera Pro 4GB and Benewake TF02-Pro", 15)
t(p1, 88, 1535, "To select", 15, 700)
t(p1, 220, 1535, "4G router, siren, PoE equipment, battery pack and enclosure", 15)
t(p1, 88, 1570, "To validate", 15, 700)
t(p1, 220, 1570, "runtime, thermal performance, radio coverage, mounting and site compliance", 15)
brand_footer(p1)


# PAGE 2 — technical schedule
p2 = base("Hook Cam — Technical Schedule", "02 / 02")
t(p2, 62, 190, "TECHNICAL SCHEDULE", 38, 700)
t(p2, 64, 228, "Confirmed vendor data / preliminary system requirements", 17, 400, "#657781")
e("image", {"x": "940", "y": "142", "width": "215", "height": "170", "preserveAspectRatio": "xMidYMid meet", f"{{{XLINK}}}href": photo}, p2)

def section(p, y, code, title, status):
    t(p, 62, y, code, 12, 700, "#F5B218", letter_spacing="1")
    t(p, 130, y, title, 22, 700)
    t(p, 1178, y, status, 11, 700, "#657781", text_anchor="end", letter_spacing="1")
    rule(p, 62, y + 16, 1178, y + 16, "#101D26", 2)

def rows(p, y, data, left=62, mid=300, right=1178, height=36):
    for i, (a, b) in enumerate(data):
        yy = y + i*height
        if i % 2: e("rect", {"x": str(left), "y": str(yy-24), "width": str(right-left), "height": str(height), "fill": "#F5F6F2"}, p)
        t(p, left+12, yy, a, 14, 700, "#344A56")
        t(p, mid, yy, b, 14)
    return y + len(data)*height

section(p2, 340, "C01", "reCamera Pro 4GB", "CONFIRMED / SEEED STUDIO")
y = rows(p2, 392, [
    ("Compute", "RV1126B • quad-core Cortex-A53 1.2 GHz • 3 TOPS NPU • 4 GB LPDDR4"),
    ("Vision", "SC850SL • 4K at 30 FPS • six-axis ICM-42670-P IMU"),
    ("Storage", "16 GB eMMC • microSD up to 512 GB"),
    ("Network", "Gigabit Ethernet • Wi-Fi 5.2 • Bluetooth 5.2"),
    ("Interfaces", "USB-C OTG • debug UART • CAN ×2 • GPIO ×2"),
    ("Power", "PoE or 12–24 V DC barrel input; 7.4 V battery management supported"),
])

section(p2, y+28, "S01", "Benewake TF02-Pro", "CONFIRMED / BENEWAKE")
y = rows(p2, y+80, [
    ("Measurement", "0.1–40 m at 90% reflectivity; 0.1–13.5 m at 10% reflectivity"),
    ("Accuracy", "±5 cm from 0.1–5 m; ±1% from 5–40 m; 1 cm resolution"),
    ("Update rate", "1–1000 Hz adjustable; 100 Hz default"),
    ("Optical", "850 nm VCSEL • 3° FoV • Class 1 • 100 klux ambient-light immunity"),
    ("Electrical", "5–12 V DC • ≤1 W average • UART / I²C / I/O • 3.3 V LVTTL"),
    ("Mechanical", "69 × 41.5 × 26 mm • 50 g • IP65"),
])

section(p2, y+28, "P01", "Quick-swap LiFePO4 battery", "TARGET / PRODUCT NOT SELECTED")
y = rows(p2, y+80, [
    ("Nominal system", "24 V class / 25.6 V nominal, 8S LiFePO4 target"),
    ("Energy", "500–600 Wh target; approximately 20–24 Ah at 25.6 V"),
    ("Protection", "BMS • branch fuse • service disconnect • reverse-polarity protection"),
    ("Mechanical", "Field quick-swap enclosure and keyed high-current connector"),
])

section(p2, y+28, "OPEN", "Equipment selection and engineering checks", "ACTION REQUIRED")
y = rows(p2, y+80, [
    ("4G router", "Select LTE bands, Ethernet ports, VPN, watchdog, temperature and IP requirements"),
    ("Siren", "Confirm supply voltage, current, SPL, alarm pattern, duty cycle and relay rating"),
    ("PoE", "Confirm standard, injector/switch topology, conversion efficiency and surge protection"),
    ("Runtime", "Recalculate with measured average load, temperature derating and usable battery energy"),
    ("Installation", "Freeze mounting, enclosure, cabling, antenna, LiDAR alignment and maintenance access"),
])

e("rect", {"x": "62", "y": str(y+38), "width": "1116", "height": "105", "fill": "#101D26"}, p2)
t(p2, 88, y+76, "NEXT GATE", 12, 700, "#F5B218", letter_spacing="1.4")
t(p2, 88, y+112, "Select router, siren and battery pack before electrical schematic and enclosure design.", 17, 700, "white")
brand_footer(p2)

for name, doc in [("Hook_Cam_Industrial_Overview_A4.svg", p1), ("Hook_Cam_Technical_Schedule_A4.svg", p2)]:
    ET.indent(doc, space="  ")
    (OUT/name).write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(doc, encoding="unicode"), encoding="utf-8")
    print(OUT/name)
