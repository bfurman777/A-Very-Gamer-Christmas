import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import signal
import argparse
import logging
import matplotlib.pyplot as plt
import pandas
from PIL import Image, ImageTk

logger = logging.getLogger(__name__)
logging.basicConfig(
        #filename='analyze.log', 
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%H:%M:%S'
    )
player_cb= None

DATAFILE = 'data.csv'
IMAGE_PATH = "Graphs.png" 
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
END = "\033[0m"

ForColor = {
        "Default":'\033[0;39m',
        "Black" :'\033[0;30m',
        "DarkRed" :'\033[0;31m',
        "DarkGreen" :'\033[0;32m',
        "DarkYellow" :'\033[0;33m',
        "DarkBlue" :'\033[0;34m',
        "DarkMagenta" :'\033[0;35m',
        "DarkCyan" :'\033[0;36m',
        "Gray" :'\033[0;37m',
        "DarkGray" :'\033[1;90m',
        "Red" :'\033[1;91m',
        "Green" :'\033[1;92m',
        "Yellow" :'\033[1;93m',
        "Blue" :'\033[1;94m',
        "Magenta" :'\033[1;95m',
        "Cyan" :'\033[1;96m',
        "White" :'\033[1;97m'
}

BackgColor = {
    "Red" :"\033[0;41m",
    "Green" :"\033[0;42m",
    "Yellow" :"\033[0;43m",
    "Blue" :"\033[0;44m",
    "Magenta" :"\033[0;45m",
    "Cyan" :"\033[0;46m",
    "Gray" :"\033[0;7m",
}

def my_signal_handler(signum, frame):
    print(f"\nCaught signal {signum}!")
    # You can add custom cleanup or exit logic here
    exit(0)  # Exit gracefully
signal.signal(signal.SIGINT, my_signal_handler)
        
class Player():
    def __init__(self, name):
        self.name = name
        self.History = [] # 'date', 'opponent', 'score', 'score_opponent','elo_diff', 'elo_diff_opponent'
        # history has a dict of day, month, opponent, score, opponent score, elo diff, opponent elo diff
        self.elo = 1500
        self.wins = 0
        self.losses = 0

    def print_history(self):
        for h in self.History:
            result = GREEN + 'WON' + END
            if h["score"] < h["score_opponent"]:
                result = RED + 'LOST' + END
            print("{}: played {} and {} ({}-{}). Elo diff: {} Opponent Elo diff: {}".format(h["date"], h["opponent"], result, h["score"], h["score_opponent"], int(h["elo_diff"]), int(h["elo_diff_opponent"])))

    def graph_elo( self ):
        '''
        go over history and graph elo over time
        '''
        dates = {}
        for h in self.History:
            if h['date'] in dates:
                dates[h['date']] += h['elo_diff']
            else:
                dates[h['date']] = h['elo_diff']

        #fin = pandas.DataFrame({'date':['05-12-2024'],'elo':[1500]})
        fin = pandas.DataFrame(columns=['date','elo'])
        elo = 1500
        first = True
        for k,v in dates.items():
            elo += v
            split = k.split('/')
            #print(split)
            if first:
                nd = "{:02}-{:02}-2024".format(int(split[0]), int(split[1]) - 1)
                fin = pandas.concat([fin,pandas.DataFrame({'date':[nd],'elo':[1500]})])
                first = False

            nd = "{:02}-{:02}-2024".format(int(split[0]), int(split[1]))
            fin = pandas.concat([fin,pandas.DataFrame({'date':[nd],'elo':[elo]})])
        # add last date
        ldate = "{:02}-{:02}-2024".format(7, 20)
        fin = pandas.concat([fin,pandas.DataFrame({'date':[ldate],'elo':[elo]})])
        fin['date'] = pandas.to_datetime(fin['date'], format="%m-%d-%Y")
        fin.set_index(fin['date'],inplace=True)
        logger.debug(fin)
        fin['elo'].plot(title='ELO graph').legend([self.name],loc='right')
        #plt.plot(fin['date'],fin['elo'])#,title="DataFrame Plot")

        plt.savefig(self.name)

