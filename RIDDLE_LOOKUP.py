
# TODO edit this TEAM_NEXT_RIDDLE dict based on your location
TEAM_NEXT_RIDDLE={   # { team_lowercase : next_riddle_location }  # next_riddle_location must match the key in LOCATION_GET_HERE_RIDDLE
    "jack": "TODO", 
    "sally": "TODO",
    "zero": "TODO",
    "claws": "TODO",
    "oogie": "TODO",
    "mayor": "TODO",
    "triplets": "TODO",
    "finkelstein": "TODO",
    "reaper": "TODO",
    "harlequin": "TODO", 
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


team = input("Enter team").lower().strip()
riddle = LOCATION_GET_HERE_RIDDLE[TEAM_NEXT_RIDDLE[team]]
print(riddle)
