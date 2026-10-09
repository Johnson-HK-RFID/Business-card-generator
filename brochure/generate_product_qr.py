from pathlib import Path

import qrcode
import qrcode.image.svg

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "brochure/assets/product-page-qr-code.svg"
PRODUCT_URL = "https://www.embuilded.com/products/multi-gas-detector"

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4,
)
qr.add_data(PRODUCT_URL)
qr.make(fit=True)
image = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
image.save(OUT)
print(OUT)