def expected(A, B):
    """
    Calculate expected score of A in a match against B

    :param A: Elo rating for player A
    :param B: Elo rating for player B
    """
    return 1 / (1 + 10 ** ((B - A) / 400))


def elo(old, exp, score, k=20):
    """
    Calculate the new Elo rating for a player

    :param old: The previous Elo rating
    :param exp: The expected score for this match
    :param score: The actual score for this match
    :param k: The k-factor for Elo (default: 32)
    """

    logger.debug(f"old {old} new {old + k * (score - exp)} exp {exp} score {score} k {k} ")

    return old + k * (score - exp)

def calculateNew(p1,p2,s1,s2):
    '''
    return the difference of elos
    '''
    oldelo1 = p1.elo
    oldelo2 = p2.elo
    p1exp = expected(p1.elo, p2.elo)
    p2exp = expected(p2.elo, p1.elo)
    #logger.debug('expected score 1: {} score 2: {}'.format(p1exp, p2exp))
    logger.debug(f"p1 {p1.name} old elo {p1.elo} p2 {p2.name} old elo {p2.elo}")
    # BIG difference
    if abs(p1.elo - p2.elo) > 800:
        logger.debug('elo diff 800')
        if p1.elo > p2.elo:
            # expected win
            if s1 - s2 > 0:
                p1.elo = p1.elo
                p2.elo = p2.elo
            # underdog win
            else:
                p1.elo = elo(p1.elo, p1exp, (s1 - s2),80)
                p2.elo = elo(p2.elo, p2exp, (s2 - s1),80)
        else:
            # expected win
            if s1 - s2 < 0:
                p1.elo = p1.elo
                p2.elo = p2.elo
            # underdog win
            else:
                p1.elo = elo(p1.elo, p1exp, (s1 - s2),80)
                p2.elo = elo(p2.elo, p2exp, (s2 - s1),80)
    # decent differnce
    elif abs(p1.elo - p2.elo )> 400:
        logger.debug('elo diff 400')
        if p1.elo > p2.elo:
            # expected win
            if s1 - s2 > 0:
                p1.elo = elo(p1.elo, p1exp, (s1 - s2),10)
                p2.elo = elo(p2.elo, p2exp, (s2 - s1),10)
            # underdog win
            else:
                p1.elo = elo(p1.elo, p1exp, (s1 - s2),40)
                p2.elo = elo(p2.elo, p2exp, (s2 - s1),40)
        else:
            # expected win
            if s1 - s2 < 0:
                p1.elo = elo(p1.elo, p1exp, (s1 - s2),10)
                p2.elo = elo(p2.elo, p2exp, (s2 - s1),10)
            # underdog win
            else:
                p1.elo = elo(p1.elo, p1exp, (s1 - s2),40)
                p2.elo = elo(p2.elo, p2exp, (s2 - s1),40)

    # normal difference
    else:
        p1.elo = elo(p1.elo, p1exp, (s1 - s2))
        p2.elo = elo(p2.elo, p2exp, (s2 - s1))
    logger.debug('new elos: {} - {} {} - {}\n'.format(p1.name, p1.elo, p2.name, p2.elo))
    return p1.elo - oldelo1, p2.elo - oldelo2

def graph_players(players):
        '''
        go over history and graph elo over time for a list of players
        '''
        # first build the datraframe
        fin = pandas.DataFrame(columns=['date','elo','name'])
        for player in players:
            dates = {}
            for h in player.History:
                if h['date'] in dates:
                    dates[h['date']] += h['elo_diff']
                else:
                    dates[h['date']] = h['elo_diff']

            #fin = pandas.DataFrame({'date':['05-12-2024'],'elo':[1500]})
            
            elo = 1500
            first = True
            for k,v in dates.items():
                elo += v
                split = k.split('/')
                #print(split)
                if first:
                    nd = "{:02}-{:02}-2024".format(int(split[0]), int(split[1]) - 1)
                    fin = pandas.concat([fin,pandas.DataFrame({'date':[nd],'elo':[1500],'name':player.name})])
                    first = False

                nd = "{:02}-{:02}-2024".format(int(split[0]), int(split[1]))
                fin = pandas.concat([fin,pandas.DataFrame({'date':[nd],'elo':[elo],'name':player.name})])
            # add last date
            ldate = "{:02}-{:02}-2024".format(7, 20)
            fin = pandas.concat([fin,pandas.DataFrame({'date':[ldate],'elo':[elo],'name':player.name})])
        
        # final plot
        fin['date'] = pandas.to_datetime(fin['date'], format="%m-%d-%Y")
        fin.set_index(fin['date'],inplace=True)
        logger.debug(fin)
        for group in fin.groupby('name'):
            group[1]['elo'].plot(title='ELO graph', label=group[0]).legend(bbox_to_anchor=(1,1))

        logger.debug(fin)
        fin = None
        plt.savefig("Graphs", bbox_inches='tight') # Ilie,Matt H,Chris H,Jesse,Kevin H
        plt.clf()
        plt.close()

