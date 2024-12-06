#!/usr/bin/env python3

import random
import os
import time

RIDDLES='''
TEAM 1: THE RIDDLE IS A FIDDLE AND YOU ARE A LITTLE LOST
TEAM 2: THE RIDDLE IS A FIDDLE AND YOU ARE A LITTLE LOST
TEAM 3: THE RIDDLE IS A FIDDLE AND YOU ARE A LITTLE LOST
TEAM 4: THE RIDDLE IS A FIDDLE AND YOU ARE A LITTLE LOST
TEAM 5: THE RIDDLE IS A FIDDLE AND YOU ARE A LITTLE LOST
TEAM 6: THE RIDDLE IS A FIDDLE AND YOU ARE A LITTLE LOST
TEAM 7: THE RIDDLE IS A FIDDLE AND YOU ARE A LITTLE LOST
TEAM 8: THE RIDDLE IS A FIDDLE AND YOU ARE A LITTLE LOST
TEAM 9: THE RIDDLE IS A FIDDLE AND YOU ARE A LITTLE LOST
TEAM 10: THE RIDDLE IS A FIDDLE AND YOU ARE A LITTLE LOST
TEAM 11: THE RIDDLE IS A FIDDLE AND YOU ARE A LITTLE LOST
TEAM 12: THE RIDDLE IS A FIDDLE AND YOU ARE A LITTLE LOST
'''

TOTAL_SHOTS = 70
DEFAULT = "    "
HIT = "👿👿"
MISS = " () "

