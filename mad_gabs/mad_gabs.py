import pyaudio
import wave
import os
import whisper
import time
import signal
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")

WELCOME_STRING = """
Welcome to LGS Mad Gab! Brought to you by IRAD and Artificial Intelligence!


Mad Gab is a word game where teams race to translate groups of words into phrases before time runs out:

    How to play:
    Teams work together to sound out puzzles.
    The puzzles are called mondegreens, and are made up of small words that sound like a word or phrase when said quickly.
    For example, "These If Hill Wore" sounds like "The Civil War".
    The game tests the brain's ability to process sounds into meaningful words and phrases.

    Solve the mondegreen to get your next clue!
"""

teams_next_station = \
    {
        'jack'          :   'Q',
        'sally'         :   'S',
        'zero'          :   'I',
        'claws'         :   'P',
        'oogie'         :   'E',
        'mayor'         :   'P',
        'triplets'      :   'G',
        'finkelstein'   :   'L',
        'reaper'        :   'E',
        'harlequin'     :   'I'
    }

clues = \
    {
    "I" : """
    Looking in from the street 
    You'll see something pretty neat 
    Laptops causing feelings of glee 
    As teams make connections easily""",

    "G" : """
    Look up from your screen 
    Upon a lake so pristine
    But watch your steps in this area 
    There are mines that can scare 'ya""",

    "L" : """
    Look upon this work of art 
    On the wall is where to start
    Supposedly in view of a lake 
    You'll find this claim a bit fake""",

    "S" : """
    The bathrooms here are barely functional 
    Easy there, try not to get too emotional. 
    Solve this puzzle if you dare!
    You should brush up on your Viginere.""",

    "A" : """
    In Montana and Wyoming you might find 
    Something that will blow your mind 
    Say the words, like a magic spell 
    And make sure to pronounce them well.""",

    "E" : """
    It may be a surprise
    When, among the supplies,
    You find a wheel you can turn.
    It's not wheel of fortune;
    Money, you won't earn.
    But spin this wheel, and see what you learn!""",

    "R" : """
    Look for the post of a vigilant sentry 
    Near the place that grants you entry 
    And there upon the TV screen 
    A familiar map will be seen""",

    "O" : """
    In the place where you see the park,
    Come and find our mark 
    AND with these ORdinary gates
    Solve the puzzle to determine your fates""",

    "K" : """
    An animal with horns upon its head 
    Would choose this pen to make its bed 
    Full of papers you can fold
    To reveal secrets yet untold""",

    "P" : """
    At this point you know the drill 
    Head to LJ's _______ and Grill
    One teammate will be blind
    With help, the answers they will find""",

    "Q" : """
    It's time that we departed
    Come back to where you started
    Enter the letters from each station 
    To begin your celebration""",

    "F" : "lmaooooooo"

    }

mad_gabs = \
    [
       ("CHEX KNOTS ROAD STING GONE HAND OLD PEN FIGHTER", "Chestnuts Roasting on an Open Fire"),
       ("ACRE WRIST MASK CARE OLD", "A Christmas Carol"),
       ("TWO ELF DATES SOFT GRITS MIST", "Days of Christmas"),
       ("SAND TOTS WORD CHOP", "Santa's Workshop"),
       ("JEAN GLOW WALL THOUGH WAIT", "Jingle All the Way"),
       ("FROGS TEETH THUS NOTE MEND", "Frosty the Snowman"),
       ("A BOMB IN A BULLS NODE MINT", "Abominable Snowman"),
       ("THIN I'D BEEF FORK WRIST MISS", "The Night Before Christmas"),
       ("THIN HUT CAR RACK HER", "The Nutcracker"),
       ("THUG WREN CHEWS TOLL CRISP MISS", "The Grinch Who Stole Christmas")
    ]

team_mad_gabs = { name : mad_gabs[i] for i, name in enumerate(teams_next_station)}

SCREEN_TIME_OUT = 60

def get_mad_gab(team_name):
    if team_name not in team_mad_gabs:
        print(f"Critical Error! Team {team_name} not in dictionary!!")
        return None
    return team_mad_gabs[team_name]

# Function to record audio
def record_audio(mad_gab, filename, duration=10, rate=44100, channels=2, chunk_size=1024):
    # Set up the audio stream
    p = pyaudio.PyAudio()

    print(f"{WELCOME_STRING}\n\nCan you say... \n\n{mad_gab[0]}\n")
    print('Press Enter to start recording!\n')
    input()
    print('\nStarting recording in...')
    for i in range(3):
        print(3 - i)
        time.sleep(1)

    # Open a stream to record audio from the microphone
    stream = p.open(format=pyaudio.paInt16, 
                    channels=channels, 
                    rate=rate, 
                    input=True, 
                    frames_per_buffer=chunk_size)

    print("\nSTART SPEAKING!!!\nStarting Countdown...")

    # Initialize an empty list to store frames of audio
    frames = []

    # Record audio for the specified duration
    countdown = 10
    for i in range(0, int(rate / chunk_size * duration)):
        if i % 42 == 0:
            print(countdown)
            countdown -= 1
        data = stream.read(chunk_size)
        frames.append(data)

    # Stop the stream
    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio as a .wav file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved as {filename}")
    
    return filename

# Function to transcribe audio using Whisper
def transcribe_audio(filename):
    # Load the Whisper model (this will automatically download it if not present)
    model = whisper.load_model("base")  # You can use "small", "medium", "large" based on your need

    print("\nBeep Boop Beep... I'm learning your language... Human... \n(Turning voice to text...)\n")
    # Transcribe the audio file
    result = model.transcribe(filename)
    
    # Return the transcription text
    return result['text']

def main_game_loop(team_name):
    next_stage = teams_next_station[team_name]
    if next_stage not in clues:
        print("Critical Error! No Next Clue found!!!")
        return

    # Define the file path for saving the recording
    file_name = f"{team_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    
    # Check if the file already exists and prompt for a new name if needed
    if os.path.exists(file_name):
        print(f"File '{file_name}' already exists. Please specify a new file name.")

    else:
        mad_gab = get_mad_gab(team_name=team_name)
        # Start recording (e.g., record for 10 seconds)
        recorded_file = record_audio(mad_gab, file_name, duration=10)
        
        # Transcribe the recorded audio using Whisper
        transcription = transcribe_audio(recorded_file)
        print("\nDid you say?:\n")
        print(transcription)
        if mad_gab[1].lower() in transcription.lower():
            print(f"\nTHAT'S RIGHT!!!\nI heard you loud and clear!\nHere's your next clue....\n\n{clues[next_stage]}\n\n")
            print(f'clearing the screen in {SCREEN_TIME_OUT} seconds...')
            print('CTRL+c to start a new game')

            time.sleep(SCREEN_TIME_OUT)
            os.system('clear')

            return
        print("No! No! No! You didn't say it right. You're not in the spirit! Try again...")

def verify_team_name():
    print('Enter your team name:')
    team_name = input()

    team_name = team_name.strip().lower()
    if team_name in teams_next_station:
        return team_name
    print('Team Name not recognized. Please try again!')
    return None

def game_driver():
    while(True):
        team_name = verify_team_name()
        while not team_name:
            team_name = verify_team_name()
        # Play the game!
        main_game_loop(team_name)

def main():
        game_driver()

# def restart_game_handler(signum, frame):
#     os.system('clear')
#     main()

# # catching signals
# signal.signal(signal.SIGINT, restart_game_handler)

# Main function to execute recording and transcription
if __name__ == "__main__":
    main()