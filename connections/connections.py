import tkinter as tk
from tkinter import messagebox

# Sample data
words = [
    "Apple", "Orange", "Banana", "Grape",  # Fruits
    "Car", "Truck", "Bus", "Bike",         # Vehicles
    "Red", "Blue", "Green", "Yellow",      # Colors
    "Cat", "Dog", "Mouse", "Horse"         # Animals
]

groups = {
    "Fruits": {"Apple", "Orange", "Banana", "Grape"},
    "Vehicles": {"Car", "Truck", "Bus", "Bike"},
    "Colors": {"Red", "Blue", "Green", "Yellow"},
    "Animals": {"Cat", "Dog", "Mouse", "Horse"}
}

class ConnectionsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Connections Game")
        
        self.selected = []
        self.remaining_groups = set(groups.keys())
        
        # Shuffle words and create buttons
        import random
        random.shuffle(words)
        
        self.buttons = {}
        for i, word in enumerate(words):
            btn = tk.Button(root, text=word, width=10, height=2,
                            command=lambda w=word: self.select_word(w))
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.buttons[word] = btn
        
        # Reset button
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=4, column=0, columnspan=4, pady=10)

    def select_word(self, word):
        if word in self.selected:
            self.selected.remove(word)
            self.buttons[word].config(relief="raised")
        else:
            self.selected.append(word)
            self.buttons[word].config(relief="sunken")
        
        if len(self.selected) == 4:
            self.check_group()

    def check_group(self):
        selected_set = set(self.selected)
        for group_name, group_words in groups.items():
            if selected_set == group_words and group_name in self.remaining_groups:
                self.correct_group(group_name)
                return
        
        self.incorrect_group()

    def correct_group(self, group_name):
        messagebox.showinfo("Correct!", f"You found the group: {group_name}")
        for word in self.selected:
            self.buttons[word].config(state="disabled", relief="flat")
        self.selected.clear()
        self.remaining_groups.remove(group_name)
        
        if not self.remaining_groups:
            messagebox.showinfo("Congratulations!", "You found all groups!")
            self.reset_game()

    def incorrect_group(self):
        messagebox.showerror("Incorrect", "Those words do not form a valid group.")
        for word in self.selected:
            self.buttons[word].config(relief="raised")
        self.selected.clear()

    def reset_game(self):
        for word, btn in self.buttons.items():
            btn.config(state="normal", relief="raised")
        self.selected.clear()
        self.remaining_groups = set(groups.keys())
'''
# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectionsGame(root)
    root.mainloop()

class ConnectionsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Connections Game")
        self.player_name = None
        self.lives = 4

        # Start screen setup
        self.start_frame = tk.Frame(root)
        self.start_frame.pack()

        tk.Label(self.start_frame, text="Enter your name:").pack(pady=10)
        self.name_entry = tk.Entry(self.start_frame)
        self.name_entry.pack(pady=5)
        tk.Button(self.start_frame, text="Submit", command=self.start_game).pack(pady=10)

    def start_game(self):
        self.player_name = self.name_entry.get()
        if not self.player_name.strip():
            messagebox.showwarning("Name Required", "Please enter your name to start the game.")
            return

        # Hide start frame and setup game
        self.start_frame.pack_forget()
        self.setup_game()

    def setup_game(self):
        self.lives = 4
        self.selected = []
        self.remaining_groups = set(groups.keys())

        # Main game frame
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()

        # Header
        header = tk.Frame(self.game_frame)
        header.pack(pady=10)
        tk.Label(header, text=f"Player: {self.player_name}", font=("Arial", 16)).grid(row=0, column=0, sticky="w")
        self.lives_label = tk.Label(header, text=f"Lives: {self.lives}", font=("Arial", 16), fg="red")
        self.lives_label.grid(row=0, column=1, sticky="e")

        # Buttons grid
        self.buttons_frame = tk.Frame(self.game_frame)
        self.buttons_frame.pack()

        self.correct_frame = tk.Frame(self.game_frame)
        self.correct_frame.pack(pady=10)

        # Shuffle and Reset Buttons
        control_frame = tk.Frame(self.game_frame)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Shuffle", command=self.shuffle_grid).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Reset", command=self.reset_game).grid(row=0, column=1, padx=5)

        # Shuffle and display buttons
        self.shuffle_grid()

    def shuffle_grid(self):
        import random
        random.shuffle(words)

        # Clear the buttons frame
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        self.buttons = {}
        for i, word in enumerate(words):
            btn = tk.Button(self.buttons_frame, text=word, width=10, height=2,
                            command=lambda w=word: self.select_word(w))
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.buttons[word] = btn

    def select_word(self, word):
        if word in self.selected:
            self.selected.remove(word)
            self.buttons[word].config(relief="raised")
        else:
            self.selected.append(word)
            self.buttons[word].config(relief="sunken")

        if len(self.selected) == 4:
            self.check_group()

    def check_group(self):
        selected_set = set(self.selected)
        for group_name, group_words in groups.items():
            if selected_set == group_words and group_name in self.remaining_groups:
                self.correct_group(group_name)
                return

        self.incorrect_group()

    def correct_group(self, group_name):
        messagebox.showinfo("Correct!", f"You found the group: {group_name}")
        for word in self.selected:
            btn = self.buttons.pop(word)
            btn.config(state="disabled", relief="flat")
            btn.pack(in_=self.correct_frame, side="left", padx=5)

        self.selected.clear()
        self.remaining_groups.remove(group_name)

        if not self.remaining_groups:
            messagebox.showinfo("Congratulations!", "You found all groups!")
            self.reset_game()

    def incorrect_group(self):
        self.lives -= 1
        self.lives_label.config(text=f"Lives: {self.lives}")
        if self.lives == 0:
            messagebox.showerror("Game Over", "You ran out of lives! Restarting the game.")
            self.game_frame.pack_forget()
            self.start_frame.pack()
            return

        messagebox.showerror("Incorrect", "Those words do not form a valid group.")
        for word in self.selected:
            self.buttons[word].config(relief="raised")
        self.selected.clear()

    def reset_game(self):
        self.game_frame.pack_forget()
        self.setup_game()


# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectionsGame(root)
    root.mainloop()
'''