from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "brochure/svg/TRACI_HNAG1000_Data_Sheet_Integrated_Footer_Master.svg"
OUT = ROOT / "brochure/svg/TRACI_HNAG1000_Data_Sheet_Integrated_Footer.svg"

svg = MASTER.read_text(encoding="utf-8")

replacements = {
    # Turn the inset Applications box into a full-width transition band.
    '<path d="M1178 1643H62V1709H1178V1643Z" fill="#0F2937"/>':
    '<path d="M1240 1643H0V1712H1240V1643Z" fill="#0F2937"/>',
    # Pull the footer background upward so it directly follows Applications.
    '<path d="M1240 1754H0V1950H1240V1754Z" fill="#F1F4F6"/>':
    '<path d="M1240 1712H0V1950H1240V1712Z" fill="#F1F4F6"/>',
    # Replace the detached top rule with a slim brand-colour seam.
    '<path d="M1240 1754H0V1761H1240V1754Z" fill="#F5B218"/>':
    '<path d="M1240 1709H0V1714H1240V1709Z" fill="#F5B218"/>',
}

for old, new in replacements.items():
    if old not in svg:
        raise RuntimeError(f"Expected master element not found: {old}")
    svg = svg.replace(old, new, 1)

OUT.write_text(svg, encoding="utf-8")
print(OUT)
