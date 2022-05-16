from base64 import encode
import socket
import json
from Strategy import possibleMoves, myMove


ipserver="localhost"
port=3000
hisserverAddress=(ipserver,port)      #adresse de l'hôte du serveur
monip='0.0.0.0'
monport=7000
myserveraddress=(monip,monport)    
pong={"response": "pong"}
ping={"request": "ping"}

#LANCEMENT
def inscription():                                                 #fonction de depart qui se connecte au serveur de jeu et s'inscript
    with open ("inscription.json","r") as file:   
        data=file.read()                                           #contient les donnée d'inscription
    with socket.socket() as s:     
        s.connect(hisserverAddress)
        s.send(data.encode())  
        server()

def server():                                                      #fonction qui tourne en boucle
    with socket.socket() as s:                                     #renvoie pong quand reçoit ping
        s.bind(myserveraddress)                                    #renvoie un coup quand on lui en demande un
        s.listen() 
        while True:
            jeu, address=s.accept()
            message=json.loads(jeu.recv(2048).decode())
            if message==ping:
                jeu.send(json.dumps(pong).encode())
            elif message["request"] == "play":
                Etat = message["state"]
                Board = Etat["board"]
                print(Board)
                pmove = possibleMoves(Etat)
                print(pmove)
                MonMove = {}
                if len(pmove) == 0:
                   pass       
                else:
                    MonMove = myMove(Etat)
                    datas = json.dumps(MonMove)
                    jeu.send(bytes(datas, encoding="utf-8"))    
                    print("A joué")
            elif len(message) == 0:
                s.close()
            else:
                print(message)


print("c'est parti !")                     
if __name__ == "__main__":
    inscription()