#################################### GUI code ####################################

def only_allow_integers(new_value):
    # Allow empty string (for deletion), or if it's a valid integer
    if new_value.isdigit():  # Check if the input is a digit
        value = int(new_value)
        if value <= 100:  # Set your maximum value here
            return True
        else:
            return False
    elif new_value == "":  # Allow clearing the entry
        return True
    else:
        return False

def only_letters_spaces_max64(new_value):
    # Allow empty input (for deletion)
    if new_value == "":
        return True
    # Enforce max length
    if len(new_value) > 64:
        return False
    # Allow only letters and spaces
    return all(char.isalpha() or char.isspace() for char in new_value)

def open_new_game_window():
    def submit():
        # Collect inputs from the text boxes and date selector
        inputs = {
            "Player 1": entry1.get(),
            "Score 1": entry2.get(),
            "Player 2": entry3.get(),
            "Score 2": entry4.get(),
            "Date": f'{month_cb.get()}/{day_cb.get()}/{year_cb.get()}'
        }
        valid = True
        try:
            s1 = int(inputs["Score 1"])
            s2 = int(inputs["Score 2"])
            if len(inputs["Player 1"]) == 0 or len(inputs["Player 2"]) == 0:
                messagebox.showinfo('Warning','Please enter some Names for the Players')
                valid = False
            if inputs["Player 1"] == inputs["Player 2"]:
                messagebox.showinfo('Warning','Please enter different Names for the Players')
                valid = False
        except:
            messagebox.showinfo('Warning','Please enter some Numbers for Scores')
            valid = False
        if valid:
            messagebox.showinfo('Message',"New game added!") 
            with open(DATAFILE,'a') as ftowrite:
                ftowrite.write(f'{inputs["Date"]},{inputs["Player 1"]},{inputs["Player 2"]},{inputs["Score 1"]},{inputs["Score 2"]}\n')        
            popup.destroy() 
            update_table_data()
            
    popup = tk.Toplevel(root)
    popup.resizable(False, False)
    popup.title("Input Form")

    # Create labels and text boxes
    labels_text = [["Player 1:", "Score 1:"], ["Player 2:", "Score 2:"]]
    entries = []

    # Register the validation function with Tkinter
    vcmd = (popup.register(only_allow_integers), '%P')
    vcmd2 = (popup.register(only_letters_spaces_max64), '%P')

    for i, text in enumerate(labels_text):
        label = tk.Label(popup, text=text[0])
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
        
        entry = tk.Entry(popup, validate='key', validatecommand=vcmd2)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)
        
        label = tk.Label(popup, text=text[1])
        label.grid(row=i, column=2, padx=10, pady=5, sticky="e")
        
        entry = tk.Entry(popup, width=5, validate='key', validatecommand=vcmd)
        entry.grid(row=i, column=3, padx=10, pady=5)
        entries.append(entry)

    entry1, entry2, entry3, entry4 = entries  # Unpack entries for easier access

    # Create a Frame that spans 2 columns and 2 rows
    frame = tk.Frame(popup, bg="lightgray", borderwidth=2, relief="groove")
    frame.grid(row=4, column=0, rowspan=1, columnspan=6, sticky="nsew", padx=5, pady=5)

    # Get today's date
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    current_day = today.day

    # Ranges
    years = list(range(2000, current_year + 1))
    months = list(range(1, 13))
    days = list(range(1, 32))

    # Labels
    ttk.Label(frame, text="Year", width=5).grid(row=4, column=1, padx=10, pady=5)
    ttk.Label(frame, text="Month", width=5).grid(row=4, column=3, padx=10, pady=5)
    ttk.Label(frame, text="Day", width=5).grid(row=4, column=5, padx=10, pady=5)

    # Combo boxes with default values set to today's date
    year_cb = ttk.Combobox(frame, values=years, state="readonly", width=5)
    year_cb.set(current_year)
    year_cb.grid(row=4, column=0,padx=30)

    month_cb = ttk.Combobox(frame, values=months, state="readonly", width=5)
    month_cb.set(current_month)
    month_cb.grid(row=4, column=2)

    day_cb = ttk.Combobox(frame, values=days, state="readonly", width=5)
    day_cb.set(current_day)
    day_cb.grid(row=4, column=4)

    # Add a submit button
    submit_button = tk.Button(popup, text="Submit", command=submit)
    submit_button.grid(row=5, column=0, columnspan=6, pady=10)
    
