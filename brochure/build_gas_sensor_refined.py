"""Build an editable A4 gas detector brochure from the existing brand artwork.

Logo path geometry, QR modules and existing photo bytes are copied verbatim.
The current case photo asset is retained; its filename does not establish provenance.
"""
from base64 import b64encode
from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent
SVG = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
ET.register_namespace('', SVG)
ET.register_namespace('xlink', XLINK)
INK = '#1C2632'
AMBER = '#F5A91B'
MUTED = '#52636D'
master = ET.parse(BASE / 'svg/TRACI_HNAG1000_Gas_Sensor_Case_Master_A4.svg').getroot()
parts = list(master[0])
page = ET.Element(f'{{{SVG}}}svg', {
    'width': '210mm', 'height': '297mm', 'viewBox': '0 0 794 1123', 'fill': 'none',
})


def add(tag, parent=None, **attrs):
    node = ET.SubElement(page if parent is None else parent, f'{{{SVG}}}{tag}', {
        k.replace('_', '-'): str(v) for k, v in attrs.items()
    })
    return node


def text(x, y, value, size=12, weight=400, color=INK, parent=None, **attrs):
    node = add('text', parent=parent, x=x, y=y, fill=color,
               font_family='Arial, Helvetica, sans-serif', font_size=size,
               font_weight=weight, **attrs)
    node.text = value
    return node


def rect(x, y, w, h, color, **attrs):
    return add('rect', x=x, y=y, width=w, height=h, fill=color, **attrs)


def line(x1, y1, x2, y2, color='#D8DEE2', width=1):
    return add('line', x1=x1, y1=y1, x2=x2, y2=y2, stroke=color, stroke_width=width)


add('title').text = 'TRACI HNAG1000-4-STX / Four Gas Detector / A4'
add('desc').text = 'Editable A4 brochure. Brand outlines, QR modules and existing product photographs are preserved.'
rect(0, 0, 794, 1123, 'white')
rect(0, 0, 794, 8, AMBER)

# Copy the exact eight logo paths from the supplied master, including TM.
traci = add('svg', id='traci-original-logo', x=40, y=32, width=302, height=53,
            viewBox='43 27 434 75', preserveAspectRatio='xMinYMid meet')
for node in parts[2:10]:
    traci.append(deepcopy(node))
text(754, 45, 'PRODUCT DATA SHEET', 10, 700, MUTED, text_anchor='end', letter_spacing='.6')
text(754, 64, 'HNAG1000-4-STX', 15, 700, text_anchor='end')
line(40, 101, 754, 101, '#A7B2B9')
text(40, 132, 'Portable Online', 24, 700)
text(40, 167, 'Four Gas Detector', 34, 700)
text(40, 189, 'Continuous monitoring of EX, O2, CO and H2S', 13, color=MUTED)

# Embed the supplied cleaned product SVG, including its original white masks.
pair = ET.parse(BASE / 'assets/gas-detector-pair-clean.svg').getroot()
pair.set('id', 'original-clean-product-pair')
pair.set('x', '40')
pair.set('y', '226')
pair.set('width', '350')
pair.set('height', '184')
pair.set('preserveAspectRatio', 'xMidYMid meet')
page.append(pair)
case = (BASE / 'assets/gas-detector-case-original.png').read_bytes()
add('image', id='existing-case-photo', x=413, y=204, width=341, height=233,
    preserveAspectRatio='xMidYMid meet', href='data:image/png;base64,' + b64encode(case).decode())

rect(40, 447, 714, 82, '#F1F4F6')
rect(40, 447, 3, 82, AMBER)
text(56, 468, '24-HOUR CONNECTED MONITORING', 14, 700, '#A96F00')
text(56, 488, '2.5-inch colour display, local audible and visual alarms, temperature and humidity sensing,', 13)
text(56, 506, 'remote data transmission and multiple wireless communication options.', 13)
text(56, 523, 'EX  |  O2  |  CO  |  H2S', 13, 700)

