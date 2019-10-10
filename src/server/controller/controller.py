from server.model import model


class Controller:
    def __init__(self, server_model: model.Server):
        self.model = server_model

    def getMessage(self):
