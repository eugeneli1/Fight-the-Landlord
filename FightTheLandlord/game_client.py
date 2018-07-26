import socket
from _thread import *
from queue import Queue
from tkinter import *
import random
import copy

HOST = ""
PORT = 15158
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

####################################
# customize these functions
####################################

def init(data):
    data.waitingmode = True 
    data.gamemode = False 
    data.chupai = False
    loadPlayingCardImages(data)
    data.photogamebackground= PhotoImage(file = "gamebackground.gif")
    data.photofarmer1 = PhotoImage(file = "farmer1.gif")
    data.photofarmer2 = PhotoImage(file = "farmer2.gif") 
    data.photofarmer3 = PhotoImage(file = "farmer3.gif")  
    data.photostartbutton = PhotoImage(file = "startbutton.gif") 
    data.photoback = PhotoImage(file = "playing-card-gifs/x3.gif")
    data.allCards = [i for i in range(0,54)]
    # load data.xyz as appropriate
    data.curcard = [] 
    data.me = []
    data.otherStranger = []
    data.selCards = [] 
    data.conCards = [] 
    data.imageWidth = 71 ##########
    data.imageHeight = 96 #########
    data.margin = 10 ############
    data.last = []
    data.confirmColor = 'green'
    data.suibian = False
    
def drawwaitingmode(canvas,data):
    if data.waitingmode == True:
        if len(data.otherStranger) == 0:
            canvas.create_image(0.5*data.width, 0.7*data.height, 
                                image = data.photofarmer1)
        if len(data.otherStranger) == 1:
            canvas.create_image(0.1*data.width, 0.7*data.height, 
                                image = data.photofarmer2)
            canvas.create_image(0.5*data.width, 0.7*data.height, 
                                image = data.photofarmer1)
        if len(data.otherStranger) == 2:
            #canvas.create_image(0.5*data.width,0.5*data.height, 
            #                    image = data.photostartbutton) 
            canvas.create_image(0.8*data.width, 0.5*data.height, 
                            image = data.photofarmer3) 
            canvas.create_image(0.1*data.width, 0.7*data.height, 
                                image = data.photofarmer2)
            canvas.create_image(0.5*data.width, 0.7*data.height, 
                                image = data.photofarmer1)
                            
def gameinterface(canvas, data):  ##########
    if data.gamemode == True:
        canvas.create_image(data.width/2,data.height*0.7, image = data.photostartbutton) 
        canvas.create_image(0.1*data.width, 0.3*data.height, 
                            image = data.photostartbutton) 
        canvas.create_image(0.8*data.width, 0.3*data.height, 
                            image = data.photostartbutton)
        #drawOther(canvas,data)
        drawCardsInHand(canvas,data)

def drawOther(canvas,data):
    for i in range(len(data.otherStranger)):
            for j in range(1,len(data.otherStranger[i])):
                if i == 0:
                    if j == 0:
                        canvas.create_image(data.width*0.9,data.height*0.2, 
                                            image =data.photoback)
                    else:
                        canvas.create_image(data.width*0.9,
                       data.height*0.2 + data.height*0.025*j, image = data.photoback) 
                if i == 1:
                    if j == 0: 
                        canvas.create_image(data.width*0.2,data.height*0.2, 
                                            image =data.photoback)
                    else:
                        canvas.create_image(data.width*0.2,
                            data.height*0.2 + data.height*0.025*j, image = data.photoback)

def mousePressed(event, data):
    if (event.x >= data.width/2 - 123 and event.x <= data.width/2+123
        and event.y >= data.height/2 - 123 and event.y <= data.height/2 + 123):
        data.waitingmode = False 
            #data.gamemode = True
    if data.gamemode == True and data.chupai == True:
        #write when the mouse touches the card, add it to the cur. 
            #in it, also delete the card from the me
            #otherstrangers delete card 
        selectCards(event,data)
        print(data.selCards)
        confirmCards(event,data)
        passCards(event,data)
        cur = data.conCards
        if (event.x >= data.width/2 - 123 and event.x <= data.width/2 + 123 
            and event.y >= (data.height*0.7)-123 and event.y <= (data.height*0.7)+123):
            s = "%d " *len(cur)  + "\n"
            final = s[0:-2] + s[-1] 
            msg = final % tuple(cur) 
            data.server.send(msg.encode())
         


                    
