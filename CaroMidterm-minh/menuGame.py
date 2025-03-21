import tkinter as tk
import sys  # Import sys module to use sys.exit()

class GameMenu:
    def __init__(self, game=None):
        self.game = game
        self.root = None
        
    def run(self):
        self.root = tk.Tk()
        self.root.title("Game Menu")
        self.root.geometry("500x500")
        self.root.config(bg="#FFEB3B")
        
        # Create title label
        title_label = tk.Label(
            self.root, 
            text="Game Menu", 
            font=("Arial", 30, "bold"), 
            bg="#FFEB3B", 
            fg="darkblue"
        )
        title_label.pack(pady=30)
        
        # Create buttons
        player_button = tk.Button(
            self.root, 
            text="Chơi với người", 
            width=25, 
            height=3, 
            font=("Arial", 16), 
            bg="#f1f1f1", 
            fg="black", 
            relief="flat", 
            bd=0, 
            command=self.play_with_player
        )
        player_button.pack(pady=15)
        player_button.bind("<Enter>", self.on_enter)
        player_button.bind("<Leave>", self.on_leave)
        
        computer_button = tk.Button(
            self.root, 
            text="Chơi với máy", 
            width=25, 
            height=3, 
            font=("Arial", 16), 
            bg="#f1f1f1", 
            fg="black", 
            relief="flat", 
            bd=0, 
            command=self.play_with_computer
        )
        computer_button.pack(pady=15)
        computer_button.bind("<Enter>", self.on_enter)
        computer_button.bind("<Leave>", self.on_leave)
        
        exit_button = tk.Button(
            self.root, 
            text="Thoát", 
            width=25, 
            height=3, 
            font=("Arial", 16), 
            bg="#f1f1f1", 
            fg="black", 
            relief="flat", 
            bd=0, 
            command=self.exit_game
        )
        exit_button.pack(pady=15)
        exit_button.bind("<Enter>", self.on_enter)
        exit_button.bind("<Leave>", self.on_leave)
        
        self.root.mainloop()
    
    def play_with_player(self):
        print("Chơi với người đã được chọn!")
        if self.game:
            self.game.change_gamemode('pvp')
        self.close_menu()
    
    def play_with_computer(self):
        print("Chơi với máy đã được chọn!")
        if self.game:
            self.game.change_gamemode('ai')
        self.close_menu()
    
    def exit_game(self):
        print("Thoát game...")
        self.close_menu()
        sys.exit()
    
    def close_menu(self):
        if self.root:
            self.root.quit()
            self.root.destroy()
    
    def on_enter(self, e):
        e.widget.config(bg="#4CAF50", fg="white")
        e.widget.config(font=("Arial", 16, "bold"))
    
    def on_leave(self, e):
        e.widget.config(bg="#f1f1f1", fg="black")
        e.widget.config(font=("Arial", 16))

# Function to create and run the menu
def create_menu_window(game=None):
    menu = GameMenu(game)
    menu.run()