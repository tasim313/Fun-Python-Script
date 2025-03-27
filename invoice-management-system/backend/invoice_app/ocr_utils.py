# invoice_app/ocr_utils.py
import cv2
import pytesseract
from PIL import Image
import re

def preprocess_image(image_path):
    # Load image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Deskew and denoise
    image = cv2.GaussianBlur(image, (5, 5), 0)
    return image

def extract_invoice_data(image_path):
    # Preprocess image
    processed_image = preprocess_image(image_path)
    # Extract text using Tesseract
    text = pytesseract.image_to_string(processed_image)
    # Parse text to extract fields
    invoice_number = re.search(r'Invoice No[:\.\s]*(\d+)', text).group(1)
    date = re.search(r'Date[:\.\s]*(\d{2}/\d{2}/\d{4})', text).group(1)
    vendor = re.search(r'Vendor[:\.\s]*([A-Za-z\s]+)', text).group(1)
    total_amount = re.search(r'Total[:\.\s]*(\d+\.\d{2})', text).group(1)
    return {
        'invoice_number': invoice_number,
        'date': date,
        'vendor': vendor,
        'total_amount': total_amount,
    }