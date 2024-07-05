import package.CustomHandler as CustomHandler
from package.ImageHandler import ImageHandler
import pymupdf
from PIL import Image
class PDFHandler(CustomHandler.CustomHandler):
    def __init__(self, type):
        super().__init__(type)

    def process(self, file):
        # Return result
        result = []

        # Image handler
        imageHandler = ImageHandler(self.type)
        out = {'raw': [], 'processed': []}
        with pymupdf.open(file) as doc:
            for page_count, page in enumerate(doc):
                # Convert a page to image
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                out['raw'].append(img)
                # Save image
                # Image processing
                image_res = imageHandler.process(img, page=page_count+1)
                out['processed'].extend(image_res['processed'])
        return out
