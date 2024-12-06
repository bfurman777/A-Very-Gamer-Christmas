#!/usr/bin/python3
# run from the wordle-cli directory!
# I am 7

import subprocess
import os
import signal
from threading import Thread
import time
import sys

RIDDLES = {
    2:"You will find me upon a shelf, but I am not like any elf. I used to be part of a tree, now there's knowledge inside of me.",
    3:"You can race against me, but never win. My hands make a circle, but I never spin. If you don't understand me, then with math you must begin. \nThe answer you seek is held upon my grin.",
    4:"Frosty the snowman has appeared on the scene, with his corn cob pipe, his button nose and his laptop screen. \nThere must have been some magic in that program that he found, for when he executed it he began to dance around.",
    5:"Need to make a call? I'm just down the hall. Want to travel time and space? I know just the place.\nSuperman needed to deal with something strange? I'm just the place to change.",
    6:"Take a seat and give a smile, it'll be on your badge for quite a while; behind you is the color blue, hope you see this clue through!",
    7:"Waters and computers don't typically mix, but for this I know a fix. Although they are in view of a lake, there is no water in their wake.",
    8:"Timber! I call as I fall. Now I have a view of the lake and all the decorations a person could make.",
    9:"When everything feels like its on fire, I will help make the situation less dire. If I am hard to see, use the color of a lemon to find me.\nI am usually kept away from others, in the place we've held celebrations for expectant mothers.",
    10:"I'm a great place to stash a boat, but don't have enough water to help one float. \nIf you can't find me, don't lose faith, I'll still keep your clue safe.",
    11:"Vehicles are a normal view, but turn around and you will see your holiday clue.",
    12:"Although my name suggests a place where you'd find mighty matadors. I instead contain desks and many office drawers. \nI am typically used by those who are just starting out, here they do their training and learn what the company's about.",
    13:"Look, it's a bird! No, it's a plane! No it's a ... duck? I think we need to take this from the top, go back to your starting spot."
}

TEAM_LOOKUP = { # teamNum:nextStation
    1:12,
    2:5,
    3:3,
    4:13,
    5:2,
    6:5,
    7:8,
    8:4,
    9:5,
    10:12,
    11:8
}

READING_TIME = 100  # sec to read solution
global p
pid = 0

def keep_wordle_alive_t():
    while 1:
        p = subprocess.Popen(["dist/wordle-cli", "random"])
        p.wait()
        os.system('clear')
        time.sleep(0.1)
        if os.path.exists('VICTORY_FLAG'):
            os.system('clear')
            while 1:
                try:
                    team_num = int(input('Enter team number: '))
                    next_station = TEAM_LOOKUP[team_num]
                    riddle = RIDDLES[next_station]
                    break
                except:
                    print('Invalid team number.')
                    pass  # loop again
            os.system('rm VICTORY_FLAG')
            print()
            print('For your next clue:')
            print()
            print('\t' + riddle)
            print('''
     .-"```"-.              
     /_\ _ _ __\\           
    | /{` ` `  `}             
   {.} {_,_,_,_,}           
       )/ a  a \(
      _()_          __
     { | /_)(_\ | }       _/  \\
   /`{ \        / }`\   _| `  |
  /   { '.____.' }   \ {_`-._/
 /     {_,    ,_}     \/ `-._}
|        `{--}`    \  /    /
|    /    {  }     | `    /
;    |    {  }     |\    /
 \    \   {__}     | '..'
  \_.-'}==//\\====/
  {_.-'\==\\//====\\
   |   ,)  ``     
    \__|          
            ''')
            input('Press enter to continue..')
            #time.sleep(READING_TIME)

keep_wordle_alive_t()