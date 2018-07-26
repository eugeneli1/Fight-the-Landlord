# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
import random

####################################
# customize these functions
####################################
# MODE DISTRIBUTOR

def init(data):
    # load data.xyz as appropriate
    data.screen = PhotoImage(file='screen.gif')
    data.mode = 'splashscreen'
    data.prevMode = None
    if data.mode == 'splashscreen':
        help = Button(data.root, text="Help", command=lambda:onButton(data,2))
        help.pack()
    # game mode below
    data.counter = 0
    loadPlayingCardImages(data) # always load images in init!
    data.allCards = [i for i in range(0,54)]
    data.cardsInHand = []
    data.player = "landlord"
    data.imageWidth = 71
    data.imageHeight = 96
    data.margin = 10
    cardsInHand(data)
    data.selCards = [] # selected cards
    data.conCards = [] # confirmed cards

#########################
# buttons
#########################

def onButton(data, buttonId):
    if (buttonId == 1): restartPressed(data)
    elif (buttonId == 2): helpPressed(data)

def restartPressed(data):
    data.mode = 'splashscreen'

def helpPressed(data):
    if data.mode == 'help': return
    data.prevMode = data.mode
    data.mode = 'help'

def startButtonRange(x,y):
    if x in range(411,658) and y in range(450,557):
        return True
    else:
        return False

def mousePressed(event, data):
    # use event.x and event.y
    if data.mode == 'splashscreen': splashscreenMousePressed(event,data)
    elif data.mode == 'help': helpMousePressed(event,data)
    elif data.mode == 'game': gameMousePressed(event,data)

def keyPressed(event, data):
    pass

def timerFired(data):
    gameTimerFired(data)

def redrawAll(canvas, data):
    # draw in canvas
    if data.mode == 'splashscreen': splashscreenRedrawAll(canvas,data)
    elif data.mode == 'help': helpRedrawAll(canvas,data)
    elif data.mode == 'game': gameRedrawAll(canvas,data)


#########################
# splashscreen mode
#########################

def splashscreenMousePressed(event,data):
    x = event.x
    y = event.y
    if startButtonRange(x,y):
        data.mode = 'game'

def splashscreenRedrawAll(canvas,data):
    canvas.create_image(0, 0, anchor=NW, image=data.screen)
    pass

#########################
# game mode
#########################

def gameMousePressed(event,data):
    selectCards(event,data)
    confirmCards(event,data)

def selectCards(event,data):
    leftX = (data.width-data.cardsWidth)/2
    rightX = leftX + data.cardsWidth
    topY = data.height-data.margin-data.imageHeight
    bottomY = topY + data.imageHeight
    if leftX<event.x<rightX and topY<event.y<bottomY:
        selCard = int((event.x - leftX) // (data.imageWidth/4))
        if selCard >= len(data.cardsInHand):
            selCard = -1
        if data.cardsInHand[selCard] not in data.selCards:
            data.selCards.append(data.cardsInHand[selCard])
        else: 
            index = data.selCards.index(data.cardsInHand[selCard])
            data.selCards.pop(index)

def confirmCards(event,data):
    topY = data.height - data.imageHeight - data.margin*5
    bottomY = topY + data.margin*2
    leftX = data.width/2 + data.margin
    rightX = leftX + data.margin*6
    if leftX < event.x < rightX and topY < event.y < bottomY:
        if data.selCards != []:
            data.conCards = data.selCards
            data.selCards = []
            for card in data.conCards:
                data.cardsInHand.remove(card)

def loadPlayingCardImages(data):
    cards = 55 # cards 1-52, joker1, joker2, back
    data.cardImages = [ ]
    for card in range(cards):
        rank = (card%13)+1
        suit = "cdhsx"[card//13]
        filename = "playing-card-gifs/%s%d.gif" % (suit, rank)
        data.cardImages.append(PhotoImage(file=filename))
    filename = "poker.png"
    data.background.append(PhotoImage(file=filename))

def getPlayingCardImage(data, cardIndex):
    return data.cardImages[cardIndex]

def getSpecialPlayingCardImage(data, name):
    specialNames = ["back", "joker1", "joker2"]
    return getPlayingCardImage(data, specialNames.index(name)+1, "x")

def cardsInHand(data):
    if data.player == "landlord":
        cards = 20
    else: cards = 17
    for i in range(cards):
        a = random.randint(0,len(data.allCards)-1)
        cardIndex = data.allCards.pop(a)
        data.cardsInHand.append(cardIndex)
    data.cardsInHand.sort()

def drawConfirmButton(canvas,data):
    topY = data.height - data.imageHeight - data.margin*5
    bottomY = topY + data.margin*2
    leftX = data.width/2 + data.margin
    rightX = leftX + data.margin*6
    canvas.create_rectangle(leftX,topY,rightX,bottomY,fill="yellow")
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
    drawConfirmCards(canvas,data)

def drawCardsInHand(canvas,data):
    data.cardsWidth = len(data.cardsInHand)*data.imageWidth/4 + data.imageWidth*3/4
    left = (data.width-data.cardsWidth)/2
    top = data.height - data.imageHeight - data.margin
    for cardIndex in data.cardsInHand:
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

def gameRedrawAll(canvas,data):
    canvas.create_rectangle(0,0,data.width+100,data.height+100, fill = 'RoyalBlue4')
    drawCards(canvas,data)
    drawConfirmButton(canvas,data)
    drawPassButton(canvas,data)

#########################
# help mode
#########################
def helpMousePressed(event,data):
    x = event.x
    y = event.y
    if x in range(800,950) and y in range(50,100):
        data.mode = data.prevMode

def helpRedrawAll(canvas,data):
    instruction = '''
    Instructions:

    1) A shuffled pack of 54 cards is dealt to three players.
    2) Each player is dealt 17 cards, faced down, with the last three leftover 
        cards detained on the playing desk.
    3) During the dealting, one card will be randonmly faced up, the player who 
        gets it becomes the landlord.



    Winning Rule:

    If the landlord runs out of card before any other players, then he/she wins.
    But, if there is one or more other players runs out of cards, then the landlord
    loses.
    '''
    canvas.create_rectangle(0,0,data.width,data.height, fill= 'SteelBlue1')
    canvas.create_text(data.width/2,data.height/2, 
                        text = instruction, font = "times 20")
    canvas.create_rectangle(800,50,950,100, fill = 'RoyalBlue4')
    canvas.create_text((800+950)/2,(50+100)/2,text = 'Go Back', 
        font = "times 30 bold")


####################################
# use the run function as-is
####################################
def run(width=1065, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
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
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds

    # create the root and the canvas (Note Change: do this BEFORE calling init!)
    root = Tk()
    root.configure(background = "RoyalBlue4")
    # Store root in data so buttons can access
    data.root = root

    init(data)
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

run()