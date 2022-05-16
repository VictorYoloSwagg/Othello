import socket
import json

ipserver="localhost"
port=3000
hisserverAddress=(ipserver,port)      #adresse de l'hôte du serveur
monip='0.0.0.0'
monport=7000
myserveraddress=(monip,monport)    
pong={"response": "pong"}
ping={"request": "ping"}

bord=[0,1,2,3,4,5,6,7,15,23,31,39,47,55,63,62,61,60,59,58,57,56,48,40,32,24,16,8] 
bordg=[0,8,16,24,32,40,48,56]     #bord gauche
bordd=[7,15,23,31,39,47,55,63]      #bord droit
bordh=[0,1,2,3,4,5,6,7]
borb=[56,57,58,59,60,61,62,63]


#LANCEMENT
def inscription():                                                 #fonction de depart qui se connecte au serveur de jeu et s'inscript
    with open ("inscription.json","r") as file:   
        data=file.read()                                           #contient les donnée d'inscription
    with socket.socket() as s:     
        s.connect(hisserverAddress)
        s.send(data.encode())  
        server()

def case():
    pass

def server():                                                      #fonction qui tourne en boucle
    with socket.socket() as s:                                     #renvoie pong quand reçoit ping
        s.bind(myserveraddress)                                    #renvoie un coup quand on lui en demande un
        s.listen() 
        while True:
            jeu, address=s.accept()
            message=json.loads(jeu.recv(2048).decode())
            if message==ping:
                jeu.send(json.dumps(pong).encode())
                

print("c'est parti !")                      
if __name__ == "__main__":
    inscription()
