from base64 import b64encode
from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BRAND_SOURCE = ROOT / "brochure/svg/TRACI_HNAG1000_Data_Sheet_A4_Print.svg"
PHOTO = HERE / "assets/recamera-pro-front.png"
OUT = HERE / "svg"

SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)


def el(tag, attrs=None, parent=None, value=None):
    item = ET.Element(f"{{{SVG}}}{tag}", attrs or {})
    if value is not None:
        item.text = value
    if parent is not None:
        parent.append(item)
    return item


def tx(parent, x, y, value, size=18, weight=400, fill="#0F2937", **extra):
    attrs = {
        "x": str(x), "y": str(y), "font-family": "Arial, Helvetica, sans-serif",
        "font-size": str(size), "font-weight": str(weight), "fill": fill,
    }
    attrs.update({k.replace("_", "-"): str(v) for k, v in extra.items()})
    return el("text", attrs, parent, value)


def line(parent, x1, y1, x2, y2, stroke="#78909C", width=3, dash=None):
    attrs = {"x1": str(x1), "y1": str(y1), "x2": str(x2), "y2": str(y2),
             "stroke": stroke, "stroke-width": str(width)}
    if dash:
        attrs["stroke-dasharray"] = dash
    return el("line", attrs, parent)


def rounded(parent, x, y, w, h, fill="white", stroke="#D5DEE3", sw=2, radius=14):
    return el("rect", {"x": str(x), "y": str(y), "width": str(w), "height": str(h),
                       "rx": str(radius), "fill": fill, "stroke": stroke,
                       "stroke-width": str(sw)}, parent)


def find_group(root, group_id):
    for item in root.iter():
        if item.attrib.get("id") == group_id:
            return item
    raise RuntimeError(f"Missing brand group: {group_id}")


brand_root = ET.parse(BRAND_SOURCE).getroot()
traci_logo = find_group(brand_root, "traci-original-logo")
embuilded_logo = find_group(brand_root, "embuilded-original-logo")
photo_uri = "data:image/png;base64," + b64encode(PHOTO.read_bytes()).decode("ascii")


def page(title, subtitle, page_number):
    root = el("svg", {"width": "210mm", "height": "297mm", "viewBox": "0 0 1240 1754"})
    el("title", parent=root, value=title)
    el("desc", parent=root, value="Hook Cam system concept sheet. Editable SVG text with preserved TRACI and Embuilded logo artwork.")
    el("rect", {"width": "1240", "height": "1754", "fill": "white"}, root)
    el("rect", {"width": "1240", "height": "14", "fill": "#F5B218"}, root)

    logo = deepcopy(traci_logo)
    logo.attrib["transform"] = "translate(35 -4) scale(.54)"
    root.append(logo)
    tx(root, 1170, 54, f"SYSTEM CONCEPT • {page_number}/2", 13, 700, text_anchor="end", letter_spacing="1")
    line(root, 62, 142, 1178, 142, "#6B7C87", 2)
    tx(root, 62, 205, title, 42, 700)
    tx(root, 64, 244, subtitle, 18, 400, "#46606D")
    return root


def icon_camera(g, x, y):
    rounded(g, x, y + 18, 105, 72, "#FFFFFF", "#0F2937", 4, 12)
    el("circle", {"cx": str(x + 53), "cy": str(y + 54), "r": "22", "fill": "none", "stroke": "#F5B218", "stroke-width": "8"}, g)
    el("path", {"d": f"M{x+22} {y+18} L{x+36} {y} H{x+70} L{x+84} {y+18}", "fill": "none", "stroke": "#0F2937", "stroke-width": "4"}, g)


def icon_router(g, x, y):
    rounded(g, x, y + 26, 112, 62, "#FFFFFF", "#0F2937", 4, 10)
    line(g, x + 22, y + 26, x + 10, y, "#0F2937", 4)
    line(g, x + 90, y + 26, x + 102, y, "#0F2937", 4)
    for n in range(3):
        el("circle", {"cx": str(x + 30 + 22*n), "cy": str(y + 58), "r": "5", "fill": "#F5B218"}, g)