def PvC():
    os.system('clear')

    player_ship_coordinates = []
    computer_ship_coordinate = [] # computer_ship_coordinates
    field_coordinates = [" " for i in range(100)]
    coordinate_value = {"A":0, "B":10, "C":20, "D":30, "E":40, "F":50, "G":60, "H":70, "I":80, "J":90}

    player_shot = 0
    computer_shot = 0

    prev_coordinates = [] # for 'undo'

    def char_range(c1, c2):
        for c in range(ord(c1), ord(c2)):
            yield chr(c)

    def field(shots_fired, shots_left):
        return ("""
      We have used {}/{} shots to fend off the invading Krampus army!
                               Enemy ship totals: 1x len4, 5x len3

         0    1    2    3    4    5    6    7    8    9
       ---------------------------------------------------
    A  |{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|
       ---------------------------------------------------
    B  |{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|
       ---------------------------------------------------
    C  |{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|
       ---------------------------------------------------
    D  |{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|
       ---------------------------------------------------
    E  |{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|
       ---------------------------------------------------
    F  |{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|
       ---------------------------------------------------
    G  |{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|
       ---------------------------------------------------
    H  |{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|
       ---------------------------------------------------
    I  |{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|
       ---------------------------------------------------
    J  |{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|
       ---------------------------------------------------
        """.format(shots_fired, shots_left, *field_coordinates))

    def ai_start(csc):
        # 4 block length ship x 1
        for i in range(1):
            direction = random.choice(["h", "v"])

            if direction == "h":
                # selectable coordinates for 4 block length ship (horizontal)
                selectable_coordinates = []
                for char in char_range("A", "K"):
                    for j in range(0, 7):
                        selectable_coordinates.append(char+str(j))
                ###

                start_coordinate = random.choice(selectable_coordinates)
                csc.append(start_coordinate)
                csc.append(start_coordinate[0]+str(int(start_coordinate[1])+1))
                csc.append(start_coordinate[0]+str(int(start_coordinate[1])+2))
                csc.append(start_coordinate[0]+str(int(start_coordinate[1])+3))

            if direction == "v":
                # selectable coordinates for 4 block length ship (vertical)
                selectable_coordinates = []
                for char in char_range("A", "H"):
                    for j in range(0, 10):
                        selectable_coordinates.append(char+str(j))
                ###

                start_coordinate = random.choice(selectable_coordinates)
                csc.append(start_coordinate)
                csc.append(chr(ord(start_coordinate[0])+1)+start_coordinate[1])
                csc.append(chr(ord(start_coordinate[0])+2)+start_coordinate[1])
                csc.append(chr(ord(start_coordinate[0])+3)+start_coordinate[1])
        ###

        # 3 block length ship x 5
        for i in range(5):
            direction = random.choice(["h", "v"])

            if direction == "h":
                # selectable coordinates for 3 block length ship (horizontal)
                selectable_coordinates = []
                for char in char_range("A", "K"):
                    for j in range(0, 8):
                        selectable_coordinates.append(char+str(j))

                for coo in csc:
                    try:
                        selectable_coordinates.remove(coo)
                    except:
                        continue
                ###

                while True:
                    start_coordinate = random.choice(selectable_coordinates)
                    c0 = start_coordinate # coordinate0
                    c1 = start_coordinate[0]+str(int(start_coordinate[1])+1) # coordinate1
                    c2 = start_coordinate[0]+str(int(start_coordinate[1])+2) # coordinate2

                    if (c1 in csc) or (c2 in csc):
                        continue

                    else:
                        csc.append(c0)
                        csc.append(c1)
                        csc.append(c2)
                        break

            if direction == "v":
                # selectable coordinates for 3 block length ship (vertical)
                selectable_coordinates = []
                for char in char_range("A", "I"):
                    for j in range(0, 10):
                        selectable_coordinates.append(char+str(j))

                for coo in csc:
                    try:
                        selectable_coordinates.remove(coo)
                    except:
                        continue
                ###

                while True:
                    start_coordinate = random.choice(selectable_coordinates)
                    c0 = start_coordinate # coordinate0
                    c1 = chr(ord(start_coordinate[0])+1)+start_coordinate[1] # coordinate1
                    c2 = chr(ord(start_coordinate[0])+2)+start_coordinate[1] # coordinate2

                    if (c1 in csc) or (c2 in csc):
                        continue

                    else:
                        csc.append(c0)
                        csc.append(c1)
                        csc.append(c2)
                        break

        ###

        # # 2 block length ship x 3
        # for i in range(3):
        #     direction = random.choice(["h", "v"])

        #     if direction == "h":
        #         # selectable coordinates for 2 block length ship (horizontal)
        #         selectable_coordinates = []
        #         for char in char_range("A", "K"):
        #             for j in range(0, 9):
        #                 selectable_coordinates.append(char+str(j))

        #         for coo in csc:
        #             try:
        #                 selectable_coordinates.remove(coo)
        #             except:
        #                 continue
        #         ###

        #         while True:
        #             start_coordinate = random.choice(selectable_coordinates)
        #             c0 = start_coordinate
        #             c1 = start_coordinate[0]+str(int(start_coordinate[1])+1)

        #             if (c1 in csc):
        #                 continue

        #             else:
        #                 csc.append(c0)
        #                 csc.append(c1)
        #                 break

        #     if direction == "v":
        #         # selectable coordinates for 2 block length ship (vertical)
        #         selectable_coordinates = []
        #         for char in char_range("A", "J"):
        #             for j in range(0, 10):
        #                 selectable_coordinates.append(char+str(j))

        #         for coo in csc:
        #             try:
        #                 selectable_coordinates.remove(coo)
        #             except:
        #                 continue
        #         ###

        #         while True:
        #             start_coordinate = random.choice(selectable_coordinates)
        #             c0 = start_coordinate
        #             c1 = chr(ord(start_coordinate[0])+1)+start_coordinate[1]

        #             if (c1 in csc):
        #                 continue

        #             else:
        #                 csc.append(c0)
        #                 csc.append(c1)
        #                 break
        # ###

        # # 1 block length ship x 4
        # for i in range(4):
        #     # selectable coordinates for 1 block length ship
        #     selectable_coordinates = []
        #     for char in char_range("A", "K"):
        #         for j in range(0, 10):
        #             selectable_coordinates.append(char+str(j))

        #     for coo in csc:
        #         try:
        #             selectable_coordinates.remove(coo)
        #         except:
        #             continue
        #     ###

        #     start_coordinate = random.choice(selectable_coordinates)
        #     csc.append(start_coordinate)
        # ###

    ai_start(computer_ship_coordinate)

    field_coordinates = [DEFAULT for i in range(100)] # clear field

    selectable_coordinates = []
    print('Krampus is invading! We need your missile-guiding expertise!')
    print('However, we have a limited supply of bombs for shooting down their battleships. Be conservitive with ammo!')
    print('Radar reports:')
    print('  4 block length ship x 1')
    print('  3 block length ship x 5')
    print('Press enter to start this task, if you choose to accept it.')
    input('-Santa')
    os.system('clear')

    shots_fired = 0
    total_shots = TOTAL_SHOTS

    while shots_fired < total_shots:
        print(field(shots_fired, total_shots))
        coordinate = input("Coordinate: ").upper()
        os.system('clear')

        if (len(coordinate) < 2) or (len(coordinate) > 2) or (coordinate[0] not in "ABCDEFGHIJ") or (coordinate[1] not in "1234567890"):
            print("Please enter a letter between A-J first and then enter a number between 0-9. Sample: D6")
            continue

        if field_coordinates[coordinate_value[coordinate[0]]+int(coordinate[1])] != DEFAULT:
            print("You already shot it!")
            continue

        shots_fired += 1

        if coordinate in computer_ship_coordinate:
            char = HIT
            player_shot += 1
        else:
            char = MISS

        field_coordinates[coordinate_value[coordinate[0]]+int(coordinate[1])] = char

        if player_shot == 19:
            os.system('clear')
            print(field(shots_fired, total_shots))
            print("Santa is very thankful for your help!")
            print("Find your next station with the clues below:")
            print("Riddle will self-destruct in 60 seconds.")
            print(RIDDLES)
            time.sleep(60)
            PvC()
            exit()

    print('MISSION FAILED')
    time.sleep(1)
    PvC()


if __name__ == "__main__":
    PvC()

