# Python Version 2.7.3
# File: minesweeper.py

from tkinter import *
from tkinter import messagebox as tkMessageBox
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from collections import deque
import random
import platform
import time
from datetime import time, date, datetime

### START - TO EDIT ###
HEIGHT = 28
WIDTH = 33


PERCENT_MINES = 0.2

# assert(WIDTH == 50 and HEIGHT == 28)  # we are hard coding now

### END - TO EDIT ###




# TODO edit this TEAM_NEXT_RIDDLE dict based on your location
TEAM_NEXT_RIDDLE={   # { team_lowercase : next_riddle_location }  # next_riddle_location must match the key in LOCATION_GET_HERE_RIDDLE
    "jack": "K", 
    "sally": "R",
    "zero": "Q",
    "claws": "I",
    "oogie": "S",
    "mayor": "R",
    "triplets": "O",
    "finkelstein": "P",
    "reaper": "P",
    "harlequin": "E", 
}

LOCATION_GET_HERE_RIDDLE={  # { location : riddle_to_get_here }
#Breakroom - Start (Stockings)
"X":"""
N/A
""",

#Laptop Station 1 (Connections/Streetview)
"I":"""
Looking in from the street 
You'll see something pretty neat 
Laptops causing feelings of glee 
As teams make connections easily
""",

#Laptop Station 2 (Minesweeper/Lakeview)
"G":"""
Look up from your screen 
Upon a lake so pristine
But watch your steps in this area 
There are mines that can scare 'ya
""",

#Visual Mural (Intern/locker area by Lakeview)
"L":"""
Look upon this work of art 
On the wall is where to start
Supposedly in view of a lake 
You'll find this claim a bit fake
""",

#Emoji Crypto Station (Bathroom Wall)
"S":"""
The bathrooms here are barely functional 
Easy there, try not to get too emotional. 
Solve this puzzle if you dare!
You should brush up on your Viginere.
""",

#Voice Recognition Station (Mini conference room 6 A Montana and Wyoming)
"A":"""
In Montana and Wyoming you might find 
Something that will blow your mind 
Say the words, like a magic spell 
And make sure to pronounce them well.
""",

#Wheel Crypto Station (Supply Room)
"E":"""
It may be a surprise
When, among the supplies,
You find a wheel you can turn.
It's not wheel of fortune;
Money, you won't earn.
But spin this wheel, and see what you learn!
""",

#Front Lobby TV (Picture Hunt)
"R":"""
Look for the post of a vigilant sentry 
Near the place that grants you entry 
And there upon the TV screen 
A familiar map will be seen 
""",

#Logic Gates (Parkview) 
"O":"""
In the place where you see the park,
Come and find our mark 
AND with these ORdinary gates
 Solve the puzzle to determine your fates
""",

#Origami Station (Bullpen)
"K":"""
An animal with horns upon its head 
Would choose this pen to make its bed 
Full of papers you can fold
To reveal secrets yet untold
""",

#Keep Talking and Nobody Explodes (Warehouse)
"P":"""
At this point you know the drill 
Head to LJ's _______ and Grill
One teammate will be blind
With help, the answers they will find
""",

#Breakroom - End (Decrypting laptop)
"Q":"""
It's time that we departed
Come back to where you started
Enter the letters from each station 
To begin your celebration
""",

#Fake/Deadend station (Warehouse lockboxes)
"F":""
} 




STATE_DEFAULT = 0
STATE_CLICKED = 1
STATE_FLAGGED = 2

BTN_CLICK = "<Button-1>"
BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"

window = None

