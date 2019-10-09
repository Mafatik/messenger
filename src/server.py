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
                if user is not self:
                    user.sendLine(message.encode())
        else:
            if message.startswith('login:'):
                login = message.replace('login:', '')
                if login not in [client.login for client in self.factory.clients]:
                    print(f'New user {self.login}')
                    self.login = login
                    self.sendLine(f'Welcome, {self.login}!'.encode())
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

    def __init__(self):
        self.clients = set()

    def startFactory(self):
        print('Server started')


reactor.listenTCP(7410, Server())
reactor.run()