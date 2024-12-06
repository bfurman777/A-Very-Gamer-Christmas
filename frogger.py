#!/usr/bin/env python3

import os
import random
import time

DEBUG = False

LOCATION_GET_HERE_RIDDLE = {  # {location:riddle_to_get_here}
2 :
"Through the entrance by a Puerto Rican's car, \n\
If you feel secure you've gone too far.\n\
Park here only if you dare.\n\
Of he-who-shall-not-be-named you must beware.",

3:
"At this station you will find,\n\
A game to test your mind,\n\
If you dare to try to play,\n\
be prepared to type away,\n\
near a certain flightless bird,\n\
even though that sounds absurd.",

4:
"I am guarded all day and night,\n\
Enter here to start the day right,\n\
You can sit and relax in this comfy spot,\n\
And take in the sight of the parking lot.",

5:
"A royal game with lots of fun.\n\
Trap the king and them you're done.\n\
Gather round near the street.\n\
See which opponents you can beat.",

6:
"Between two rooms where privacy is sought,\n\
I stand on the wall, information fraught.\n\
rights and regulations, my messages impart,\n\
A silent guardian, close to the beating heart.",

7:
"A room small\n\
Can be the most important of all\n\
Once a place where water flows\n\
Now a room where quiet goes\n\
Zooming there with all your might\n\
Make sure the sign is right",

8:
"Go hop over to the lake,\n\
On a device with a solid state.\n\
There a game you will play\n\
And the next riddle it will say.",

9:
"You can ask me to make you a work of art.\n\
All you have to do is simply press 'Start',\n\
I'll spit it out for you to enjoy,\n\
But take care for my canvas can be easy to destroy.\n\
Luckily, you can find more in an abundant supply,\n\
In one of the many cabinets nearby.",

10:
"Wood-clad sentinels, in silent row we stand,\n\
Watching cars come and go, across the painted land.\n\
We hold secrets, whispered and untold,\n\
Treasure hidden, both new and old.",

11:
"I stand as a guardian at an entrance's gate,\n\
ensuring no unwanted items find their fate.\n\
With my watchful gaze and sensitive touch,\n\
I detect the presence of devices, oh so much.\n\
But my senses, alas, are not always keen,\n\
and false alarms often pierce the scene.\n\
A friendly voice, though often astray,\n\
Announces my findings, day by day.",

12:
"The holidays can be celebrated in many ways,\n\
sometimes navigating the traditions can be a maze.\n\
Stick to your path, follow what you know,\n\
at the end your next step it will show.",

13:
"Travel near and travel far\n\
Maybe have a drink at the bar.\n\
do you recall the path you took?\n\
Have the host take a look!",
}

TEAM_NEXT_RIDDLE = {  # { team:next_riddle_location }
    1: 13,
    2: 9,
    3: 4,
    4: 9,
    5: 3,
    6: 2,
    7: 7,
    8: 10,
    9: 5,
    10: 5,
    11: 6,
    12: 10
}
RIDDLE_TIMER = 75 # sec

# You start at the bottom, row# ROWS-1
COLS = 12
ROWS = 14

BOARD = [['.']*COLS for i in range(ROWS)]

VALID_MOVES = ['n', 's', 'e', 'w', 'c']

# board icons
ROAD = '--'
WATER = '~~'
FROG = 'YOU'
LOG = 'log'
CAR = 'car'
GOAL = 'WIN'

# keys in the player struct
R = 'row'
C = 'colm'
# misc keys
LEFT = 'left'
MID = 'middle'
RIGHT = 'right'

# death reasons
CAR_ACCIDENT = 'A car runs you over, flattening you instantly. Maybe look both sides before crossing the street!'
DROWNDED = 'You fall into the water, but you do not know how to swim! Perhaps you should wait for something to hop on?'
FELL_OFF_MAP = 'You fall off of the predefined bounds of your world. Don\'t try thinking outside the box.'
RIDDLE_EXPIRED = 'Riddle timer expired. Your riddle was stolen. Try again!'


# ROWS-1 == 13 is the starting row
# 12 is a road, with cars in front of and to the left of the player
# 11 is safe
# 10,9,8 is roads
# 7 is safe
# 6 is a river
# 5 is safe
# 4,3 is a double river
# 2 is victory
# 0,1 is unused (at least 1 needs to be unused for bounds checks)
VICTORY_ROW = 2

