import socket
from jsonStream import readJSON, writeJSON
from Strategy import strategyf, strategys


# On crée un socket client qui va tenter de se connecter au seveur (modèle sensé être statique, il doit donc être en dehors de la class)


def client_s():
    s_client = socket.socket()
    s_client.connect(('localhost', 3000))
    return s_client


#Pour envoyer le move qu'on veut faire


def move(move_played, ia):
    my_move = {
        "response": "move",
        "move": move_played,
        "message": "Fun message"
    }
    writeJSON(ia, my_move)


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
            readJSON(ia_socket, registration)
            message = writeJSON(ia_socket)
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
        '''backlog of size 5'''
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


    #Pour commencer à jouer et récupérer l'état du jeu, on appelle la class IAStrategy

    def play(self, ia, message):
        
        #On commence par récupérer les informations envoyée sur l'état du jeu
    
        state = message["state"]
        cases = message["cases"]
        current = message["current"]
        board = state["board"]
        print(board)
        print(cases)
        if current == 0:
            strategyf(board ,state)
            print('first')
        else:
            strategys(board ,state)
            print('second')

    def give_up(self):
        sendJSON(self._s,{"response": "giveup",})


if __name__ == "__main__":
    IAClient().run()