class Minesweeper:

    def __init__(self, tk):

        # import images
        self.images = {
            "plain": PhotoImage(file = "images/tile_plain.gif"),
            "clicked": PhotoImage(file = "images/tile_clicked.png"),
            "mine": PhotoImage(file = "images/tile_mine.gif"),
            "flag": PhotoImage(file = "images/tile_flag.gif"),
            "wrong": PhotoImage(file = "images/tile_wrong.gif"),
            "background": PhotoImage(file = "images/tile_background.png"),
            "numbers": []
        }
        for i in range(1, 9):
            self.images["numbers"].append(PhotoImage(file = "images/tile-"+str(i)+".png"))

        # set up frame
        self.tk = tk
        self.frame = Frame(self.tk)
        self.frame.pack()

        # set up labels/UI
        self.labels = {
            "time": Label(self.frame, text = "00:00:00"),
            "mines": Label(self.frame, text = "Mines: 0"),
            "flags": Label(self.frame, text = "Flags: 0")
        }
        self.labels["time"].grid(row = 0, column = 0, columnspan = WIDTH) # top full width
        self.labels["mines"].grid(row = HEIGHT+1, column = 0, columnspan = int(WIDTH/2)) # bottom left
        self.labels["flags"].grid(row = HEIGHT+1, column = int(WIDTH/2)-1, columnspan = int(WIDTH/2)) # bottom right

        self.restart() # start game
        self.updateTimer() # init timer
        
    def get_background_cords(self):
            '''
            Generate a list of (y,x) tuples that should be in the background
            This dude's x's and y's are messed up, don't blame me! (he is using row and column)
            In the scope of this function, the definition is right in this world.
            '''
            background_cords = []  # output list of (x,y) tuples
            
            # hard coding with HEIGHT = 28, WIDTH = 50
            #top_center = (25, 27)
            right_outline = [
            	(24,27), (25,27), # top
                (25,27), (40,17), (44,17), (48,10), (42,10), (49,3), (32,3),  # tips
                (43,18), (42,18), (42,19), (41,19), (40,19), (40,20), (39,20), (38,20), (38,21), (37,21), (36,21), (36,22), (35,22), (34,22), (34,23), (33,23), (32,23), (32,24), (31,24), (30,24), (30,25), (29,25), (28,25), (28,26), (27,26), (26,26), (25,26), (44,18), (45,17), (47,17), (43,18), # first branch
                (39,17), (43,17), (42,17), (41,17), (40,16), (41,16), (41,15), (42,15), (43,15), (43,14), (44,14), (45,14), (45,13), (46,13), (46,12), (47,12), (47,11), (48,11), (47,10), (46,10), (45,10), (44,10), (43,10), # second branch
                (41,10), (41,9), (42,9), (42,8), (43,8), (43,7), (44,7), (44,6), (45,6), (45,5), (46,5), (47,5), (47,4), (48,4), (47,4), # third branch
                (48,3), (47,3), (46,3), (45,3), (44,3), (43,3), (42,3), (41,3), (40,3), (39,3), (38,3), (37,3), (36,3), (35,3), (34,3), (33,3), (32,2), (32,1), (32,0)  #stump and bottom
            ]  
            # lazy rescaling from width 51 -> 33 (3/5)
            right_outline = [ (x*3//5, y) for (x,y) in right_outline ]
            
            # calculate all cells to the right of the outline
            for (x,y) in right_outline:
            	for xi in range(x,WIDTH):
            		background_cords.append( (xi,y) )
            		
            # mirror the background to the left side
            background_cords = background_cords + [(WIDTH-x-1,y) for (x,y) in background_cords]
            
            # convert from (x,y) to (r,c)
            return [(HEIGHT-y-1,x) for (x,y) in background_cords]
            

    def setup(self):
        # create flag and clicked tile variables
        self.flagCount = 0
        self.correctFlagCount = 0
        self.clickedCount = 0
        self.startTime = None
        
        # generate background list tiles
        background_cords = self.get_background_cords()

        # create buttons
        self.tiles = dict({})
        self.mines = 0
        for x in range(0, HEIGHT):
            for y in range(0, WIDTH):
                if y == 0:
                    self.tiles[x] = {}

                id = str(x) + "_" + str(y)
                isMine = False

                if (x,y) in background_cords:
                        gfx = self.images["background"]
                        tile = {
                            "id": id,
                            "isMine": isMine,
                            "state": STATE_CLICKED,
                            "coords": {
                                "x": x,
                                "y": y
                            },
                            "button": Button(self.frame, image = gfx),
                            "mines": 0 # calculated after grid is built
                        }
                        tile["button"].bind(BTN_CLICK, self.onClickWrapper(x, y))
                        #tile["button"].bind(BTN_FLAG, self.onRightClickWrapper(x, y))
                        tile["button"].grid( row = x+1, column = y ) # offset by 1 row for timer
                        
                        # fake the click for mine counts
                        self.clickedCount += 1
                else:
                        # tile image changeable for debug reasons:
                        gfx = self.images["plain"]

                        # currently random amount of mines
                        if random.uniform(0.0, 1.0) < PERCENT_MINES:
                            isMine = True
                            self.mines += 1

                        tile = {
                            "id": id,
                            "isMine": isMine,
                            "state": STATE_DEFAULT,
                            "coords": {
                                "x": x,
                                "y": y
                            },
                            "button": Button(self.frame, image = gfx),
                            "mines": 0 # calculated after grid is built
                        }

                        tile["button"].bind(BTN_CLICK, self.onClickWrapper(x, y))
                        tile["button"].bind(BTN_FLAG, self.onRightClickWrapper(x, y))
                        tile["button"].grid( row = x+1, column = y ) # offset by 1 row for timer

                self.tiles[x][y] = tile

        # loop again to find nearby mines and display number on tile
        for x in range(0, HEIGHT):
            for y in range(0, WIDTH):
                mc = 0
                for n in self.getNeighbors(x, y):
                    mc += 1 if n["isMine"] else 0
                self.tiles[x][y]["mines"] = mc
                
        # loop the background to set the edge tiles accordingly
        for (x,y) in background_cords:
            tile = self.tiles[x][y]
            if tile["mines"] > 0:
                tile["button"].config(image = self.images["numbers"][tile["mines"]-1])
        

    def restart(self):
        self.setup()
        self.refreshLabels()

    def refreshLabels(self):
        self.labels["flags"].config(text = "Flags: "+str(self.flagCount))
        self.labels["mines"].config(text = "Mines: "+str(self.mines))

    def gameOver(self, won):
        for x in range(0, HEIGHT):
            for y in range(0, WIDTH):
                if self.tiles[x][y]["isMine"] == False and self.tiles[x][y]["state"] == STATE_FLAGGED:
                    self.tiles[x][y]["button"].config(image = self.images["wrong"])
                if self.tiles[x][y]["isMine"] == True and self.tiles[x][y]["state"] != STATE_FLAGGED:
                    self.tiles[x][y]["button"].config(image = self.images["mine"])

        self.tk.update()

        #msg = "You Win! Play again?" if won else "You Lose! Play again?"
        #res = tkMessageBox.askyesno("Game Over", msg)
        # if res:
        #    self.restart()
        #else:
        #    self.tk.quit()
        
        while True:
            try:
                team = askstring(title="You win!", 
                    prompt="Congratulations! You have successfully defused and decorated your beautiful tree!\nWhat is your team name?:")
                team = team.lower().strip()
                riddle = LOCATION_GET_HERE_RIDDLE[TEAM_NEXT_RIDDLE[team]]
                break
            except Exception as e:
                pass  # bad team name

        tkMessageBox.showinfo("Riddle for team: " + team.upper(), riddle)
        self.restart()


    def updateTimer(self):
        ts = "00:00:00"
        if self.startTime != None:
            delta = datetime.now() - self.startTime
            ts = str(delta).split('.')[0] # drop ms
            if delta.total_seconds() < 36000:
                ts = "0" + ts # zero-pad
        self.labels["time"].config(text = ts)
        self.frame.after(100, self.updateTimer)

    def getNeighbors(self, x, y):
        neighbors = []
        coords = [
            {"x": x-1,  "y": y-1},  #top right
            {"x": x-1,  "y": y},    #top middle
            {"x": x-1,  "y": y+1},  #top left
            {"x": x,    "y": y-1},  #left
            {"x": x,    "y": y+1},  #right
            {"x": x+1,  "y": y-1},  #bottom right
            {"x": x+1,  "y": y},    #bottom middle
            {"x": x+1,  "y": y+1},  #bottom left
        ]
        for n in coords:
            try:
                neighbors.append(self.tiles[n["x"]][n["y"]])
            except KeyError:
                pass
        return neighbors

    def onClickWrapper(self, x, y):
        return lambda Button: self.onClick(self.tiles[x][y])

    def onRightClickWrapper(self, x, y):
        return lambda Button: self.onRightClick(self.tiles[x][y])

    def onClick(self, tile):
        # hard coding debug for get_background_cords haha -> make it pretty
        #x,y = int(tile["coords"]["x"]), int(tile["coords"]["y"])
        #print("({},{}), ".format(y,HEIGHT-1-x), end="")
        #return
        
        if self.startTime == None:
            self.startTime = datetime.now()

        if tile["isMine"] == True:
            # end game
            self.gameOver(False)
            return

        # conveinince function: autoclear if all neighboring bombs are cleared
        x,y = int(tile["coords"]["x"]), int(tile["coords"]["y"])
        # print("me:", tile)
        num_nmines_marked = 0
        for ntile in self.getNeighbors(x,y):
            if ntile["isMine"] == True and ntile["state"] == STATE_FLAGGED:
            	num_nmines_marked += 1
        if num_nmines_marked == tile["mines"]:
            self.clearSurroundingTiles(tile["id"])
            
        # change image
        if tile["state"] == STATE_CLICKED:
            pass
        elif tile["mines"] == 0:
            tile["button"].config(image = self.images["clicked"])
            self.clearSurroundingTiles(tile["id"])
        else:
            tile["button"].config(image = self.images["numbers"][tile["mines"]-1])
            
            
        # if not already set as clicked, change state and count
        if tile["state"] != STATE_CLICKED:
            tile["state"] = STATE_CLICKED
            self.clickedCount += 1
            
        # orig
        # if self.clickedCount == (HEIGHT * WIDTH) - self.mines:
        # hack - my counts are wild from convience functions and tree outline
        if self.clickedCount >= (HEIGHT * WIDTH) - self.mines and self.mines == self.flagCount:
            self.gameOver(True)

    def onRightClick(self, tile):
        if self.startTime == None:
            self.startTime = datetime.now()

        # if not clicked
        if tile["state"] == STATE_DEFAULT:
            tile["button"].config(image = self.images["flag"])
            tile["state"] = STATE_FLAGGED
            tile["button"].unbind(BTN_CLICK)
            # if a mine
            if tile["isMine"] == True:
                self.correctFlagCount += 1
            self.flagCount += 1
            self.refreshLabels()
        # if flagged, unflag
        elif tile["state"] == 2:
            tile["button"].config(image = self.images["plain"])
            tile["state"] = 0
            tile["button"].bind(BTN_CLICK, self.onClickWrapper(tile["coords"]["x"], tile["coords"]["y"]))
            # if a mine
            if tile["isMine"] == True:
                self.correctFlagCount -= 1
            self.flagCount -= 1
            self.refreshLabels()
        
        # hack - could they never win from a mine before?
        if self.clickedCount == (HEIGHT * WIDTH) - self.mines and self.mines == self.flagCount:
            self.gameOver(True)

    def clearSurroundingTiles(self, id):
        queue = deque([id])

        while len(queue) != 0:
            key = queue.popleft()
            parts = key.split("_")
            x = int(parts[0])
            y = int(parts[1])

            for tile in self.getNeighbors(x, y):
                self.clearTile(tile, queue)

    def clearTile(self, tile, queue):
        if tile["state"] != STATE_DEFAULT:
            return

        if tile["mines"] == 0:
            tile["button"].config(image = self.images["clicked"])
            queue.append(tile["id"])
        else:
            tile["button"].config(image = self.images["numbers"][tile["mines"]-1])

        tile["state"] = STATE_CLICKED
        self.clickedCount += 1

### END OF CLASSES ###

def main():
    # create Tk instance
    window = Tk()
    # set program title
    window.title("Minesweeper")
    # create game instance
    minesweeper = Minesweeper(window)
    # run event loop
    window.mainloop()

if __name__ == "__main__":
    main()