# dictionary with {row: [idx with an item on it]}
ROAD_ROWS = {   # cars on the road; if there are no cars, this is a field of grass, not a road
    13: [],
    12: [],  # will be populated
    11: [],
    10: [],  # will be populated
    9: [],  # will be populated
    8: [],
    7: [],
    5: [],
    2: []
    }   
RIVER_ROWS = {  # 
    6: [1,2, 5,6,7, 10,11],
    4: [3,4, 6,7, 10,11],
    3: [2,3, 4,5,6, 10,11],
}

PLAYER = { R:-1, C:-1}  # row colm pair

import signal
import sys

def printboard():
    if not DEBUG:
        return
    for r in range(ROWS):
        for c in range(COLS):
            icon = BOARD[r][c]
            if PLAYER[R] == r and PLAYER[C] == c:
                icon = FROG
            print('{: ^5}'.format(icon), end=' ')
        print()
    print()

def update_board():
    for r in range(ROWS):
        for c in range(COLS):
            if r in ROAD_ROWS:
                BOARD[r][c] = ROAD
                if c in ROAD_ROWS[r]:
                    BOARD[r][c] = CAR
            if r in RIVER_ROWS:
                BOARD[r][c] = WATER
                if c in RIVER_ROWS[r]:
                    BOARD[r][c] = LOG
            if r == VICTORY_ROW:
                BOARD[r][c]

