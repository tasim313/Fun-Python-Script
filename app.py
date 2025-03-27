from flask import Flask, render_template, request, send_file
import os
import pytesseract
import cv2
import pandas as pd
import docx
from pdf2image import convert_from_path
import tempfile
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Tesseract OCR path (for Ubuntu)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Function to extract text from an image (PNG, JPG, etc.)
def extract_text_from_image(image_path):
    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text
    except Exception as e:
        return f"Error processing image: {e}"

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        full_text = ""
        for image in images:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_img:
                img_path = temp_img.name
                image.save(img_path, 'PNG')
                full_text += extract_text_from_image(img_path)
                os.remove(img_path)
        return full_text
    except Exception as e:
        return f"Error processing PDF: {e}"

# Function to extract text from a DOCX file
def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        return f"Error processing DOCX: {e}"

# Function to extract text from an ODT file
def extract_text_from_odt(odt_path):
    try:
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode='w+t', encoding='utf-8') as temp_file:
            temp_txt_path = temp_file.name
            subprocess.run(['unoconv', '-f', 'txt', '-o', temp_txt_path, odt_path], check=True)
            with open(temp_txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
            os.remove(temp_txt_path)
            return text
    except Exception as e:
        return f"Error processing ODT: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Get the file extension and determine extraction method
    file_extension = os.path.splitext(filename)[1].lower()
    
    if file_extension in ['.png', '.jpg', '.jpeg']:
        extracted_text = extract_text_from_image(file_path)
    elif file_extension == '.pdf':
        extracted_text = extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        extracted_text = extract_text_from_docx(file_path)
    elif file_extension == '.odt':
        extracted_text = extract_text_from_odt(file_path)
    else:
        extracted_text = "Unsupported file type."
    
    # Clean up the uploaded file after processing
    os.remove(file_path)
    
    # Return extracted text
    return render_template('index.html', extracted_text=extracted_text)

@app.route('/download/<format>', methods=['POST'])
def download_file(format):
    # Retrieve extracted text from the form (via POST)
    text = request.form.get('extracted_text', '')
    if not text.strip():
        return "No text to save", 400
    
    # Create the file based on the chosen format
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{format}') as temp_file:
        file_path = temp_file.name
        if format == 'csv':
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
        elif format in ['xlsx', 'ods']:
            # Process text into a DataFrame and save as Excel/ODS
            df = pd.DataFrame([line.strip() for line in text.split('\n')])
            df.to_excel(file_path, index=False, engine='odf' if format == 'ods' else 'openpyxl')
        return send_file(file_path, as_attachment=True, download_name=f'extracted_text.{format}')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)