import os
import fitz  # pymupdf
from PyQt5.QtCore import QThread, pyqtSignal


class Img2pdf(QThread):
    signal = pyqtSignal(int, int)

    def __init__(self):
        super(Img2pdf, self).__init__()
        self.img_path = None
        self.out_path = None
        self.pdf_name = None

    def __del__(self):
        self.wait()

    def setData(self, img_path, out_path, pdf_name):
        self.img_path = img_path
        self.out_path = out_path
        self.pdf_name = pdf_name

    def run(self):
        self.convert()

    def convert(self):
        doc = fitz.open()
        img_dir = os.listdir(self.img_path)
        total = len(img_dir)
        count = 0
        for file_name in img_dir:
            count += 1
            self.signal.emit(count, total)
            if not (file_name.endswith('.jpg') or file_name.endswith('.png')):
                continue
            img_ab_path = self.img_path + os.sep + file_name
            imgdoc = fitz.open(img_ab_path)
            imgbytes = imgdoc.convert_to_pdf()
            imgpdf = fitz.open('pdf', imgbytes)
            doc.insert_pdf(imgpdf)

        doc.save(os.path.join(self.out_path, self.pdf_name))
        doc.close()

# img = Img2pdf()
# img.convert('E:\\图片\\NieR Art 幸田和磨アート集',
#             'E:\\图片\\NieR Art 幸田和磨アート集',
#             'NieR Art 幸田和磨アート集.pdf')
