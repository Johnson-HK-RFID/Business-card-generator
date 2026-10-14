"""Refine the user's Case_Contact master while retaining its light-footer identity."""
from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent
SOURCE = BASE / 'svg/TRACI_HNAG1000_Gas_Sensor_Case_Contact_A4.svg'
OUT = BASE / 'svg/TRACI_HNAG1000_Gas_Sensor_Case_Optimized_A4.svg'
SVG = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
ET.register_namespace('', SVG)
ET.register_namespace('xlink', XLINK)
source = ET.parse(SOURCE).getroot()
original = next(n for n in source if n.tag == f'{{{SVG}}}g')
parts = list(original)
overlay = next(n for n in source if n.get('id') == 'case-and-contact-update-v1')
INK = '#1C2632'
AMBER = '#F5B218'
MUTED = '#52636D'
page = ET.Element(f'{{{SVG}}}svg', {
    'width': '210mm', 'height': '297mm', 'viewBox': '0 0 794 1123', 'fill': 'none',
})


def add(tag, parent=None, **attrs):
    return ET.SubElement(page if parent is None else parent, f'{{{SVG}}}{tag}', {
        k.replace('_', '-'): str(v) for k, v in attrs.items()
    })


def text(x, y, value, size=13, weight=400, color=INK, **attrs):
    node = add('text', x=x, y=y, fill=color, font_family='Arial, Helvetica, sans-serif',
               font_size=size, font_weight=weight, **attrs)
    node.text = value
    return node


def rect(x, y, w, h, fill, **attrs):
    return add('rect', x=x, y=y, width=w, height=h, fill=fill, **attrs)


def line(x1, y1, x2, y2, color='#D9E0E4', width=1):
    return add('line', x1=x1, y1=y1, x2=x2, y2=y2, stroke=color, stroke_width=width)


add('title').text = 'TRACI HNAG1000-4-STX / Gas Sensor / Light A4'
add('desc').text = ('Optimized from the supplied Case Contact brochure. Original logo outlines, '
                    'cleaned detector picture, existing case picture and QR artwork are preserved. '
                    'Body text is editable; physical page size is A4.')
defs = add('defs')
original_image = next(n for n in source.iter() if n.get('id') == 'image0_194_889')
defs.append(deepcopy(original_image))
rect(0, 0, 794, 1123, 'white')
rect(0, 0, 794, 9, AMBER)

# Retain the master's exact logo size, layout and dark colourway.
brand_header = add('g', id='traci-original-logo')
for n in parts[2:10]:
    brand_header.append(deepcopy(n))
text(754, 39, 'PRODUCT DATA SHEET', 10, 700, MUTED, text_anchor='end')
text(754, 59, 'HNAG1000-4-STX', 14.5, 700, text_anchor='end')
line(40, 117, 754, 117, '#9CAAB4')
text(40, 149, 'Portable Online Four Gas Detector', 26, 700)
text(40, 171, 'Continuous monitoring of EX, O2, CO and H2S', 13.5, color=MUTED)

# Copy the exact image reference and existing masks as one transformable group.
products = add('g', id='original-clean-detector-pair', transform='translate(-5 9) scale(1.07)')
for n in overlay:
    if n.tag == f'{{{SVG}}}use' or (
        n.tag == f'{{{SVG}}}rect' and n.get('fill') == 'white' and n.get('x') != '39.75'
    ):
        products.append(deepcopy(n))
case_source = next(n for n in overlay if n.get('id') == 'protective-case-photo')
case = deepcopy(case_source)
case.attrib.update({'x': '474', 'y': '218', 'width': '260', 'height': '189'})
page.append(case)

# Existing feature summary in a restrained, light panel.
rect(40, 422, 714, 86, '#F1F4F6', rx=4)
text(57, 445, '24-HOUR CONNECTED MONITORING', 14.5, 700, '#AD7500')
text(57, 465, '2.5-inch colour display, local audible and visual alarms, temperature and humidity sensing,', 13)
text(57, 484, 'remote data transmission and multiple wireless communication options.', 13)
text(57, 502, 'EX  |  O2  |  CO  |  H2S', 13, 700)

text(40, 535, 'Technical data', 21, 700)
text(754, 533, 'CNAS TEST REPORT / ENQUIRIES', 10, 700, MUTED, text_anchor='end')
rect(40, 551, 714, 29, INK)
text(52, 570, 'PARAMETER', 11.5, 700, 'white')
text(235, 570, 'SPECIFICATION', 11.5, 700, 'white')
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
y = 580
for index, (label, values) in enumerate(rows):
    height = 43 if len(values) > 1 else 29
    rect(40, y, 714, height, '#F7F4EA' if index % 2 else 'white')
    text(52, y + (26 if len(values) > 1 else 19), label, 13, 700)
    for number, value in enumerate(values):
        text(235, y + 19 + number * 17, value, 13.5)
    y += height
line(220, 580, 220, y, '#E1E6E9', .8)
line(40, y, 754, y, '#CFD8DE', .8)

# Keep a small dark applications strip, as in the original gas sensor design.
rect(0, 927, 794, 49, INK)
text(40, 945, 'APPLICATIONS', 10.5, 700, AMBER, letter_spacing='.5')
text(40, 964, 'Oil & gas · Chemical processing · Steel · Power · Wastewater · Tunnels · Hazardous-area safety', 11, color='white')
rect(0, 976, 794, 2, AMBER)
rect(0, 978, 794, 145, '#F1F4F6')

# Original Embuilded outlines and colours, uniformly resized, with no overlay masks.
company = add('svg', id='embuilded-original-logo', x=40, y=1010, width=253, height=67,
              viewBox='76 1004 287 76', preserveAspectRatio='xMinYMid meet')
for n in parts[67:121]:
    company.append(deepcopy(n))
line(312, 1002, 312, 1101, '#CED7DD')
text(330, 1005, 'CONTACT', 10.5, 700, '#AD7500', letter_spacing='.5')
text(330, 1029, 'Freddie Leung', 16, 700)
text(330, 1046, 'BD Manager', 11, color=MUTED)
text(330, 1071, 'freddie.leung@embuilded.com', 12.5, color='#324955')
text(330, 1094, '+852 9385 5543', 13, color='#324955')
rect(638, 997, 99, 99, 'white', rx=3)
qr = add('svg', id='original-product-qr', x=638, y=997, width=99, height=99,
         viewBox='599 995 91 91', preserveAspectRatio='xMidYMid meet')
qr.append(deepcopy(parts[128]))
text(687.5, 1110, 'VIEW PRODUCT DETAILS', 8.5, 700, text_anchor='middle')

ET.indent(page, space='  ')
ET.ElementTree(page).write(OUT, encoding='utf-8', xml_declaration=True)
print(OUT)