def selectCards(event,data):
    leftX = (data.width-data.cardsWidth)/2
    rightX = leftX + data.cardsWidth
    topY = data.height-data.margin-data.imageHeight
    bottomY = topY + data.imageHeight
    if leftX<event.x<rightX and topY<event.y<bottomY:
        selCard = int((event.x - leftX) // (data.imageWidth/4))
        if selCard >= len(data.me):
            selCard = -1
        if data.me[selCard] not in data.selCards:
            data.selCards.append(data.me[selCard])
        else: 
            index = data.selCards.index(data.me[selCard])
            data.selCards.pop(index)

def confirmCards(event,data):
    topY = data.height - data.imageHeight - data.margin*5
    bottomY = topY + data.margin*2
    leftX = data.width/2 + data.margin
    rightX = leftX + data.margin*6
    if leftX < event.x < rightX and topY < event.y < bottomY:
        legal = getCombo(data.selCards, data.conCards)
        print('legal',legal)
        if data.suibian == True or (legal and data.selCards != []):
            if data.suibian == True: data.suibian = False
            data.conCards = data.selCards
            data.selCards = []
            #data.server.send(str(data.conCards).encode())
            for card in data.conCards:
                data.me.remove(card) ######data.cardsInHand
            data.chupai = False
        #data.server.send(('send' + str(data.conCards) + '\n').encode())
            data.server.send('next\n'.encode())
            data.confirmColor = 'green'
        else:
            data.confirmColor = 'red'

def passCards(event,data):
    topY = data.height - data.imageHeight - data.margin*5
    bottomY = topY + data.margin*2
    leftX = data.width/2 - data.margin*7
    rightX = leftX + data.margin*6
    if  leftX <= event.x <= rightX:
        if  topY <= event.y <= bottomY: # pass
            print('PASS!!')
            data.chupai = False
            data.server.send('pass\n'.encode())


def getCombo(selection, lastPlayerPlayed):
    if lastPlayerPlayed == []:
        return True
    if sorted(selection) == [52, 53]:
        return True
    if sorted(lastPlayerPlayed) == [52, 53]:
        return False
    prevresult = identifyCombo(lastPlayerPlayed)
    result = identifyCombo(selection)
    if (len(result) == 1 and type(result[0]) == Quad and 
        (len(prevresult) != 1)):
            return True
    TorQ = False
    if result == False: return False
    if len(result) != len(prevresult): return False
    for i in range(len(result)):
        if type(result[i]) != type(prevresult[i]): return False
        elif type(result[i]) == Triple or type(result[i]) == Quad:
            TorQ = True
    if TorQ:
        for i in range(len(result)):
            if type(result[i]) != Triple and type(result[i]) != Quad: 
                break
            if ((type(result[i]) != type(prevresult[i])) or (result[i] == prevresult[i]) 
                    or (result[i].compare(prevresult[i]) == False)):
                    return False
    else:
        for i in range(len(result)):
            if ((type(result[i]) != type(prevresult[i])) or (result[i] == prevresult[i])
                    or (result[i].compare(prevresult[i]) == False)):
                return False
    return True

def identifyCombo(selection):
    combos= []
    selection.sort()
    new = getCard(selection) # %13
    length = len(new)
    divide = separate(new)
    maxLen = findMax(divide)
    if len(selection) == 1: # single
        return [Single(selection)]
    if len(selection) == 2 and checkDouble(selection): # double
        return [Double(selection)]
    if len(selection) == 3 and checkTriple(selection): # triple
        return [Triple(selection)]
    if len(selection) == 4 and checkQuad(selection):
        return [Quad(selection)]
    if checkSequence(new): #  single sequence
        sequence = []
        for digit in new:
            sequence.append(Single([digit]))
        return sequence
    if len(divide) > 0:
        if checkDoubleSequence(divide): # all doubles
            sequence = []
            for digit in divide:
                sequence.append(Double(digit))
            return sequence
    for l in range(3,maxLen+1):
        test = copy.deepcopy(divide)
        result = checkSize(test,l)
        if result != False:
            return result
    return False

def checkDoubleSequence(L):
    rows = len(L)
    for i in range(rows):
        if len(L[i]) != 2:
            return False
    check = []
    for i in range(rows):
        check.append(L[i][0])
    mini = min(check)
    maxi = max(check)
    return check == list(range(mini,maxi+1)) and len(check) >= 3

def checkSize(divide,size):
    newdivide  = copy.deepcopy(divide)
    match = []
    for i in range(len(divide)):
        if len(divide[i]) >= size:
            match.append(i)
    mini = min(match)
    maxi = max(match)
    matchCount = len(match) # how many triples/quad
    if match != list(range(mini,maxi+1)): return False
    # the continue stops at i
    for i in range(mini,maxi+1):
        for remove in range(size):
            divide[i].pop()
    left = count2DLength(divide) # num lefting
    if matchCount == left: 
        return SizeDaiSingleOrDouble(newdivide, match, divide, size)
    if not Dai(divide): return False # if one is more than 2
    double = ifAllDouble(divide)
    if double !=False and double == matchCount:
        return SizeDaiSingleOrDouble(newdivide, match, divide, size) # size dai double
    if getDoubleSingleCombo(divide) == matchCount: 
        return SizeDaiSingleOrDouble(newdivide, match, divide, size)
    return False 

def SizeDaiSingleOrDouble(divide, match, left, size):
    result = []
    for matchI in match:
        num = divide[matchI][0]
        numList = [num] * size
        if size == 3:
            result.append(Triple(numList))
        elif size == 4:
            result.append(Quad(numList))
    for remain in left:
        if len(remain) == 1:
            result.append(Single(remain))
        elif len(remain) ==2:
            result.append(Double(remain))
    return result

def checkSequence(new):
    if 14 in new: return False
    mini = min(new)
    maxi = max(new)
    return new == list(range(mini,maxi+1)) and len(new) >= 5


def Dai(left):
    for value in left:
        if len(value) != 0 and len(value) > 2:
            return False
    return True

def getDoubleSingleCombo(L):
    count = 0
    for value in L:
        if len(value) >0: count+=1
    return count

def ifAllDouble(L):
    count = 0
    for value in L:
        if len(value) != 0 and len(value) != 2:
            return False
        else: count+=1
    return count

def count2DLength(L):
    count = 0
    for value in L:
        count += len(value)
    return count

def findMax(L):
    longest = 0
    for value in L:
        if len(value) > longest:
            longest = len(value)
    return longest


def checkQuad(selection):
    num = selection[0]
    return selection.count(num) == 4

def separate(selection):
    combos = []
    for digit in range(0,17):
        count = selection.count(digit)
        if count >0:
            combos.append([digit]*count)
    return combos

def checkDouble(cards):
    num = cards[0]
    return cards.count(num) ==2

def checkTriple(cards):
    num = cards[0]
    return cards.count(num) == 3

def checkQuad(cards):
    num = cards[0]
    return cards.count(num) == 4


curSelection = []

def isLegal(lastPlayerPlayed, curSelection):
    pass


def getCard(selection):
    new = []
    for num in selection:
        if num == 52:
            new.append(15) # little joker
        elif num == 53:
            new.append(16) # big joker
        elif num%13 == 0:
            new.append(13) #A
        elif num%13 == 1:
            new.append(14)
        else:
            new.append(num%13)
    return new

def suitToCard(x):
    if x == 52:
        return 15 # little joker
    elif x == 53:
        return 16 # big joker
    elif x%13 == 0:
        return 13 #A
    elif x%13 == 1:
        return 14
    else:
        return x%13



class Single(object):
    def __init__(self, card):
        self.cards = card
        self.suitX = card[0]
        self.cardX = suitToCard(self.suitX)
    def __repr__(self):
        return 'Single' + str(self.cards)
    def __eq__(self,other):
        return isinstance(other, Single) and (self.cardX == other.cardX)
    def compare(self,other):
        if self.cardX == other.cardX: return False
        return self.cardX > other.cardX
    def __hash__(self):
        return hash(self.suitX)

class Double(Single):
    def __init__(self,cards):
        super().__init__(cards)
        self.suitY = cards[1]
        self.cardY = suitToCard(self.suitY)
    def __repr__(self):
        return 'Double' + str(self.cards)
    def __eq__(self, other):
        return (isinstance(other, Double) and 
            self.cardX == other.cardX)
    def compare(self, other):
        super().compare(other)


class Triple(Double):
    def __init__(self, cards):
        super().__init__(cards)
        self.suitZ = cards[2]
        self.cardZ = suitToCard(self.suitZ)
    def __repr__(self):
        return 'Triple' + str(self.cards)
    def __eq__(self, other):
        return (isinstance(other, Triple) and self.cardX == other.cardX)
    def compare(self, other):
        super().compare(other)

class Quad(Triple):
    def __init__(self, cards):
        super().__init__(cards)
        self.suitA = cards[3]
        self.cardA = suitToCard(self.suitA)
    def __repr__(self):
        return 'Quad' + str(self.cards)
    def __eq__(self, other):
        return (isinstance(other, Quad) and self.cardA == other.cardA)
    def compare(self, other):
        super().compare(other)

def loadPlayingCardImages(data):
    cards = 55 # cards 1-52, joker1, joker2, back
    data.cardImages = [ ]
    for card in range(cards):
        rank = (card%13)+1
        suit = "cdhsx"[card//13]
        filename = "playing-card-gifs/%s%d.gif" % (suit, rank)
        data.cardImages.append(PhotoImage(file=filename))

def getPlayingCardImage(data, cardIndex):
    return data.cardImages[cardIndex]

def getSpecialPlayingCardImage(data, name):
    specialNames = ["back", "joker1", "joker2"]
    return getPlayingCardImage(data, specialNames.index(name)+1, "x")
'''
def drawConfirmButton(canvas,data):
    topY = data.height - data.imageHeight - data.margin*5
    bottomY = topY + data.margin*2
    leftX = data.width/2 + data.margin
    rightX = leftX + data.margin*6
    canvas.create_rectangle(leftX,topY,rightX,bottomY,fill="yellow")
    canvas.create_text(data.width/2+data.margin*4,topY,text="Confirm",anchor=N)
'''

def drawConfirmButton(canvas,data):
    topY = data.height - data.imageHeight - data.margin*5
    bottomY = topY + data.margin*2
    leftX = data.width/2 + data.margin
    rightX = leftX + data.margin*6
    canvas.create_rectangle(leftX,topY,rightX,bottomY,fill=data.confirmColor)
    canvas.create_text(data.width/2+data.margin*4,topY,text="Confirm",anchor=N)


def drawPassButton(canvas,data):
    topY = data.height - data.imageHeight - data.margin*5
    bottomY = topY + data.margin*2
    leftX = data.width/2 - data.margin*7
    rightX = leftX + data.margin*6
    canvas.create_rectangle(leftX,topY,rightX,bottomY,fill="yellow")
    canvas.create_text(data.width/2-data.margin*4,topY,text="Pass",anchor=N)

def drawCards(canvas,data):
    drawCardsInHand(canvas,data)
    #drawOther(canvas,data)
    drawConfirmCards(canvas,data)

def drawCardsInHand(canvas,data):
    data.cardsWidth = len(data.me)*data.imageWidth/4 + data.imageWidth*3/4
    left = (data.width-data.cardsWidth)/2
    top = data.height - data.imageHeight - data.margin
    for cardIndex in data.me:
        image = getPlayingCardImage(data, cardIndex)
        if cardIndex in data.selCards:
            canvas.create_image(left, top-10, anchor=NW, image=image)
        else: canvas.create_image(left, top, anchor=NW, image=image)
        left += data.imageWidth/4

def drawConfirmCards(canvas,data):
    conCardsWidth = len(data.conCards)*data.imageWidth/4 + data.imageWidth*3/4
    left = (data.width-conCardsWidth)/2
    top = data.height/2 - data.imageHeight/2
    for cardIndex in data.conCards:
        image = getPlayingCardImage(data, cardIndex)
        canvas.create_image(left, top, anchor=NW, image=image)
        left += data.imageWidth/4
    #for cardIndex in data.last:
    #    image = getPlayingCardImage(data, cardIndex)
    #    canvas.create_image(left, top, anchor=NW, image=image)
    #    left += data.imageWidth/4

def gameRedrawAll(canvas,data):
    canvas.create_rectangle(0,0,data.width+100,data.height+100, fill = 'RoyalBlue4')

def keyPressed(event, data):
    pass



def timerFired(data):
    if (serverMsg.qsize() > 0):
        message = serverMsg.get(False)
        #try:
        print("recieved: ", message)
        if message.startswith("newPlayer"):
          msg = message.split()
          print(msg)
          newPID = int(msg[1])
          data.otherStranger.append([newPID])
          print(data.otherStranger)
        elif message.startswith("playerMoved"):
            print(msg)
            msg = message.split()
            PID = int(msg[1])
            print(msg)
            if len(msg) == 36:
                ls1 = msg[1:18]
                ls2 = msg[18:35]  
                data.otherStranger[0] += ls1
                data.otherStranger[1] += ls2 
            if len(msg) < 36:
                data.curcard = [] 
                for num in msg:
                    data.curcard += [num] 
                for i in range(len(data.otherStranger)):
                    if data.otherStranger[i][0] == PID:
                        mark = i
                for j in range(len(data.curcard)):
                    data.otherStranger[mark].remove(data.curcard[j])
        elif message.startswith('data'):
            data.me = convertToList(message[5:-1])
        elif message.startswith('begin'):
            #data.waitingmode == False
            data.gamemode = True
        elif message.startswith('turn'):
            data.chupai = True
        #if message.startswith('send'):
        #    data.conCards = convertToList(message[5:-1])
        elif message.startswith('lastC'):
            data.conCards = convertToList(message[5:])
            data.last = data.conCards
        elif message.startswith('suibian'):
            data.suibian = True

        #except:
        #     print("failed!")
        #serverMsg.task_done()

def convertToList(msg):
    new = []
    print('!!!',msg)
    for value in msg.split(','):
        new.append(int(value))
    return new


def redrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2,image = data.photogamebackground)
    drawwaitingmode(canvas, data) 
    gameinterface(canvas, data)
    drawCards(canvas,data)
    #drawOther(canvas,data)
    drawConfirmButton(canvas,data)
    drawPassButton(canvas,data)
    if data.chupai == True and data.gamemode == True:
        canvas.create_rectangle(10,10,90,50, fill = 'black')
        canvas.create_text(50,30, text = "Your Turn", font = "arial 20", fill = 'white')
    
    
    
####################################
# use the run function as-is
####################################

def run(width, height, serverMsg=None, server=None):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.server = server
    data.serverMsg = serverMsg
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

serverMsg = Queue(100)
start_new_thread(handleServerMsg, (server, serverMsg))

run(1065, 600, serverMsg, server)
