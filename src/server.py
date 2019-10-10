from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.protocols.basic import LineOnlyReceiver


class Handler(LineOnlyReceiver):
    factory: 'Server'
    login: str

    def connectionMade(self):
        self.login = None
        self.factory.clients.add(self)
        print('Connected')

    def lineReceived(self, line):
        message = line.decode()

        if self.login is not None:
            message = f'<{self.login}>: {message}'
            for user in self.factory.clients:
                user.sendLine(message.encode())
                self.factory.new_message(message.encode())
        else:
            if message.startswith('login:'):
                login = message.replace('login:', '')
                if login not in [client.login for client in self.factory.clients]:
                    self.login = login
                    print(f'New user {self.login}')
                    self.sendLine(f'Welcome, {self.login}!'.encode())
                    for message in self.factory.send_history():
                        self.sendLine(message)
                else:
                    self.sendLine('This login is already in use!'.encode())
                    self.transport.loseConnection()
            else:
                self.sendLine('Wrong login'.encode())

    def connectionLost(self, reason=connectionDone):
        self.factory.clients.remove(self)
        print('Disconnected')


class Server(ServerFactory):
    protocol = Handler
    clients: set
    messages: list

    def __init__(self):
        self.clients = set()
        self.messages = list()

    def startFactory(self):
        print('Server started')

    def send_history(self):
        return self.messages

    def new_message(self, message):
        if len(self.messages) > 10:
            self.messages.pop(0)
        self.messages.append(message)


reactor.listenTCP(7410, Server())
reactor.run()