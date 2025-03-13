import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import pytesseract
import cv2
import pandas as pd
import os
import docx
from pdf2image import convert_from_path
import subprocess
import tempfile
from tkinterdnd2 import TkinterDnD, DND_FILES

# Tesseract OCR path for Ubuntu
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Function to extract text from an image
def extract_text_from_image(image_path):
    """Extracts text from an image."""
    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text
    except Exception as e:
        messagebox.showerror("Error", f"Error processing image: {e}")
        return ""

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF."""
    try:
        images = convert_from_path(pdf_path)
        full_text = ""
        for image in images:
            img_path = "temp_image.png"  # Create a temporary image file
            image.save(img_path, 'PNG')
            full_text += extract_text_from_image(img_path)
            os.remove(img_path)  # Delete temporary image
        return full_text
    except Exception as e:
        messagebox.showerror("Error", f"Error processing PDF: {e}")
        return ""

# Function to extract text from a DOCX file
def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(docx_path)
        full_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return full_text
    except Exception as e:
        messagebox.showerror("Error", f"Error processing DOCX: {e}")
        return ""

# Function to extract text from an ODT file
def extract_text_from_odt(odt_path):
    """Extracts text from an ODT file using unoconv."""
    try:
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode='w+t', encoding='utf-8') as temp_file:
            temp_txt_path = temp_file.name
            subprocess.run(['unoconv', '-f', 'txt', '-o', temp_txt_path, odt_path], check=True)
            with open(temp_txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
            os.remove(temp_txt_path)
            return text
    except FileNotFoundError:
        messagebox.showerror("Error", "unoconv not found. Please install it.")
        return ""
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error processing ODT: {e}")
        return ""

# Function to process the selected file
def process_file(file_path=None):
    """Processes the selected file and extracts text."""
    if not file_path:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg"),
                                                          ("PDF files", "*.pdf"),
                                                          ("DOCX files", "*.docx"),
                                                          ("ODT files", "*.odt")])
    if file_path:
        file_extension = os.path.splitext(file_path)[1].lower()
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

        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, extracted_text)

# Function to handle file drop
def handle_file_drop(event):
    """Handles file drop events."""
    file_path = event.data.strip('{}')  # Remove curly braces from the file path
    process_file(file_path)

# Function to save extracted text to a CSV file
def save_to_csv():
    """Saves extracted text to a CSV file."""
    text = text_output.get(1.0, tk.END)
    if text.strip():
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                f.write(text)  # Simplest possible CSV write. Consider using CSV module for structured data.
            messagebox.showinfo("Success", "Text saved to CSV.")
    else:
        messagebox.showerror("Error", "No text to save.")

# Function to save extracted text to an Excel file
def save_to_excel():
    """Saves extracted text to an Excel file."""
    text = text_output.get(1.0, tk.END)
    if text.strip():
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df = pd.DataFrame([line.strip() for line in text.split('\n')])
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", "Text saved to Excel.")
    else:
        messagebox.showerror("Error", "No text to save.")

# Function to save extracted text to a LibreOffice Calc file
def save_to_calc():
    """Saves extracted text to a LibreOffice Calc file."""
    text = text_output.get(1.0, tk.END)
    if text.strip():
        file_path = filedialog.asksaveasfilename(defaultextension=".ods", filetypes=[("LibreOffice Calc files", "*.ods")])
        if file_path:
            df = pd.DataFrame([line.strip() for line in text.split('\n')])
            df.to_excel(file_path, index=False, engine='odf')
            messagebox.showinfo("Success", "Text saved to LibreOffice Calc.")
    else:
        messagebox.showerror("Error", "No text to save.")

# GUI setup
root = TkinterDnD.Tk()  # Use TkinterDnD's Tk instead of tk.Tk
root.title("OCR Text Extractor")

# Drag-and-drop area
drop_area = tk.Label(root, text="Drag and drop a file here", bg="lightgray", fg="black", width=80, height=10)
drop_area.pack(pady=10)
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', handle_file_drop)

# Upload file button
upload_button = ttk.Button(root, text="Upload File", command=process_file)
upload_button.pack(pady=10)

# Text output widget
text_output = tk.Text(root, height=20, width=80)
text_output.pack(pady=10)

# Save to CSV button
save_csv_button = ttk.Button(root, text="Save to CSV", command=save_to_csv)
save_csv_button.pack(pady=5)

# Save to Excel button
save_excel_button = ttk.Button(root, text="Save to Excel", command=save_to_excel)
save_excel_button.pack(pady=5)

# Save to LibreOffice Calc button
save_calc_button = ttk.Button(root, text="Save to LibreOffice Calc", command=save_to_calc)
save_calc_button.pack(pady=5)

# Run the application
root.mainloop()