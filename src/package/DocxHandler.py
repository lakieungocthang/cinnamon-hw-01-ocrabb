import package.CustomHandler as CustomHandler

class DocxHandler(CustomHandler.CustomHandler):
    def __init__(self, type):
        super().__init__(type)

    def process(self, file):
        pass
