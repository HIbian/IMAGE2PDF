import os.path
import sys

from img2pdf import Img2pdf

from jpg2pdfUI import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


def opendir(ui_label):
    path = QFileDialog.getExistingDirectory()
    ui_label.setText(path)


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        self.img_dir_btn.clicked.connect(lambda: opendir(self.img_dir))
        self.img_dir.textChanged.connect(self.setPDFNameAndOutPath)
        self.pdf_out_btn.clicked.connect(lambda: opendir(self.pdf_out))

        self.thread = Img2pdf()
        self.thread.signal.connect(self.updateprogress)
        self.start_btn.clicked.connect(self.startClicked)

    def startClicked(self):
        self.progressBar.setTextVisible(False)
        self.thread.setData(self.img_dir.text(), self.pdf_out.text(), self.pdf_name.text())
        self.thread.start()

    def updateprogress(self, count, total):
        print("{}/{}".format(count, total))
        self.progressBar.setMaximum(total)
        self.progressBar.setValue(count)
        if count == total:
            self.progressBar.setTextVisible(True)

    def setPDFNameAndOutPath(self):
        self.pdf_out.setText(self.img_dir.text())
        folder_name = os.path.split(self.img_dir.text())[-1]
        pdf_name = folder_name + ".pdf"
        self.pdf_name.setText(pdf_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())
