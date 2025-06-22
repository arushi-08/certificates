import io
import os

import fitz
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from pdf2image import convert_from_path

# Configuration
TEMPLATE_PATH = 'template.pdf'
FONT_PATH = 'PinyonScript-Regular.ttf'  # Use your font file
FONT_SIZE = 55
badge_name = "Test"
OUTPUT_DIR = f'public_html/certificates/{badge_name}'
CSV_PATH = 'recipients_processed.csv'

pdfmetrics.registerFont(TTFont('PinyonScript', FONT_PATH))


# Position where the name should appear (adjust as needed)
NAME_X = 300  # Horizontal position in points
NAME_Y = 400  # Vertical position in points


def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Directory created successfully: {directory_path}")
        except OSError as e:
            print(f"Error creating directory {directory_path}: {e}")


def find_name_position(template_path, phrase="THIS CERTIFICATE IS PROUDLY PRESENTED TO"):
    doc = fitz.open(template_path)
    page = doc[0]
    blocks = page.get_text("blocks")
    for b in blocks:
        text = b[4].strip().upper()
        if phrase in text:
            # b = (x0, y0, x1, y1, text, block_no, block_type)
            x_center = (b[0] + b[2]) / 2
            y_below = b[3] + 20  # 30pt below the phrase
            return x_center, y_below
    # Fallback: center of the page
    width, height = letter
    return width / 2, height / 2


def main():
    # Read recipient data
    df = pd.read_csv(CSV_PATH)
     # Find dynamic position for name
    name_x, name_y = find_name_position(TEMPLATE_PATH)


    for idx, row in df.iterrows():
        name = row['name']
        uuid = row['uuid']
       
        # Create a PDF in memory with the name
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont('PinyonScript', FONT_SIZE) 
        text_width = pdfmetrics.stringWidth(name, 'PinyonScript', FONT_SIZE)
        can.drawString(name_x - text_width / 2, name_y, name)  # Centered
        can.save()
        packet.seek(0)

        # Merge with template
        template_pdf = PdfReader(open(TEMPLATE_PATH, "rb"))
        new_pdf = PdfReader(packet)
        output = PdfWriter()

        # Merge the name onto the template
        page = template_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)

        # Save the result
        create_directory_if_not_exists(OUTPUT_DIR)
        output_path = f"{OUTPUT_DIR}/{uuid}_certificate.pdf"
        with open(output_path, "wb") as outputStream:
            output.write(outputStream)
        
        # Convert the first page of the PDF to a PNG image
        images = convert_from_path(output_path, first_page=0, last_page=1)
        if images:
            # Save the image to a file
            png_output_path = f"{OUTPUT_DIR}/{uuid}_certificate.png"
            images[0].save(png_output_path, 'PNG')


    print("Certificates generated successfully.")


if __name__ == '__main__':
    main()
