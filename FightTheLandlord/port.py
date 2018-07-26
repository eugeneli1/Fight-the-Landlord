import socket
from _thread import *
from queue import Queue

host = '128.237.221.255'
port = 1024

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = commland[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

try:
    server.connect(("128.237.134.183",port))

except socket.error as e:
    print(str(e))

serverMsg = Queue(100)
start_new_thread(handleServerMsg, (server, serverMsg))

 