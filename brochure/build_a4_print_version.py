from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "brochure/svg/TRACI_HNAG1000_Data_Sheet_Integrated_Footer.svg"
OUT = ROOT / "brochure/svg/TRACI_HNAG1000_Data_Sheet_A4_Print.svg"

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)

source_root = ET.parse(SOURCE).getroot()
source_outer = list(source_root)[0]
source_defs = list(source_root)[1]
source_main = list(source_outer)[1]

# The original product sheet is already a native 1240 x 1754 A4 composition.
# Keep it at 100% width and reflow only the technical-data rows to make room
# for the brand/contact footer. No logo, photo or text outline is distorted.
main = deepcopy(source_main)
main_children = list(main)

row_height = 38
original_row_height = 48
row_scale = row_height / original_row_height

# Technical-data body: 11 backgrounds and their two text columns.
for row in range(11):
    background_index = 20 + row * 3
    text_left_index = 21 + row * 3
    text_right_index = 22 + row * 3
    old_y = 1096 + row * original_row_height
    new_y = 1096 + row * row_height
    background = main_children[background_index]
    background.set(
        "transform",
        f"translate(0 {new_y}) scale(1 {row_scale:.8f}) translate(0 {-old_y})",
    )
    shift = new_y - old_y
    if shift:
        main_children[text_left_index].set("transform", f"translate(0 {shift})")
        main_children[text_right_index].set("transform", f"translate(0 {shift})")

# Shorten the table's vertical divider to the new table height.
main_children[53].set("d", "M312 1096V1514")

# Applications remains the final product-information band, immediately above
# the company footer.
applications_shift = -110
for index in (54, 55, 56):
    main_children[index].set("transform", f"translate(0 {applications_shift})")

svg = ET.Element(
    f"{{{SVG_NS}}}svg",
    {
        "width": "210mm",
        "height": "297mm",
        "viewBox": "0 0 1240 1754",
        "fill": "none",
    },
)
title = ET.SubElement(svg, f"{{{SVG_NS}}}title")
title.text = "HNAG1000-4-STX A4 Product Data Sheet"
desc = ET.SubElement(svg, f"{{{SVG_NS}}}desc")
desc.text = (
    "Native ISO 216 A4 portrait layout, 210 by 297 millimetres. Technical "
    "data is reflowed to use the full page width without stretching logos, "
    "photographs or text."
)
svg.append(deepcopy(source_defs))
svg.append(main)

# Replace the extended 1950-unit footer with a compact native-A4 footer.
ET.SubElement(
    svg,
    f"{{{SVG_NS}}}rect",
    {"x": "0", "y": "1602", "width": "1240", "height": "152", "fill": "#F1F4F6"},
)
ET.SubElement(
    svg,
    f"{{{SVG_NS}}}rect",
    {"x": "0", "y": "1599", "width": "1240", "height": "5", "fill": "#F5B218"},
)

footer_content = ET.SubElement(
    svg,
    f"{{{SVG_NS}}}g",
    {
        "id": "compact-brand-contact-footer",
        "transform": "translate(173.6 1615) scale(.72) translate(0 -1768)",
    },
)
for element in list(source_outer)[4:]:
    footer_content.append(deepcopy(element))

ET.indent(svg, space="  ")
OUT.write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    + ET.tostring(svg, encoding="unicode"),
    encoding="utf-8",
)
print(OUT)