def icon_battery(g, x, y):
    rounded(g, x, y + 8, 116, 76, "#FFFFFF", "#0F2937", 4, 8)
    el("rect", {"x": str(x + 116), "y": str(y + 31), "width": "12", "height": "30", "rx": "3", "fill": "#0F2937"}, g)
    el("path", {"d": f"M{x+58} {y+20} L{x+40} {y+52} H{x+59} L{x+48} {y+75} L{x+81} {y+39} H{x+62} Z", "fill": "#F5B218"}, g)


def icon_lidar(g, x, y):
    rounded(g, x, y + 10, 105, 76, "#0F2937", "#0F2937", 2, 8)
    el("circle", {"cx": str(x + 35), "cy": str(y + 48), "r": "16", "fill": "#F5B218"}, g)
    el("circle", {"cx": str(x + 72), "cy": str(y + 48), "r": "16", "fill": "#E5E7EB"}, g)
    line(g, x + 106, y + 48, x + 138, y + 48, "#0F2937", 4)


def icon_siren(g, x, y):
    el("path", {"d": f"M{x+25} {y+76} H{x+95} L{x+84} {y+28} Q{x+60} {y+4} {x+36} {y+28} Z", "fill": "#F5B218", "stroke": "#0F2937", "stroke-width": "4"}, g)
    line(g, x + 15, y + 78, x + 105, y + 78, "#0F2937", 6)
    line(g, x + 60, y - 5, x + 60, y - 25, "#F5B218", 6)


def footer(root):
    line(root, 62, 1688, 1178, 1688, "#D5DEE3", 2)
    brand = deepcopy(embuilded_logo)
    brand.attrib["transform"] = "translate(50 1694) scale(.45) translate(0 -1788)"
    root.append(brand)
    tx(root, 1178, 1728, "DRAFT — component selection and wiring subject to engineering validation", 12, 400, "#6B7C87", text_anchor="end")


# PAGE 1 — system architecture
p1 = page("Hook Cam", "Portable edge-AI monitoring, height sensing and field alert system", 1)
rounded(p1, 62, 285, 430, 500, "#F7F9FA", "#D5DEE3", 2, 16)
tx(p1, 90, 330, "CORE VISION DEVICE", 15, 700, "#F5A91B", letter_spacing="1")
tx(p1, 90, 370, "Seeed Studio reCamera Pro 4GB", 25, 700)
el("image", {"x": "92", "y": "400", "width": "370", "height": "300", "preserveAspectRatio": "xMidYMid meet", f"{{{XLINK}}}href": photo_uri}, p1)
tx(p1, 90, 742, "4K edge vision • 3 TOPS NPU • PoE / 12–24 V DC", 15, 700)

rounded(p1, 520, 285, 658, 500, "white", "#D5DEE3", 2, 16)
tx(p1, 550, 330, "SYSTEM CONNECTION CONCEPT", 15, 700, "#F5A91B", letter_spacing="1")

# Central camera and surrounding system nodes.
icon_camera(p1, 795, 455)
tx(p1, 848, 570, "reCamera Pro", 17, 700, text_anchor="middle")

icon_battery(p1, 565, 380)
tx(p1, 625, 492, "24 V LiFePO4", 16, 700, text_anchor="middle")
tx(p1, 625, 514, "500–600 Wh target", 13, 400, "#6B7C87", text_anchor="middle")

icon_router(p1, 1010, 380)
tx(p1, 1066, 492, "4G Router", 16, 700, text_anchor="middle")

icon_lidar(p1, 565, 610)
tx(p1, 625, 728, "TF02-Pro", 16, 700, text_anchor="middle")
tx(p1, 625, 750, "Height / range", 13, 400, "#6B7C87", text_anchor="middle")

icon_siren(p1, 1010, 620)
tx(p1, 1070, 728, "Siren", 16, 700, text_anchor="middle")

# Connection arrows and labels.
line(p1, 693, 430, 795, 490, "#F5B218", 5)
tx(p1, 718, 442, "DC/DC + PoE", 12, 700, "#8A6500", transform="rotate(29 718 442)")
line(p1, 1010, 447, 900, 495, "#0F2937", 4)
tx(p1, 943, 452, "Ethernet", 12, 700, transform="rotate(-24 943 452)")
line(p1, 703, 655, 795, 535, "#0F2937", 4)
tx(p1, 722, 626, "UART / I²C", 12, 700, transform="rotate(-52 722 626)")
line(p1, 1010, 655, 900, 535, "#F5B218", 5)
tx(p1, 951, 616, "GPIO / relay", 12, 700, "#8A6500", transform="rotate(48 951 616)")

