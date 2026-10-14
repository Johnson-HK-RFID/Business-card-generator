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
INK, AMBER, MUTED = '#1C2632', '#F5B218', '#52636D'
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
                    'Gas channel labels summarize specifications already present in the master.')
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
products = add('g', id='original-clean-detector-pair', transform='translate(-11 -37) scale(1.75)')
for n in overlay:
    if n.tag == f'{{{SVG}}}use' or (
        n.tag == f'{{{SVG}}}rect' and n.get('fill') == 'white' and n.get('x') != '39.75'
    ):
        products.append(deepcopy(n))
case = deepcopy(next(n for n in overlay if n.get('id') == 'protective-case-photo'))
case.attrib.update({'x': '808', 'y': '329', 'width': '355', 'height': '257'})
page.append(case)

# Four channel names add useful context rather than new product claims.
channels = add('g', id='gas-channel-overview')
rect(64, 644, 1112, 70, '#F7F4EA')
for idx, (symbol, label) in enumerate([
    ('EX', 'Combustible gas'), ('O2', 'Oxygen'), ('CO', 'Carbon monoxide'), ('H2S', 'Hydrogen sulphide'),
]):
    x = 84 + 278 * idx
    if idx:
        line(x - 20, 660, x - 20, 698, '#D7D9D4')
    text(x, 689, symbol, 27, 700)
    text(x + (57 if symbol != 'H2S' else 65), 687, label, 17, color=MUTED)

rect(64, 738, 1112, 107, '#F1F4F6', rx=5)
text(88, 769, '24-HOUR CONNECTED MONITORING', 22, 700, '#AD7500')
text(88, 801, '2.5-inch colour display, local audible and visual alarms, temperature and humidity sensing,', 19.5)
text(88, 828, 'remote data transmission and multiple wireless communication options.', 19.5)

text(64, 891, 'Technical data', 31, 700)
rect(64, 913, 1112, 42, INK)
text(84, 941, 'PARAMETER', 17, 700, 'white')
text(386, 941, 'SPECIFICATION', 17, 700, 'white')
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
y = 955
for idx, (label, values) in enumerate(rows):
    h = 50 if len(values) > 1 else 34
    rect(64, y, 1112, h, '#F7F4EA' if idx % 2 else 'white')
    text(84, y + (32 if len(values) > 1 else 24), label, 20, 700)
    for line_no, value in enumerate(values):
        text(386, y + 22 + line_no * 22, value, 21)
    y += h
line(364, 955, 364, y, '#E1E6E9', 1)
line(64, y, 1176, y, '#CFD8DE', 1)
text(64, 1381, 'CNAS TEST REPORT ENQUIRIES', 17, 700, MUTED)
text(1176, 1381, 'Contact us for details', 17, color=MUTED, text_anchor='end')

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
text(506, 1551, 'CONTACT', 17, 700, '#AD7500', letter_spacing='.5')
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
