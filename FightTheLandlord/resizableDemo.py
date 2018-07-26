# resizableDemo.py
# with sizeChanged (Configure) event
# and with minsize

from tkinter import *

####################################
# customize these functions
####################################

def init(data): pass
def mousePressed(event, data): pass
def keyPressed(event, data): pass
def timerFired(data): pass

def redrawAll(canvas, data):
    # Draw the demo info
    font = ("Arial", 16, "bold")
    msg = "Resizable Demo"
    canvas.create_text(data.width/2, data.height/3, text=msg, font=font)
    # Draw the canvas size
    size = ( data.width, data.height )
    msg = "size = " + str(size)
    canvas.create_text(data.width/2, data.height*2/3, text=msg, font=font)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
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
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)

    # Note change #1 (change how we pack):
    # canvas.pack()
    canvas.pack(fill=BOTH, expand=YES)

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    # Note change #2:
    def sizeChanged(event):
        data.width = event.width - 4
        data.height = event.height - 4
        redrawAllWrapper(canvas, data)
    root.bind("<Configure>", sizeChanged)
    root.minsize(204,104) # 4 extra pixels for frame boundaries

    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 200)