tx(p1, 62, 845, "HOW THE SYSTEM WORKS", 18, 700, "#F5A91B", letter_spacing="1")
steps = [
    ("01", "Detect", "On-device AI analyses the camera stream without relying on continuous cloud inference."),
    ("02", "Measure", "TF02-Pro provides non-contact height or clearance data for contextual verification."),
    ("03", "Connect", "The 4G router provides remote telemetry, alerts and optional live-view access."),
    ("04", "Respond", "A configurable output drives the local siren while events are recorded and reported."),
]
for i, (num, name, body) in enumerate(steps):
    x = 62 + i * 284
    rounded(p1, x, 880, 260, 205, "#F7F9FA", "#D5DEE3", 2, 12)
    tx(p1, x + 20, 925, num, 34, 700, "#F5B218")
    tx(p1, x + 20, 966, name, 21, 700)
    words = body.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if len(trial) > 30:
            lines.append(current); current = word
        else:
            current = trial
    lines.append(current)
    for j, value in enumerate(lines[:4]):
        tx(p1, x + 20, 1000 + j * 23, value, 14, 400, "#46606D")

rounded(p1, 62, 1120, 1116, 510, "white", "#D5DEE3", 2, 16)
tx(p1, 92, 1165, "PRELIMINARY POWER ARCHITECTURE", 18, 700, "#F5A91B", letter_spacing="1")
tx(p1, 92, 1205, "Quick-swap battery", 18, 700)
tx(p1, 350, 1205, "Protection + conversion", 18, 700)
tx(p1, 660, 1205, "PoE / DC distribution", 18, 700)
tx(p1, 930, 1205, "Loads", 18, 700)
line(p1, 250, 1200, 330, 1200, "#F5B218", 5)
line(p1, 565, 1200, 640, 1200, "#F5B218", 5)
line(p1, 850, 1200, 915, 1200, "#F5B218", 5)
power_notes = [
    "• 8S LiFePO4 / 25.6 V nominal", "• 500–600 Wh target capacity", "• Field quick-swap enclosure",
    "• BMS + fuse + disconnect", "• 24 V to regulated DC rails", "• Surge / reverse-polarity protection",
    "• Camera power by PoE or 12–24 V", "• Separate protected auxiliary outputs", "• Cable and connector selection TBD",
    "• reCamera Pro", "• 4G router", "• TF02-Pro + siren",
]
columns = [(92, power_notes[0:3]), (350, power_notes[3:6]), (660, power_notes[6:9]), (930, power_notes[9:12])]
for x, values in columns:
    for j, value in enumerate(values):
        tx(p1, x, 1250 + j * 34, value, 14, 400, "#324955")

tx(p1, 92, 1398, "Indicative autonomy", 18, 700)
tx(p1, 92, 1435, "At 80% usable energy: approximately 20–24 h at 20 W average load, or 14–16 h at 30 W.", 16)
tx(p1, 92, 1466, "Final runtime requires confirmed router, siren duty cycle, converter efficiency and environmental derating.", 14, 400, "#6B7C87")
tx(p1, 92, 1522, "OPEN ITEMS", 15, 700, "#F5A91B", letter_spacing="1")
tx(p1, 92, 1554, "4G router model • siren voltage/power • PoE topology • enclosure/IP rating • mounting method • final battery pack", 15)
footer(p1)


# PAGE 2 — component specifications
p2 = page("Hook Cam — Component Specification", "Confirmed vendor data separated from target requirements and items awaiting selection", 2)

def spec_card(root, x, y, w, h, kicker, heading, rows, accent="#F5B218"):
    rounded(root, x, y, w, h, "white", "#D5DEE3", 2, 16)
    el("rect", {"x": str(x), "y": str(y), "width": "9", "height": str(h), "rx": "5", "fill": accent}, root)
    tx(root, x + 30, y + 40, kicker, 14, 700, accent, letter_spacing="1")
    tx(root, x + 30, y + 78, heading, 25, 700)
    row_y = y + 112
    for label, value in rows:
        line(root, x + 30, row_y, x + w - 30, row_y, "#E2E8EB", 1)
        tx(root, x + 30, row_y + 27, label, 14, 700, "#46606D")
        tx(root, x + 190, row_y + 27, value, 14, 400)
        row_y += 43


