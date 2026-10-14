"""Native 1240 x 1754 pixel refinement of the gas sensor Case Contact brochure."""
from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent
SOURCE = BASE / 'svg/TRACI_HNAG1000_Gas_Sensor_Case_Contact_A4.svg'
OUT = BASE / 'svg/TRACI_HNAG1000_Gas_Sensor_Case_Optimized_1240x1754.svg'
SVG = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
ET.register_namespace('', SVG)
ET.register_namespace('xlink', XLINK)
source = ET.parse(SOURCE).getroot()
parts = list(next(n for n in source if n.tag == f'{{{SVG}}}g'))
overlay = next(n for n in source if n.get('id') == 'case-and-contact-update-v1')
INK, AMBER, MUTED = '#1C2632', '#EFB33B', '#52636D'
page = ET.Element(f'{{{SVG}}}svg', {
    'width': '1240', 'height': '1754', 'viewBox': '0 0 1240 1754', 'fill': 'none',
})


def add(tag, parent=None, **attrs):
    return ET.SubElement(page if parent is None else parent, f'{{{SVG}}}{tag}', {
        k.replace('_', '-'): str(v) for k, v in attrs.items()
    })


def text(x, y, value, size=20, weight=400, color=INK, **attrs):
    node = add('text', x=x, y=y, fill=color, font_family='Arial, Helvetica, sans-serif',
               font_size=size, font_weight=weight, **attrs)
    node.text = value
    return node


def rect(x, y, w, h, fill, **attrs):
    return add('rect', x=x, y=y, width=w, height=h, fill=fill, **attrs)


def line(x1, y1, x2, y2, color='#D9E0E4', width=1):
    return add('line', x1=x1, y1=y1, x2=x2, y2=y2, stroke=color, stroke_width=width)


add('title').text = 'TRACI HNAG1000-4-STX / Gas Detector / 1240 x 1754'
add('desc').text = ('Native 1240 x 1754 pixel brochure with editable text. '
                    'Preserves the selected master logo outlines, embedded product photos and QR modules. '
                    'One continuous specification table contains gas-by-gas measurements and general data. '
                    'CNAS reporting availability is a supplier service statement, not product certification.')
defs = add('defs')
defs.append(deepcopy(next(n for n in source.iter() if n.get('id') == 'image0_194_889')))
rect(0, 0, 1240, 1754, 'white')
rect(0, 0, 1240, 13, AMBER)

header = add('svg', id='traci-original-logo', x=64, y=44, width=630, height=109,
             viewBox='43 27 434 75', preserveAspectRatio='xMinYMid meet')
for n in parts[2:10]:
    header.append(deepcopy(n))
text(1176, 65, 'PRODUCT DATA SHEET', 15, 700, MUTED, text_anchor='end')
text(1176, 96, 'HNAG1000-4-STX', 22, 700, text_anchor='end')
line(64, 181, 1176, 181, '#A5B1B9', 1.4)
text(64, 228, 'Portable Online Four Gas Detector', 39, 700)
text(64, 263, 'Continuous monitoring of EX, O2, CO and H2S', 20, color=MUTED)

# Preserve the cleaned master image plus all three original masking rectangles.
products = add('g', id='original-clean-detector-pair', transform='translate(-22 -104) scale(2)')
for n in overlay:
    if n.tag == f'{{{SVG}}}use' or (
        n.tag == f'{{{SVG}}}rect' and n.get('fill') == 'white' and n.get('x') != '39.75'
    ):
        products.append(deepcopy(n))
case = deepcopy(next(n for n in overlay if n.get('id') == 'protective-case-photo'))
case.attrib.update({'x': '790', 'y': '337', 'width': '382', 'height': '277'})
page.append(case)

# A prose summary avoids a third table and gives the dark data header more emphasis.
rect(64, 678, 1112, 115, '#F1F4F6', rx=4)
rect(64, 678, 3, 115, AMBER)
text(88, 709, '24-HOUR CONNECTED MONITORING', 22, 700, AMBER)
text(88, 743, '2.5-inch colour display, local audible and visual alarms, temperature and humidity sensing,', 19.5)
text(88, 773, 'remote data transmission and multiple wireless communication options.', 19.5)

