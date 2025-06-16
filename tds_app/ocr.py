from PIL import Image
import pytesseract
import base64
from io import BytesIO

def extract_text(base64_data):
    try:
        image_data = base64.b64decode(base64_data)
        image = Image.open(BytesIO(image_data))
        return pytesseract.image_to_string(image)
    except Exception:
        return ""
