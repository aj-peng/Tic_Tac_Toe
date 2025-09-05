from tkinter import *
import random

# Game Config
CELLS = 9
GAME_WIDTH = 720
GAME_HEIGHT = GAME_WIDTH
CELL_SIZE = GAME_WIDTH // 3
BACKGROUND_COLOR = "#000000"
X_COLOR = "#1167b1"
O_COLOR = "#b11111"

# Game state
x_score = 0
o_score = 0
playing = False
ai_enabled = True  # Set to True for single-player mode
ai_delay = 500  # milliseconds

# Class definition
class TicTacToe:
    def __init__(self):
        self.board = {i: '' for i in range(9)}
        self.current_player = 'X'
    
    def reset_board(self):
        self.board = {i: '' for i in range(9)}
        self.current_player = 'X'
        canvas.delete(ALL)
        self.draw_board()

    def draw_board(self):
        canvas.delete("grid")
        for i in range(1, 3):
            canvas.create_line(i * (GAME_WIDTH // 3), 0, i * (GAME_WIDTH // 3), GAME_HEIGHT, 
                               fill="white", width=2, tag="grid") # Vertical line
            canvas.create_line(0, i * (GAME_HEIGHT // 3), GAME_WIDTH, i * (GAME_HEIGHT // 3), 
                               fill="white", width=2, tag="grid") # Horizontal line
            
    def draw_move(self, cell: int):
        x = (cell % 3) * (GAME_WIDTH // 3) + (GAME_WIDTH // 6)
        y = (cell // 3) * (GAME_HEIGHT // 3) + (GAME_HEIGHT // 6)
        color = X_COLOR if self.board[cell] == 'X' else O_COLOR
        canvas.create_text(x, y, font=('Arial', 72), text=self.board[cell], fill=color, tag="move")
    
    def make_move(self, cell: int):
        if self.board[cell] == '' and playing:
            self.board[cell] = self.current_player
            self.draw_move(cell)
            if self.check_winner():
                end_game("{} wins!".format(self.current_player))
            elif all(self.board[i] != '' for i in range(9)):
                end_game("It's a draw!")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if ai_enabled and self.current_player == 'O':
                    window.after(ai_delay, self.ai_move)
    
    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # Columns
            (0, 4, 8), (2, 4, 6)             # Diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != '':
                return True
        return False

    def on_click(self, event: Event):
        if playing and not (ai_enabled and self.current_player == 'O'):
            col = event.x // CELL_SIZE
            row = event.y // CELL_SIZE
            cell = row * 3 + col
            self.make_move(cell)

    def ai_move(self):
        if not playing or self.current_player != 'O':
            return
            
        available_cells = [i for i in range(9) if self.board[i] == '']
        if not available_cells:
            return
            
        # Check if AI can win in the next move
        for cell in available_cells:
            self.board[cell] = 'O'
            if self.check_winner():
                self.board[cell] = ''
                self.make_move(cell)
                return
            self.board[cell] = ''
            
        # Block opponent's winning move
        for cell in available_cells:
            self.board[cell] = 'X'
            if self.check_winner():
                self.board[cell] = ''
                self.make_move(cell)
                return
            self.board[cell] = ''
            
        # Try to take center if available
        if 4 in available_cells:
            self.make_move(4)
            return
            
        # Try to take corners
        corners = [0, 2, 6, 8]
        available_corners = [c for c in corners if c in available_cells]
        if available_corners:
            self.make_move(random.choice(available_corners))
            return
        
        # Otherwise, pick a random cell
        self.make_move(random.choice(available_cells))

# Game functions
def update_score():
    label.config(text="X: {}  O: {}".format(x_score, o_score))

def reset_game():
    global playing
    playing = True
    canvas.delete(ALL)
    ticTacToe.reset_board()

def end_game(message: str):
    global playing, x_score, o_score
    if not playing:
        return

    playing = False
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, 
                       font=('Arial', 28), text=message, fill="yellow", tag="menu")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 40, 
                       font=('Arial', 18), text="[Press SPACE to Play Again]", fill="yellow", tag="menu")
    
    if "X wins" in message:
        x_score += 1
    elif "O wins" in message:
        o_score += 1
    update_score()

def start_screen():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 20, 
                       font=('Arial', 28), text="TIC TAC TOE", fill="white", tag="menu")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 30, 
                       font=('Arial', 18), text="Use mouse1 to claim squares", fill="white", tag="menu")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 70, 
                       font=('Arial', 18), text="[Press SPACE to Play]", fill="white", tag="menu")

# Setup
ticTacToe = TicTacToe()

window = Tk()
window.title("Tic Tac Toe")
window.resizable(False, False)

label = Label(window, font=('Arial', 24))
label.pack(side="bottom")
update_score()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind("<space>", lambda event: reset_game())
canvas.bind("<Button-1>", ticTacToe.on_click)

start_screen()
window.mainloop()
