import time
import os

class tower:
    def __init__(self, full=False):
        if full:
            self.stack = [6,5,4,3,2,1]
            self.top = 6
        else:
            self.stack = [0,0,0,0,0,0]
            self.top = 0
    
    def pop(self):
        if self.top > 0:
            self.top -= 1
            temp = self.stack[self.top]
            self.stack[self.top] = 0
            return temp
        else:
            return -1

    def push(self,value):
        if self.top < 6:
            if self.top == 0:
                self.stack[self.top] = value
                self.top += 1
                return 0
            elif self.stack[self.top - 1] > value:
                self.stack[self.top] = value
                self.top += 1
                return 0
            return -2
        else:
            return -1
    
    def moveTo(self, tower):
        res = self.pop()
        if res == -1:
            return -1
        res2 = tower.push(res)
        if res2 != 0:
            self.push(res)
            return -2
        return 0
    
    def visualize(self):
        tree = {
            1:"/O\\",
            2:"/XAX\\",
            3:"/8/A\\8\\",
            4:"/OXOXOXO\\",
            5:"/()//A\\\\()\\",
            6:"/OX8XOXOX8XO\\",
            7:"/{}//()A()\\\\{}\\"
        }
        RED='\033[1;34m'
        GREEN='\033[1;32m'
        ORANGE='\033[1;33m'
        YELLOW='\033[1;33m'
        PURPLE='\033[1;35m'
        BLUE='\033[1;31m'
        CYAN='\033[1;36m'
        CLEAR='\033[0m'
        colored_tree = {
            1:"       {}/{}O{}\\{}       ".format(GREEN,RED,GREEN,CLEAR),
            2:"      {}/{}X{}A{}X{}\\{}      ".format(GREEN,PURPLE,GREEN,PURPLE,GREEN,CLEAR),
            3:"     {}/{}8{}/A\\{}8{}\\{}     ".format(GREEN,ORANGE,GREEN,BLUE,GREEN,CLEAR),
            4:"    {}/{}O{}X{}O{}X{}O{}X{}O{}\\{}    ".format(GREEN,RED,CLEAR,YELLOW,CLEAR,PURPLE,CLEAR,ORANGE,GREEN,CLEAR),
            5:"   {}/{}(){}//A\\\\{}(){}\\{}   ".format(GREEN,BLUE,GREEN,CYAN,GREEN,CLEAR),
            6:"  {}/{}O{}X{}8{}X{}O{}X{}O{}X{}8{}X{}O{}\\{}  ".format(GREEN,ORANGE,YELLOW,BLUE,YELLOW,RED,YELLOW,CYAN,YELLOW,CLEAR,YELLOW,PURPLE,GREEN,CLEAR),
            #7:"/[]//()A()\\\\[]\\{}".format(RED,CLEAR)
        }
        fin = []
        fin.append("                 " )
        fin.append("                 " )
        fin.append("                 " )
        fin.append("                 " )
        fin.append("        {}*{}        ".format(YELLOW,CLEAR) ) #fin.append("        *        " )
        for i in range(0,len(self.stack))[::-1]:
            fin.append("        {}|{}        ".format(ORANGE,CLEAR) )
            if self.stack[i] == 0:
                fin.append("        {}|{}        ".format(ORANGE,CLEAR) )#3 5 7 9 11 13 15, 17 MAX
            else:
                ss=colored_tree[self.stack[i]]
                #ss = "OOO"
                #if self.stack[i] > 1:
                #    for j in range(1,self.stack[i]):
                #        ss = "O" + ss + "O"
                while len(ss) < 17:
                    ss = " " + ss + " "
                fin.append(ss)
        fin.append("        {}|{}        ".format(ORANGE,CLEAR) )
        return fin

