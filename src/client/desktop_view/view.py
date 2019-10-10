from PyQt5 import QtWidgets
from client.desktop_view import gui


class MessengerApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.gui = gui.Ui_MainWindow