text(64, 834, 'Technical data', 31, 700)
# One header covers the complete table. The first three rows share four gas columns.
rect(64, 855, 1112, 40, INK)
text(84, 881, 'PARAMETER', 17, 700, 'white')
text(334, 881, 'SPECIFICATION', 17, 700, 'white')
centres = [421.75, 637.25, 852.75, 1068.25]
for idx, (label, values) in enumerate([
    ('Target gases', ['EX', 'O2', 'CO', 'H2S']),
    ('Measuring range', ['0–100 %LEL', '0–30 %vol', '0–500 ppm', '0–100 ppm']),
    ('Resolution', ['0.1 %LEL', '0.1 %vol', '1 ppm', '0.1 ppm']),
]):
    y = 895 + idx * 42
    rect(64, y, 1112, 42, 'white' if idx % 2 == 0 else '#F7F4EA')
    text(84, y + 28, label, 20, 700)
    for x, value in zip(centres, values):
        text(x, y + 28, value, 21, 700 if idx == 0 else 400, text_anchor='middle')
for x in [529.5, 745, 960.5]:
    line(x, 895, x, 1021, '#E1E6E9')

rows = [
    ('Accuracy / response', '±2 % F.S. / T90 < 10 s'),
    ('Environment', '−30 to 50 °C; 0–95 %RH; 86–106 kPa'),
    ('Supply', '12–30 V DC; ≤50 mA'),
    ('Protection', 'IP66 / Ex d IIC T6'),
    ('Wireless', 'GPRS · 4G · Wi-Fi · LoRa · ZigBee'),
    ('Runtime', 'Single gas: >16 h; four gas without pump: >12 h'),
    ('Dimensions', '460 H × 340 W × 115 D mm'),
    ('Warranty', '1 year; expected service life 3–5 years'),
]
for idx, (label, value) in enumerate(rows):
    y = 1021 + idx * 42
    rect(64, y, 1112, 42, '#F7F4EA' if idx % 2 == 0 else 'white')
    text(84, y + 28, label, 20, 700)
    text(334, y + 28, value, 21)
line(314, 895, 314, 1357, '#E1E6E9')
# Subtle division between the gas-specific measurements and general specifications.
line(64, 1021, 1176, 1021, '#D7DFE4', 1.2)
line(64, 1357, 1176, 1357, '#CFD8DE')
# Service availability supplied by the user; do not depict it as product accreditation.
text(64, 1388, 'CNAS-accredited laboratory test reports available on request.', 18, color=MUTED)

rect(0, 1420, 1240, 88, INK)
text(64, 1451, 'APPLICATIONS', 17, 700, AMBER, letter_spacing='.6')
text(64, 1483, 'Oil & gas · Chemical processing · Steel · Power · Wastewater · Tunnels · Hazardous-area safety', 17.5, color='white')
rect(0, 1508, 1240, 3, AMBER)
rect(0, 1511, 1240, 243, '#F1F4F6')

brand = add('svg', id='embuilded-original-logo', x=64, y=1581, width=380, height=101,
            viewBox='76 1004 287 76', preserveAspectRatio='xMinYMid meet')
for n in parts[67:121]:
    brand.append(deepcopy(n))
line(474, 1546, 474, 1703, '#CED7DD', 1.5)
text(506, 1551, 'CONTACT', 17, 700, AMBER, letter_spacing='.5')
text(506, 1587, 'Freddie Leung', 26, 700)
text(506, 1613, 'BD Manager', 17, color=MUTED)
text(506, 1655, 'freddie.leung@embuilded.com', 21, color='#324955')
text(506, 1692, '+852 9385 5543', 21, color='#324955')
rect(1014, 1541, 153, 153, 'white', rx=4)
qr = add('svg', id='original-product-qr', x=1014, y=1541, width=153, height=153,
         viewBox='599 995 91 91', preserveAspectRatio='xMidYMid meet')
qr.append(deepcopy(parts[128]))
text(1090.5, 1721, 'VIEW PRODUCT DETAILS', 13, 700, text_anchor='middle')

ET.indent(page, space='  ')
ET.ElementTree(page).write(OUT, encoding='utf-8', xml_declaration=True)
print(OUT)
