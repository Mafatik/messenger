import sys
from PyQt5 import QtWidgets
from src.client.view import view
# from .controller import controller
# from .model import model


def main():
    app = QtWidgets.QApplication(sys.argv)
    messenger_app = view.MessengerApp()
    messenger_app.show()
    app.exec_()


if __name__ == '__main__':
    main()