#################################### Table code ####################################

def get_player_data(datafile):
    # get info on all players
    Players = {}
    fille = open(datafile,'r')
    for line in fille.readlines():
        data = line.replace('\n','').split(',')
        # print(data)
        if 'Date' in data[0] :
            continue
        tp1 = dict.get(Players,data[1],None)
        if tp1 == None:
            Players[data[1]] = Player(data[1])
        tp2 = dict.get(Players,data[2],None)
        if tp2 == None:
            Players[data[2]] = Player(data[2])

        d1, d2 = calculateNew(Players[data[1]],Players[data[2]],int(data[3]),int(data[4]))
        # add logic for score diff

        Players[data[1]].History.append(
            {'date':data[0],
            'opponent':data[2],
            'score':int(data[3]),
            'score_opponent':int(data[4]),
            'elo_diff':d1,
            'elo_diff_opponent':d2
            }
            )
        Players[data[2]].History.append(
            {'date':data[0],
            'opponent':data[1],
            'score':int(data[4]),
            'score_opponent':int(data[3]),
            'elo_diff':d2,
            'elo_diff_opponent':d1
            }
            )

        if int(data[3]) > int(data[4]):
            Players[data[1]].wins += 1
            Players[data[2]].losses += 1
        else:
            Players[data[2]].wins += 1
            Players[data[1]].losses += 1

    player_data = []
    #print("\nLeague of Let-Gends ELO (Summer 2024 Season)\n")
    sorte = sorted(Players, key=lambda x: Players[x].elo, reverse=True)
    for p in sorte:
        #print("Player: {:<10} elo :{:<4} ".format(p,int(Players[p].elo)),end='')
        #print('Wins: {:<2} Losses: {:<2} Games: {:<2} W/L: {:<4}'.format(Players[p].wins,Players[p].losses,len(Players[p].History), Players[p].wins/ len(Players[p].History) ) )
        player_data.append({"Player": p, "Elo": int(Players[p].elo), "Wins": Players[p].wins, "Losses": Players[p].losses, "Games": len(Players[p].History), "W/L": Players[p].wins/ len(Players[p].History)})    
    return player_data, Players

# example {"Player": "Alice", "Elo": 1200, "Wins": 10, "Losses": 2, "Games": 10, "W/L": 2}
player_data,_ = get_player_data(DATAFILE)

