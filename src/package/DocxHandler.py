import package.CustomHandler as CustomHandler
from package.PDFHandler import PDFHandler
from utils.FileType import FileType
from docx2pdf import convert
import os
import tempfile


class DocxHandler(CustomHandler.CustomHandler):
    def __init__(self, type):
        super().__init__(type)

    def process(self, uploaded_file):
        if uploaded_file:
            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()
            temp_docx_path = os.path.join(temp_dir, uploaded_file.name)

            # Save uploaded file to the temporary path
            # May need to manually grant permission
            with open(temp_docx_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Convert to PDF and save to 'data' folder
            filename = os.path.splitext(os.path.basename(uploaded_file.name))[0]
            pdf_file_path = os.path.join('./data', filename + ".pdf")
            convert(temp_docx_path, pdf_file_path)

            # Process the PDF file
            PDFHandler(self.type).process(pdf_file_path)

            # Clean up the temporary directory
            os.remove(temp_docx_path)
            os.rmdir(temp_dir)
