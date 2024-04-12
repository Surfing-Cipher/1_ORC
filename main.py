import os
from wand.image import Image
import pytesseract
from PIL import Image as PILImage


def save_pdf_pages_as_jpeg(pdf_filename):
    # Create a folder to save the images
    folder_name = pdf_filename.removesuffix(".pdf")
    # Create folder if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)

    # Create a text file to save OCR results with the same name as PDF
    text_filename = f"{
        folder_name}/{os.path.basename(pdf_filename).removesuffix('.pdf')}_ocr_result.txt"
    with open(text_filename, "w", encoding="utf-8") as text_file:
        with Image(filename=pdf_filename, resolution=120) as source:
            for i, image in enumerate(source.sequence):
                new_filename = f"{folder_name}/page_{i + 1}.jpeg"
                Image(image).save(filename=new_filename)

                # Perform OCR on the generated JPEG image
                ocr_result = pytesseract.image_to_string(
                    PILImage.open(new_filename))

                # Write the OCR result to the text file
                text_file.write(f"Text extracted from {new_filename}:\n")
                text_file.write(ocr_result + "\n")
                text_file.write("-----------------------------------------\n")

    print(f"OCR results saved to: {text_filename}")


pdf_filename = "NOLAN.pdf"
save_pdf_pages_as_jpeg(pdf_filename)
