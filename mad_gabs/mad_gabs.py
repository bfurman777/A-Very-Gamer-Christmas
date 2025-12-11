import pyaudio
import wave
import os
import whisper
import time
import signal
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")
# Test
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
        'serverus snape'        :   'K',
        'minerva mcgonagall'    :   'Z',
        'ron weasley'           :   'Q',
        'harry potter'          :   'S',
        'luna lovegood'         :   'P',
        'albus dumbeldore'      :   'Z',
        'draco malfoy'          :   'G',
        'rubeus hagrid'         :   'Z',
        'lord voldemort'        :   'O',
        'hermoine granger'      :   'L'
    }

clues = \
    {
    "G" : """
    Beside the lake where ripples gleam
    A Word Game awaits with quiz like scheme
    Asnwer true, let wit prevail
    Earn House points by the water's trail""",

    "R" : """
    I solemnly swear I'm up to no good
    Find where vistors once stood
    Footprints flicker, secrets gleam
    Your map reveals the hidden scheme""",

    "O" : """
    Run through the halls of stone
    Past floating candles and the portrait's drone
    At the bathroom wall, where the next clue sprawls
    And answer another teams' calls""",

    "K" : """
    Near the lot wehre muggles queue
    Your next station awaits you
    On the wall you will find
    A new puzzle to trick your mind""",

    "P" : """
    In Diagon Alley On a street next to a valley
    Catch the snitch, avoid misery,
    And claim your path to victory""",

    "Z" : """
    In the room with magic supplies
    You'll find an intersting suprise
    A wizard guide with secrets to tell
    Find the ingredients and mix them well""",

    "Q" : """
    Where potions brew and chatter blend
    Your final spell is near the end
    Rest your wand, the quest is done
    Hour Points earned, well fought and won
    Return to wehre it had begun.
    
    Hippogriff""",

    "I" : """
    Where muggles speed when lights are green
    You will find a laptop screen
    A leap of faith, your spells begun
    Start your trial at level one""",

    "L" : """
    Like Hogwarts halls with portraits grand
    It draws your attention with great demand
    In corridors wehre cloaks might sway
    Your next clue is near the bay""",

    "S" : """
    Your house transforms as full moons rise
    Metallic charms will test the wise
    Try not to lose your way
    As boxes stage the next game you play""",

    "A" : """
    From states that start with W and M,
    You find phrases in a magical den.
    Guess the meaning of the wizard's spell
    New secrets it will tell"""
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
    # model = whisper.load_model("base")  # You can use "small", "medium", "large" based on your need
    model = whisper.load_model("medium")  # You can use "small", "medium", "large" based on your need

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
        # rate=44100
        rate = 16000
        # rate = 20000
        # Start recording (e.g., record for 10 seconds)
        recorded_file = record_audio(mad_gab, file_name, duration=10, rate=rate)
        
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