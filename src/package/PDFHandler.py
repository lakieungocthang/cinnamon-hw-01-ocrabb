import package.CustomHandler as CustomHandler
from ImageHandler import ImageHandler
import pymupdf

class PDFHandler(CustomHandler.CustomHandler):
    def __init__(self, type):
        super().__init__(type)

    def process(self, file):
        # Return result
        result = []

        # Image handler
        imageHandler = ImageHandler()

        with pymupdf.open(file) as doc:
            for page_count, page in enumerate(doc):
                pix = page.get_pixmap()
                image_save = f"page_{page_count + 1}.png"
                pix.save(image_save)
                image_res = imageHandler.process(image_save)
                result.append(image_res)

        return result
