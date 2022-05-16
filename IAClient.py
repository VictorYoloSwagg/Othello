from base64 import encode
import socket
import json
from Strategy import possibleMoves, myMove


ipserver="localhost"
port=3000
prof=(ipserver,port)      
monip='0.0.0.0'
monport=7900
moi=(monip,monport)    
pong={"response": "pong"}
ping={"request": "ping"}

#LANCEMENT
def inscription():                                                
    with open ("inscription.json","r") as file:   
        data=file.read()                                           
    with socket.socket() as s:     
        s.connect(prof)
        s.send(data.encode())  
        server()

def server():                                                      
    with socket.socket() as s:                                     
        s.bind(moi)                                    
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


print("connecté")                     
if __name__ == "__main__":
    inscription()
