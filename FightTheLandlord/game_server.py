
import socket
from _thread import *
from queue import Queue
import random

HOST = ""
PORT = 15158
BACKLOG = 3

lastPlayed = None

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

def handleClient(client, serverChannel, cID):
  client.setblocking(1)
  msg = ""
  while True:
    msg += client.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverChannel.put(str(cID) + "_" + readyMsg)
      command = msg.split("\n")

def serverThread(clientele, serverChannel):
  while True:
    msg = serverChannel.get(True, None)
    print("msg recv: ", msg)
    senderID, msg = int(msg.split("_")[0]), "_".join(msg.split("_")[1:])
    print('!!!',msg)
    if msg.startswith('next'):
        changeCurrPlayer()
    #if msg.startswith('send'):
    #    global lastPlayed
    #    lastPlayed = msg
    else:
        for cID in clientele:
            #if cID != senderID:
            if len(msg)>0 and msg[0].isdigit():
                newmsg = ','.join(msg.split(' '))
                sendMsg = 'lastC' + newmsg + '\n'
                #"PlayerMoved " +  str(senderID) + " " + msg + "\n"
                clientele[cID].send(sendMsg.encode())
    clientele[currPlayer].send('turn\n'.encode())
    serverChannel.task_done()

def distributecard():
  cards = list(range(0,54))
  for player in range(3):
    for card in range(18):
      index = random.randint(0,len(cards)-1)
      if player == 0:
        player0.append(cards.pop(index))
      elif player == 1:
        player1.append(cards.pop(index))
      elif player == 2:
        player2.append(cards.pop(index))

currPlayer = 0
player0 = []
player1=[]
player2=[]
players = {0:player0,1:player1, 2:player2}
clientele = {}
currID = 0
First = 0
distributecard()

def changeCurrPlayer():
    global currPlayer
    currPlayer = (currPlayer + 1)%3

serverChannel = Queue(100)
start_new_thread(serverThread, (clientele, serverChannel))

while True:
    client, address = server.accept()
    print(currID)
    clientele[currID] = client
    for cID in clientele:
        clientele[cID].send(("newPlayer %d\n" % currID).encode())
        cards = str(players[cID])
        clientele[cID].send(('data'+cards + '\n').encode())
        #if lastPlayed != None:
        #    clientele[cID].send(lastPlayed.encode())
        if len(clientele) >= 2:
            clientele[cID].send("begin\n".encode())
    clientele[currPlayer].send("turn\n".encode())
        #if currPlayer == cID:
        #    clientele[cID].send("turn".encode())
    #clientele[currID] = client
    print("connection recieved")
    start_new_thread(handleClient, (client,serverChannel, currID))
    currID += 1
    #changeCurrPlayer()
    #print('turn',currPlayer)


