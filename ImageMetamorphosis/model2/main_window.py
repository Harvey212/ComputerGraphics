from PyQt5.QtWidgets import QMainWindow
from generate_file import Ui_MainWindow
from PyQt5 import QtCore
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)