def setup():
    PLAYER[R] = ROWS-1
    PLAYER[C] = COLS // 2

    # Hardcoded car to the nw of the start, but not n or ne, or w of the nw car
    ROAD_ROWS[12] = [COLS//2 - 1] + list(random.sample(list(set(range(COLS)) - set([COLS//2 - 2, COLS//2, COLS//2 + 1])), 3))
    ROAD_ROWS[10] = list(random.sample(range(COLS), 4))
    ROAD_ROWS[9]  = list(random.sample(range(COLS), 4))

    update_board()
    printboard()

def move_npcs():
    for r in ROAD_ROWS:
        ROAD_ROWS[r] = [c+1 if c+1 < COLS else 0 for c in ROAD_ROWS[r]]
        # randomly kill cars over time to prevent stuck game states
        if random.randint(0,100) < 5:  # 5% chance:
            try:
                ROAD_ROWS[r].pop()
            except:
                pass  # there is no cars left to pop
    for r in RIVER_ROWS:
        if PLAYER[R] == r:
            PLAYER[C] = PLAYER[C]+1 if PLAYER[C]+1 < COLS else 0  # move the player on the log
        RIVER_ROWS[r] = [c+1 if c+1 < COLS else 0 for c in RIVER_ROWS[r]]
    update_board()

def check_death():
    if PLAYER[R] in ROAD_ROWS:
        if PLAYER[C] in ROAD_ROWS[PLAYER[R]]:
            return True, CAR_ACCIDENT
    if PLAYER[R] in RIVER_ROWS:
        if not PLAYER[C] in RIVER_ROWS[PLAYER[R]]:
            return True, DROWNDED
    if PLAYER[R] >= ROWS:
        return True, FELL_OFF_MAP
    return False, None

def win_routine():
    print('Congrats, you reached the Christmas tree with all the presents!')
    print('You have {} seconds to claim your reward before the Grinch steals it and clears your screen!'.format(RIDDLE_TIMER))
    start_time = int(time.time())
    team_num = None
    while team_num == None:
        inp = input('Enter your team number to open your next riddle: ')
        try: 
            team_num = int(inp)
            riddle = TEAM_NEXT_RIDDLE[team_num]
        except:
            print('Not a valid team number.')
    curr_time = int(time.time())
    if curr_time - start_time >= RIDDLE_TIMER:
        return True, RIDDLE_EXPIRED
    print()
    print(LOCATION_GET_HERE_RIDDLE[TEAM_NEXT_RIDDLE[team_num]])
    time_left = RIDDLE_TIMER - (curr_time - start_time)
    time.sleep(time_left)
    os.system('clear')

def perception_check():
    # assuming there is always a row above the player (oversized board)
    next_row_i = PLAYER[R] - 1
    relavent_colms = {
        LEFT:  PLAYER[C]-1 if PLAYER[C]-1 >= 0 else COLS-1,  # left, or loop around 
        MID:   PLAYER[C], 
        RIGHT: PLAYER[C]+1 if PLAYER[C]+1 < COLS else 0      # right, or loop around
    }

    # you are on a road
    if PLAYER[R] in ROAD_ROWS and relavent_colms[LEFT] in ROAD_ROWS[PLAYER[R]]:
        print('You hear a "BEEEEEP!" and the squealing of brakes to the west.')

    # you are on a log
    if PLAYER[R] in RIVER_ROWS and PLAYER[C] in RIVER_ROWS[PLAYER[R]]:
        river_row = RIVER_ROWS[PLAYER[R]]
        print('You are on a wobbling log drifiting through the river.')
        if relavent_colms[LEFT] in river_row or relavent_colms[RIGHT] in river_row:
            log_extend_str='It feels like this log extends to the '
            if relavent_colms[LEFT] in river_row:
                log_extend_str += 'west and '
            if relavent_colms[RIGHT] in river_row:
                log_extend_str += 'east and '
            log_extend_str = log_extend_str[:-len(' and ')] + '.'
            print(log_extend_str)
    
    # is it a road or a field of grass in the north?
    if next_row_i in ROAD_ROWS:
        road_row = ROAD_ROWS[next_row_i]
        if len(road_row) == 0:  # this is a fake road
            print('You smell the crisp air of an open field to the north.')
        else:
            has_car = False
            if relavent_colms[LEFT] in road_row:
                print('You hear a car approaching in the northwest.')
                has_car = True
            if relavent_colms[MID] in road_row:
                print('You hear the roar of a car driving near you in the north, heading eastbound.')
                has_car = True
            if relavent_colms[RIGHT] in road_row:
                print('You smell the exhaust of a car driving away in the northeast.')
                has_car = True
            if not has_car:
                print('It is strangely quiet to the north.')
    
    if next_row_i in RIVER_ROWS:
        river_row = RIVER_ROWS[next_row_i]
        has_log = False
        if relavent_colms[LEFT] in river_row:
            print('You hear something approaching in the river from the northwest.')
            has_log = True
        if relavent_colms[MID] in river_row:
            print('A log soaks you in water as it fights the river in the north.')
            has_log = True
        if relavent_colms[RIGHT] in river_row:
            print('The sounds of a log splashing in the water become faiter and fainter in the northeast.')
            has_log = True
        if not has_log:
            print('A river hums quietly in the north.')

def move():  # ret is_dead, reason
    m = input('\nWhat is your move? Valid moves: {}\n'.format(VALID_MOVES)).lower()
    while m not in VALID_MOVES:
        print('You can not "{}" here'.format(m))
        m = input('\nWhat is your move? Valid moves: {}\n'.format(VALID_MOVES))
        
    # Move your character
    # Vertical moves
    if m in ['n', 'ne', 'nw']:
        PLAYER[R] = PLAYER[R] - 1
    if m in ['s', 'se', 'sw']:
        PLAYER[R] = PLAYER[R] + 1
    
    # Horizontal moves, wrap around
    if m in ['e', 'ne', 'se']:
        PLAYER[C] = PLAYER[C]+1 if PLAYER[C]+1 < COLS else 0
    if m in ['w', 'nw', 'sw']:
        PLAYER[C] = PLAYER[C]-1 if PLAYER[C]-1 >= 0 else COLS-1

    # No moves
    if m in ['croak', 'c']:
        print('You (c)roak very loudly (and do not move).')

    # Check if you are dead
    is_dead, death_reason = check_death()
    if is_dead:
        return is_dead, death_reason
    
    # Did you win?!?!
    if PLAYER[R] == VICTORY_ROW:
        win_routine()
        return True, RIDDLE_EXPIRED 

    # Now, move everything else
    move_npcs()
    printboard()

    # Check again if you did not get deaded
    is_dead, death_reason = check_death()
    if is_dead:
        return is_dead, death_reason

    # What do I see around me?
    perception_check()
    
    return False, None

def intro():
    print('WELCOME TO FROGGER!')
    print()
    print('You are a frog trying to hop over to the chrismas presents under the tree!')
    print('However, there are vehicle-infested roads and trecherous rivers that need to be crossed in the north.')
    print('Note: you are very fast and move before anything else in this world.')
    print('You put on your trusty Santa hat to brave the world ahead.')
    print('However, the hat is too large and covers your eyes, making it harder to see..')
    print()
    input('Press enter to continue.')
    if not DEBUG: os.system('clear')


def story():
    while 1:
        if not DEBUG: os.system('clear')
        intro()
        setup()
        perception_check()
        is_dead = False
        while not is_dead:
            is_dead, death_reason = move()
        print('\n' + death_reason)
        input('Press enter to try again..')



if __name__ == '__main__':
    story()
