import socket
from jsonStream import readJSON, writeJSON


# On crée un socket client qui va tenter de se connecter au seveur (modèle sensé être statique, il doit donc être en dehors de la class)
def client_s():
    s_client = socket.socket()
    s_client.connect(('localhost', 3000))
    return s_client


class IAClient:
    def __init__(self, host=socket.gethostname(), port=9800):
        self._s = None
        self._host = host
        self._port = port
        self._board = None

    #Pour lancer le programme
    def run(self):
        self.subscribe()

    
    #Pour se connecter au serveur.
    def subscribe(self):
        ia_socket = client_s()
        try:
            # On lance l'inscription et on attend la réponse
            registration = {
                "request": "subscribe",
                "name": "les swaggs",
                "port": self._port,
                "matricules": ["195300", "195242"]
            }
            writeJSON(ia_socket, registration)
            message = readJSON(ia_socket)
            if message["response"] == "ok":
                self.listen(self._host)
                self.accept()
            else:
                print('Error')

        except OSError:
            print('Connexion avec le serveur non établie')

    #Pour écouter sur le certain port défini dans le constructeur
    def listen(self, host):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.bind(('localhost', self._port))
        self._s.listen(5)
        #backlog of size 5
        print('Listening on port {}'.format(self._port))

    #Pour attendre que les clients se connectent et les accepter
    def accept(self):
        print('Waiting for client to connect...')
        while True:
            ia, addr = self._s.accept()
            try:
                message = writeJSON(ia)
                print('Receiving message from {}'.format(addr))
                self.request(ia, message)

            except OSError:
                pass

    #Pour les requêtes 
    def request(self, ia, message):
        if message["request"] == "ping":
            writeJSON(ia, {"response": "pong"})

        if message["request"] == "play":
            print(message["request"])
            state = message['state']
            board = state['board']
            current = state['current']
            if current == 0:
                self.move(ia, board)
            else:
                self.move(ia, board, False)

    #Pour commencer à jouer et récupérer l'état du jeu, on appelle la class IAStrategy
    def play(self, to_move, ia):
        my_move = {
            "response": "move",
            "move": to_move,
            "message": "A joué"
        }
        writeJSON(ia, my_move)

    def give_up(self):
        writeJSON(self._s,{"response": "giveup",})

    def move(self, ia, board):
        pass


if __name__ == "__main__":
    IAClient().run()