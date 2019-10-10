from client.desktop_view import view


class Controller:
    def __init__(self):
        self.view = view.MessengerApp

    def message_received(self, line):
        self.view.messangesTextEdit.text(line)

    def message_sent(self, line):