text(40, 553, 'Technical data', 20, 700)
table = add('g', id='editable-technical-data')
rect(40, 566, 714, 28, INK)
text(52, 584, 'PARAMETER', 12, 700, 'white', parent=table)
text(230, 584, 'SPECIFICATION', 12, 700, 'white', parent=table)
rows = [
    ('Target gases', ['EX / O2 / CO / H2S']),
    ('Ranges', ['EX 0–100 %LEL; O2 0–30 %vol;', 'CO 0–500 ppm; H2S 0–100 ppm']),
    ('Resolution', ['EX 0.1 %LEL; O2 0.1 %vol; CO 1 ppm; H2S 0.1 ppm']),
    ('Accuracy / response', ['±2 % F.S. / T90 < 10 s']),
    ('Environment', ['−30 to 50 °C; 0–95 %RH; 86–106 kPa']),
    ('Supply', ['12–30 V DC; ≤50 mA']),
    ('Protection', ['IP66 / Ex d IIC T6']),
    ('Wireless', ['GPRS, 4G, Wi-Fi, LoRa and ZigBee']),
    ('Runtime', ['>16 h single gas; >12 h four gas without pump']),
    ('Dimensions', ['460 H × 340 W × 115 D mm']),
    ('Warranty', ['1 year; expected service life 3–5 years']),
]
y = 594
for idx, (label, values) in enumerate(rows):
    h = 41 if len(values) > 1 else 27
    rect(40, y, 714, h, '#F7F4EA' if idx % 2 else 'white')
    text(52, y + (25 if len(values) > 1 else 18), label, 13.5, 700, parent=table)
    for number, value in enumerate(values):
        text(230, y + 18 + number * 16, value, 14, parent=table)
    y += h
line(218, 594, 218, y, '#DFE4E7', .8)
line(40, y, 754, y, '#C6CFD5', .8)
# Keep the complete editable text group above the row backgrounds.
page.remove(table)
page.append(table)

# A plain enquiry label avoids an unverified claim of accredited testing availability.
text(40, 925, 'CNAS test report', 12, 700, MUTED)
text(163, 925, '/ Enquire for availability', 12, color=MUTED)

rect(0, 944, 794, 47, '#F7F4EA')
text(40, 961, 'APPLICATIONS', 10, 700, '#A96F00', letter_spacing='.6')
text(40, 979, 'Oil & gas · Chemical processing · Steel · Power · Wastewater · Tunnels · Hazardous-area safety', 12)

rect(0, 991, 794, 132, INK)
rect(0, 991, 794, 2, AMBER)
# Use the same path geometry with an explicit reversed colourway for the dark footer.
brand = add('svg', id='embuilded-original-logo', x=40, y=1023, width=244, height=65,
            viewBox='76 1004 287 76', preserveAspectRatio='xMinYMid meet')
for node in parts[67:121]:
    item = deepcopy(node)
    if item.get('fill') == INK:
        item.set('fill', '#FFFFFF')
    brand.append(item)
line(302, 1016, 302, 1099, '#6A737D', 1)
text(320, 1024, 'CONTACT', 10.5, 700, AMBER, letter_spacing='.5')
text(320, 1046, 'Freddie Leung', 17, 700, 'white')
text(320, 1062, 'BD Manager', 10.5, color='#C9D0D6')
text(320, 1084, 'freddie.leung@embuilded.com', 14, color='white')
text(320, 1103, '+852 9385 5543', 14, color='white')
rect(648, 1009, 88, 88, 'white')
qr = add('svg', id='original-product-qr', x=648, y=1009, width=88, height=88,
         viewBox='599 995 91 91', preserveAspectRatio='xMidYMid meet')
qr.append(deepcopy(parts[128]))
text(692, 1110, 'PRODUCT DETAILS', 8, 700, 'white', text_anchor='middle', letter_spacing='.3')

out = BASE / 'svg/TRACI_HNAG1000_Gas_Sensor_Refined_A4.svg'
ET.indent(page, space='  ')
ET.ElementTree(page).write(out, encoding='utf-8', xml_declaration=True)
print(out)
