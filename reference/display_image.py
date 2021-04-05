from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import os


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle('My App')

        # The QImage class provides a hardware-independent image representation that allows direct access to the pixel
        # data, and can be used as a paint device.
        image = QImage(os.path.join('..', 'pics', 'under-a-cardinal-moon.jpg'))

        # manipulate image here

        pixmap = QPixmap().fromImage(image)

        label = QLabel()
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        self.setCentralWidget(label)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

# Start the event loop
app.exec_()
