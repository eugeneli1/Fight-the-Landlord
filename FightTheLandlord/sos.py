# from imagesdemo.py

from tkinter import *
import random

def init(data):
    loadPlayingCardImages(data) # always load images in init!
    data.allCards = [i for i in range(0,54)]
    data.cardsInHand = []
    data.player = "landlord"
    data.imageWidth = 71
    data.imageHeight = 96
    data.margin = 10
    cardsInHand(data)
    data.cardsWidth = len(data.cardsInHand)*data.imageWidth/4
    data.selCards = []

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

def cardsInHand(data):
    if data.player == "landlord":
        cards = 20
    else: cards = 17
    for i in range(cards):
        a = random.randint(0,len(data.allCards)-1)
        cardIndex = data.allCards.pop(a)
        data.cardsInHand.append(cardIndex)
    data.cardsInHand.sort()

def mousePressed(event, data):
    # cards left-top
    leftX = (data.width-data.cardsWidth)/2
    rightX = leftX + data.cardsWidth
    topY = data.height-data.margin-data.imageHeight
    bottomY = topY + data.imageHeight
    if leftX<event.x<rightX and topY<event.y<bottomY:
        selCard = int((event.x - leftX) // (data.imageWidth/4))
        if data.cardsInHand[selCard] not in data.selCards:
            data.selCards.append(data.cardsInHand[selCard])
        else: 
            index = data.selCards.index(data.cardsInHand[selCard])
            data.selCards.pop(index)
    


def keyPressed(event, data):
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    cardsWidth = len(data.cardsInHand)*data.imageWidth/4
    left = (data.width-data.cardsWidth)/2
    top = data.height - data.imageHeight - data.margin
    for cardIndex in data.cardsInHand:
        image = getPlayingCardImage(data, cardIndex)
        if cardIndex in data.selCards:
            canvas.create_image(left, top-10, anchor=NW, image=image)
        else: canvas.create_image(left, top, anchor=NW, image=image)
        left += data.imageWidth/4


####################################
# use the run function as-is
####################################

def run(width=500, height=500):
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
    # Create root before calling init (so we can create images in init)
    root = Tk()
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 250 # milliseconds
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
run(1065,600)