spec_card(p2, 62, 290, 548, 565, "CONFIRMED — SEEED STUDIO", "reCamera Pro 4GB", [
    ("Processor", "RV1126B; quad-core Cortex-A53 @ 1.2 GHz"),
    ("AI", "3 TOPS NPU; INT8 / INT16 mixed compute"),
    ("Memory", "4 GB LPDDR4"),
    ("Storage", "16 GB eMMC; microSD up to 512 GB"),
    ("Camera", "SC850SL; 4K @ 30 FPS"),
    ("Sensors", "6-axis ICM-42670-P IMU"),
    ("Audio", "Dual electret microphones; 8 Ω / 1 W speaker"),
    ("Networking", "Wi-Fi 5.2; Bluetooth 5.2; Gigabit Ethernet"),
    ("Interfaces", "USB-C OTG; debug UART; CAN ×2; GPIO ×2"),
    ("Power", "PoE; 12–24 V DC barrel; 7.4 V battery management"),
])

spec_card(p2, 630, 290, 548, 565, "CONFIRMED — BENEWAKE", "TF02-Pro LiDAR", [
    ("Technology", "Single-point ToF LiDAR; 850 nm VCSEL"),
    ("Range", "0.1–40 m @ 90% reflectivity"),
    ("Low reflectivity", "0.1–13.5 m @ 10% reflectivity"),
    ("Accuracy", "±5 cm to 5 m; ±1% from 5–40 m"),
    ("Resolution", "1 cm"),
    ("Frame rate", "1–1000 Hz adjustable; 100 Hz default"),
    ("Ambient light", "Up to 100 klux"),
    ("Protection", "IP65; Class 1 photobiological safety"),
    ("Interface", "UART, I²C and I/O; 3.3 V LVTTL"),
    ("Power", "5–12 V DC; ≤1 W average"),
])

spec_card(p2, 62, 885, 548, 410, "TARGET REQUIREMENT — NOT YET SELECTED", "Quick-swap Battery", [
    ("Chemistry", "LiFePO4"),
    ("Nominal voltage", "24 V class / 25.6 V nominal (8S target)"),
    ("Energy", "500–600 Wh target"),
    ("Indicative size", "20–24 Ah at 25.6 V"),
    ("Protection", "BMS, fuse, disconnect, over-current protection"),
    ("Mechanical", "Quick-swap, keyed connector, field enclosure"),
])

spec_card(p2, 630, 885, 548, 410, "SELECTION REQUIRED", "Router / PoE / Siren", [
    ("4G router", "Industrial LTE; Ethernet; VPN; watchdog preferred"),
    ("PoE", "Confirm injector/switch and camera PoE standard"),
    ("Siren", "Confirm voltage, SPL, current and duty cycle"),
    ("Relay/output", "Isolated driver matched to siren load"),
    ("Environmental", "Define IP rating and temperature range"),
    ("Compliance", "Confirm radio and site certification needs"),
])

rounded(p2, 62, 1325, 1116, 280, "#0F2937", "#0F2937", 0, 16)
tx(p2, 92, 1370, "INTEGRATION DECISIONS REQUIRED", 17, 700, "#F5B218", letter_spacing="1")
decisions = [
    "1. Confirm whether reCamera is powered directly from 12–24 V DC or through a dedicated PoE injector.",
    "2. Select the 4G router before finalising average power, Ethernet topology, VPN and remote-access behaviour.",
    "3. Confirm TF02-Pro mounting angle, measurement target and whether UART or I²C is used.",
    "4. Select siren voltage and SPL, then specify the isolated relay/driver and alarm duty cycle.",
    "5. Freeze enclosure, connector, battery swap and site environmental requirements before detailed engineering.",
]
for i, value in enumerate(decisions):
    tx(p2, 92, 1412 + i * 36, value, 15, 400, "white")

footer(p2)


for filename, root in [("Hook_Cam_System_Overview_A4.svg", p1), ("Hook_Cam_Component_Spec_A4.svg", p2)]:
    ET.indent(root, space="  ")
    (OUT / filename).write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode"), encoding="utf-8")
    print(OUT / filename)