class SortableTable(ttk.Treeview):
    def __init__(self, parent, columns, **kwargs):
        super().__init__(parent, columns=columns, show='headings', **kwargs)
        self.columns_list = columns
        self.sort_reverse = {col: False for col in columns}

        for col in columns:
            self.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.column(col, anchor='center')

    def insert_data(self, data):
        # Clear current rows
        for row in self.get_children():
            self.delete(row)

        for row in data:
            values = [row[col] for col in self.columns_list]
            self.insert("", tk.END, values=values)

    def sort_by_column(self, col):
        data = [
            {self.columns_list[i]: self.item(child)["values"][i] for i in range(len(self.columns_list))}
            for child in self.get_children()
        ]
        is_numeric = all(self.is_number(row[col]) for row in data)
        data.sort(key=lambda x: float(x[col]) if is_numeric else str(x[col]), reverse=self.sort_reverse[col])
        self.sort_reverse[col] = not self.sort_reverse[col]
        self.insert_data(data)

    def is_number(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

# Function to simulate new data and update the table
def update_table_data():
    # Simulate data update (e.g., new scores/wins/losses)
    new_data,_ = get_player_data(DATAFILE)
    # Update table with new data
    table.insert_data(new_data)

############ graph #############

def open_image_window():
    _, Players = get_player_data(DATAFILE)
    sorte = sorted(Players, key=lambda x: Players[x].elo, reverse=True)
    finP = []
    real_count = 0
    count = int(player_start_cb.get()) - 1
    max_players = int(player_cb.get())
    for p in sorte:
        #print(f'rc {real_count} c {count} max {max_players}')
        if real_count < count:
            real_count += 1
            continue
        if len(finP) < max_players:
            finP.append( Players[p])
            #count += 1
        real_count += 1
    #print(count)
    #print(finP)
    graph_players(finP)
    try:
        # Load image using PIL
        img = Image.open(IMAGE_PATH)
        #img = img.resize((700, 600))  # Resize if needed
        tk_img = ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # Create new window
    popup2 = tk.Toplevel(root)
    popup2.title("Graph Viewer")

    # Keep a reference so it's not garbage collected
    popup2.image = tk_img

    # Display image
    label = tk.Label(popup2, image=tk_img)
    label.pack(padx=10, pady=10)
    
########################################################################################################################################################################

# args and debug setup
parser = argparse.ArgumentParser()
#parser.add_argument("--player", '-p', default=None, help="get history of individual player")
parser.add_argument("--debug", '-d', action="store_true", help="enable debug prints")
#parser.add_argument("--graph", '-g', action="store_true", help="graph elo")
args = parser.parse_args()

if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)

# if enabled give history of player
'''
if args.player:
    # check if it is 1 player or more
    players_str = args.player.split(',')
    for p_str in players_str:
        # logic for one player
        if p_str not in Players:
            print('player {} does not exist in our data'.format(p_str))
        else:
            tplay = p_str
            print('\nPlayer: {} Wins: {} Losses: {} Games: {}'.format(tplay,Players[tplay].wins,Players[tplay].losses,len(Players[tplay].History)))
            Players[tplay].print_history()
    if args.graph:
        logger.info("Graphing Players ELO\n")
        finP = []
        for p in players_str:
            finP.append( Players[p])
        graph_players(finP)

'''

# Main app window
root = tk.Tk()
root.title("Ping_Pong.exe")
root.geometry(f"1200x{len(player_data)*22+20}")

style = ttk.Style()
style.configure("Treeview", rowheight=20)

columns = ["Player", "Elo", "Wins", "Losses", "Games", "W/L"]
table = SortableTable(root, columns, height=len(player_data))

#table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
table.grid(row=0, column=0, padx=10, pady=5, rowspan=1, columnspan=6)
table.insert_data(player_data)

# Add "Update Data" button
#ttk.Button(root, text="Update Data", command=update_table_data).pack(pady=10)

#root.mainloop()

#root = tk.Tk()
#root.title("Ping_Pong.exe")
#root.geometry("300x150")

add_game_btn = ttk.Button(root, text="Add New Game", command=open_new_game_window)
#add_game_btn.pack(expand=True)
add_game_btn.grid(row=1, column=0, padx=10, pady=5)

# Combo
players_lst = list(range(1, len(player_data)))
ttk.Label(root, text="Start From:", width=10).grid(row=1, column=1, padx=10, pady=5)
player_start_cb = ttk.Combobox(root, values=players_lst, state="readonly", width=5)
player_start_cb.set(1)
player_start_cb.grid(row=1, column=2)
# Combo
ttk.Label(root, text="Players:", width=10).grid(row=1, column=3, padx=10, pady=5)
player_cb = ttk.Combobox(root, values=players_lst, state="readonly", width=5)
player_cb.set(5)
player_cb.grid(row=1, column=4)
    
graph_btn = ttk.Button(root, text="View Graph", command=open_image_window)
graph_btn.grid(row=1, column=5, padx=10, pady=5)

# Run the main loop
root.mainloop()
