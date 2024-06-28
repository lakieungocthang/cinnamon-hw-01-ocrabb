from tkinter import Image
from utils.FileType import FileType
from package import ImageHandler, DocxHandler, PDFHandler
class HandlerFactory:
    @staticmethod
    def create_handler(file_type):
        if file_type == FileType.IMAGE:
            return ImageHandler.ImageHandler()
        elif file_type == FileType.DOCX:
            return DocxHandler.DocxHandler()
        elif file_type == FileType.PDF:
            return PDFHandler.PDFHandler()
        else:
            return None