class game:
    def __init__(self,team):
        self.t1 = tower(full=True)
        self.t2 = tower()
        self.t3 = tower()
        self.team = team

    def visualize(self):
        for i in range(0,30):
       	    print("")
        santa = [
"         ____",
"       {} _  \\",
"          |__ \\",
"         /_____\\",
"         \o o)\)_______",
"         (<  ) /#######\\",
"       __{'~` }#########|",
"      /  {   _}_/########|",
"     /   {  / _|#/ )####|",
"    /   \_~/ /_ \  |####|",
"    \______\/  \ | |####|",
"    /\__________\|/#####|",
"   |  |__[X]_____/ \###/ ",
"    \/___________\\",
"       |    |/    |",
"       |___/ |___/",
"      _|   /_|   /",
"     (___,_(___,_)"
        ]
        RED='\033[0;31m'
        CLEAR='\033[0m'
        col_santa = [
"{}         ____{}".format(RED,CLEAR),
"{}       () _  \\{}".format(RED,CLEAR),
"{}          |__ \\{}".format(RED,CLEAR),
"{}         /_____\\{}".format(RED,CLEAR),
"{}         \o o)\)_______{}".format(RED,CLEAR),
"{}         (<  ) /#######\\{}".format(RED,CLEAR),
"{}       __|'~` |#########|{}".format(RED,CLEAR),
"{}      /  |   _|_/########|{}".format(RED,CLEAR),
"{}     /   |  / _|#/ )####|{}".format(RED,CLEAR),
"{}    /   \_~/ /_ \  |####|{}".format(RED,CLEAR),
"{}    \______\/  \ | |####|{}".format(RED,CLEAR),
"{}    /\__________\|/#####|{}".format(RED,CLEAR),
"{}   |  |__[X]_____/ \###/ {}".format(RED,CLEAR),
"{}    \/___________\\{}".format(RED,CLEAR),
"{}       |    |/    |{}".format(RED,CLEAR),
"{}       |___/ |___/{}".format(RED,CLEAR),
"{}      _|   /_|   /{}".format(RED,CLEAR),
"{}     (___,_(___,_){}".format(RED,CLEAR)
        ]
        f1 = self.t1.visualize()
        f2 = self.t2.visualize()
        f3 = self.t3.visualize()
        #print(len(f1))
        #print(len(santa))
        last = ""
        for i in range(0,len(f1)):
            last += f1[i] + f2[i] + f3[i] + col_santa[i] + '\n'
        print(last)
    
    def isDone(self):
        #print(self.t1.stack)
        #print(self.t2.stack)
        #print(self.t3.stack)
        if self.t1.stack == [0,0,0,0,0,0] and self.t2.stack == [0,0,0,0,0,0] and self.t3.stack ==[6,5,4,3,2,1]:
            self.visualize()
            return True
        else:
            return False

    def makeMove(self,pos1,pos2):
        diccc = {'1':self.t1,'2':self.t2,'3':self.t3}
        res = diccc[pos1].moveTo(diccc[pos2])
        if res != 0:
            print("Invalid move, try again.")

    def play(self):
        while self.isDone() == False:
            self.visualize()
            pos1 = "wo"
            while pos1 not in ['1','2','3']:
                    pos1 = input("From which tower do you want to remove a block? (1,2, or 3) ")
            pos2 = "ge"
            while pos2 not in ['1','2','3']:
                    pos2 = input("Where do you want to place the block? (1,2, or 3) ")
            self.makeMove(pos1,pos2)

    def giveRiddle(self):
        rid = {
            1:"I'm a great place to stash a boat, but don't have enough water to help one float.\nIf you can't find me, don't lose faith, I'll still keep your clue safe.", #10
            2:"Timber! I call as I fall. Now I have a view of the lake and all the decorations a person could make.",#8
            3:"Need to make a call? I'm just down the hall.\nWant to travel time and space? I know just the place.\nSuperman needed to deal with something strange? I'm just the place to change.", #5
            4:"Need to make a call? I'm just down the hall.\nWant to travel time and space? I know just the place.\nSuperman needed to deal with something strange? I'm just the place to change.", #5
            5:"Look, it's a bird! No, it's a plane! No it's a ... duck?\nI think we need to take this from the top, go back to your starting spot.",#13
            6:"You will find me upon a shelf, but I am not like any elf. I used to be part of a tree, now there's knowledge inside of me.",#2
            7:"You will find me upon a shelf, but I am not like any elf. I used to be part of a tree, now there's knowledge inside of me.",#2
            8:"Timber! I call as I fall. Now I have a view of the lake and all the decorations a person could make.",#8
            9:"You will find me upon a shelf, but I am not like any elf. I used to be part of a tree, now there's knowledge inside of me.",#2
            10:"Need to make a call? I'm just down the hall.\nWant to travel time and space? I know just the place.\nSuperman needed to deal with something strange? I'm just the place to change.", #5
            11:"Need to make a call? I'm just down the hall.\nWant to travel time and space? I know just the place.\nSuperman needed to deal with something strange? I'm just the place to change." #5
        }
        print(rid[self.team])

while True:
    print("Welcome Scavenger Hunters!")
    team = input("\nWhich Team are you? (1-11) I would suggest not putting in other team numbers, since that would waste time\n")
    while team not in ['1','2','3','4','5','6','7','8','9','10','11']:
        team = input("Try again\n")
    team = int(team)
    g = game(team)
    print("\nGreat! Here is your task:")
    print("LJ got tasked to decorate the breakroom, so he decided to put a nice festive tree in there.")
    print("However, since he is so silly he put it in the far left corner instead on the far right corner! (so silly, right?)")
    print("Help LJ move the tree to the correct spot and he will tell you where to go next.")
    print("The catch is that you can only move one layer at a time, and a lower layer always has to be bigger than every layer sitting on top.")
    print("You move a layer by pressing 1,2 or 3 and then enter to select which top layer you wish to move.")
    print("Then, you press 1,2, or 3 then enter to select where do you want to place that layer.")
    print("Ilie coded this, so his amazing error checking should stop you from making illegal moves (I hope).")
    print("Once the whole tree is moved correctly, you will get the next riddle.")
    print("If you entered the wrong team number or wish to restart, just rerun the executable that is in your current folder.")
    print("Good Luck and Have Fun!!!\n")
    print("Due to questionable design choices, you have a minute to read your answer when you're done")
    g.play()
    print("Congratulations! Here is your next riddle:\nThis will dissapear in a minute, so I would write it down somewhere...\n")
    g.giveRiddle()
    time.sleep(60)
    os.system("clear")
    #for i in range(0,60):
    #    print("")
