import copy
import sys
import pygame
import random
import numpy as np
from constants import *

# --- PYGAME SETUP ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

# --- CLASSES ---

class Board:
    def __init__(self):
        self.squares = np.zeros((10, 10))  # 10x10 board
        self.empty_sqrs = self.squares  # [squares]
        self.marked_sqrs = 0

    def final_state(self, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''
        # For 10x10 board, we'll check for 5 in a row to win
        win_length = 5

        # Check vertical wins
        for col in range(10):
            for row in range(10 - win_length + 1):
                if all(self.squares[row + i][col] == self.squares[row][col] for i in range(win_length)) and self.squares[row][col] != 0:
                    if show:
                        color = CIRC_COLOR if self.squares[row][col] == 2 else CROSS_COLOR
                        iPos = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
                        fPos = (col * SQSIZE + SQSIZE // 2, (row + win_length - 1) * SQSIZE + SQSIZE // 2)
                        pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                    return self.squares[row][col]

        # Check horizontal wins
        for row in range(10):
            for col in range(10 - win_length + 1):
                if all(self.squares[row][col + i] == self.squares[row][col] for i in range(win_length)) and self.squares[row][col] != 0:
                    if show:
                        color = CIRC_COLOR if self.squares[row][col] == 2 else CROSS_COLOR
                        iPos = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
                        fPos = ((col + win_length - 1) * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
                        pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                    return self.squares[row][col]

        # Check diagonal wins (descending)
        for row in range(10 - win_length + 1):
            for col in range(10 - win_length + 1):
                if all(self.squares[row + i][col + i] == self.squares[row][col] for i in range(win_length)) and self.squares[row][col] != 0:
                    if show:
                        color = CIRC_COLOR if self.squares[row][col] == 2 else CROSS_COLOR
                        iPos = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
                        fPos = ((col + win_length - 1) * SQSIZE + SQSIZE // 2, (row + win_length - 1) * SQSIZE + SQSIZE // 2)
                        pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
                    return self.squares[row][col]

        # Check diagonal wins (ascending)
        for row in range(win_length - 1, 10):
            for col in range(10 - win_length + 1):
                if all(self.squares[row - i][col + i] == self.squares[row][col] for i in range(win_length)) and self.squares[row][col] != 0:
                    if show:
                        color = CIRC_COLOR if self.squares[row][col] == 2 else CROSS_COLOR
                        iPos = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
                        fPos = ((col + win_length - 1) * SQSIZE + SQSIZE // 2, (row - win_length + 1) * SQSIZE + SQSIZE // 2)
                        pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
                    return self.squares[row][col]

        # No win yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(10):
            for col in range(10):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 100  # 10x10 = 100 cells

    def isempty(self):
        return self.marked_sqrs == 0

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player
        self.opponent = 1 if player == 2 else 2

    # --- RANDOM ---
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        if empty_sqrs:  # Make sure there are empty squares
            idx = random.randrange(0, len(empty_sqrs))
            return empty_sqrs[idx]  # (row, col)
        return None  # Return None if no empty squares (shouldn't happen)

    # --- EVALUATION FUNCTION ---
    def evaluate_board(self, board):
        win_length = 5  # For 10x10 board, we check for 5 in a row
        
        # Terminal states
        final_state = board.final_state()
        if final_state == self.player:  # AI wins
            return 10000
        elif final_state == self.opponent:  # Human wins
            return -10000
        elif board.isfull():  # Draw
            return 0
        
        # Non-terminal evaluation
        score = 0
        
        # Evaluate rows
        for row in range(10):
            for col in range(10 - win_length + 1):
                window = [board.squares[row][col + i] for i in range(win_length)]
                score += self.evaluate_window(window)
        
        # Evaluate columns
        for col in range(10):
            for row in range(10 - win_length + 1):
                window = [board.squares[row + i][col] for i in range(win_length)]
                score += self.evaluate_window(window)
        
        # Evaluate diagonals (descending)
        for row in range(10 - win_length + 1):
            for col in range(10 - win_length + 1):
                window = [board.squares[row + i][col + i] for i in range(win_length)]
                score += self.evaluate_window(window)
        
        # Evaluate diagonals (ascending)
        for row in range(win_length - 1, 10):
            for col in range(10 - win_length + 1):
                window = [board.squares[row - i][col + i] for i in range(win_length)]
                score += self.evaluate_window(window)
        
        # Evaluate strategic positions
        # Center positions are more valuable
        center_value = 3
        for row in range(3, 7):
            for col in range(3, 7):
                if board.squares[row][col] == self.player:  # AI
                    score += center_value
                elif board.squares[row][col] == self.opponent:  # Human
                    score -= center_value
        
        return score
    
    def evaluate_window(self, window):
        win_length = 5
        score = 0
        
        # Count pieces in the window
        ai_count = window.count(self.player)
        human_count = window.count(self.opponent)
        empty_count = window.count(0)
        
        # Ensure no mixed pieces (both AI and human in the same window)
        if ai_count > 0 and human_count > 0:
            return 0  # Window is blocked
        
        # Calculate score based on piece configuration
        if ai_count == win_length:
            return 1000  # Immediate win
        
        # Threat levels for AI
        if ai_count == 4 and empty_count == 1:
            score += 500  # One move away from winning
        elif ai_count == 3 and empty_count == 2:
            score += 50  # Two moves away from winning
        elif ai_count == 2 and empty_count == 3:
            score += 10  # Developing position
        
        # Threat levels for human
        if human_count == win_length:
            return -1000  # Immediate loss
        
        if human_count == 4 and empty_count == 1:
            score -= 500  # Block immediate threat
        elif human_count == 3 and empty_count == 2:
            score -= 50  # Block developing threat
        elif human_count == 2 and empty_count == 3:
            score -= 10  # Block early development
        
        return score
    
    # --- MINIMAX WITH ALPHA-BETA PRUNING ---
    def minimax(self, board, maximizing, depth, max_depth, alpha=-float('inf'), beta=float('inf')):
        # Terminal case or max depth reached
        if depth >= max_depth:
            return self.evaluate_board(board), None
        
        case = board.final_state()
        if case == self.player:  # AI wins
            return 10000 - depth, None  # Prefer quicker wins
        if case == self.opponent:  # Human wins
            return -10000 + depth, None  # Delay losses
        if board.isfull():  # Draw
            return 0, None
        
        # For 10x10 board, we need to be more selective about moves to consider
        empty_sqrs = self.get_strategic_moves(board)
        
        if not empty_sqrs:  # Safety check
            return 0, None
        
        if maximizing:
            max_eval = -float('inf')
            best_move = empty_sqrs[0]  # Default to first move
            
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)  # AI move
                eval, _ = self.minimax(temp_board, False, depth + 1, max_depth, alpha, beta)
                
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break  # Prune branch
            
            return max_eval, best_move
        
        else:
            min_eval = float('inf')
            best_move = empty_sqrs[0]  # Default to first move
            
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.opponent)  # Human move
                eval, _ = self.minimax(temp_board, True, depth + 1, max_depth, alpha, beta)
                
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
                
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break  # Prune branch
            
            return min_eval, best_move
    
    def get_strategic_moves(self, board):
        """Get a list of strategic moves to consider instead of all empty squares"""
        empty_sqrs = board.get_empty_sqrs()
        
        # If the board is empty or nearly empty, just play near the center
        if board.isempty() or board.marked_sqrs < 3:
            return [(r, c) for r in range(3, 7) for c in range(3, 7) 
                    if (r, c) in empty_sqrs][:5]
        
        # For a 10x10 board, we can't consider all empty squares in minimax
        # We'll focus on squares that are adjacent to already occupied squares
        strategic_moves = []
        
        for (row, col) in empty_sqrs:
            # Check if this square is adjacent to any occupied square
            is_adjacent = False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    
                    r, c = row + dr, col + dc
                    if 0 <= r < 10 and 0 <= c < 10 and board.squares[r][c] != 0:
                        is_adjacent = True
                        break
                if is_adjacent:
                    break
            
            if is_adjacent:
                strategic_moves.append((row, col))
        
        # If no strategic moves found or if we have too few options, add some default moves
        if len(strategic_moves) < 5:
            # Add center positions
            center_moves = [(r, c) for r in range(3, 7) for c in range(3, 7) 
                           if (r, c) in empty_sqrs and (r, c) not in strategic_moves]
            strategic_moves.extend(center_moves[:5])
            
            # If still not enough, add some random moves
            if len(strategic_moves) < 5:
                remaining = [move for move in empty_sqrs if move not in strategic_moves]
                strategic_moves.extend(remaining[:5])
        
        # Limit to 10 moves maximum to keep calculation time reasonable
        if len(strategic_moves) > 10:
            strategic_moves = strategic_moves[:10]
            
        return strategic_moves
    
    def find_winning_move(self, board, player):
        """Find a move that would immediately win the game"""
        for (row, col) in board.get_empty_sqrs():
            temp_board = copy.deepcopy(board)
            temp_board.mark_sqr(row, col, player)
            if temp_board.final_state() == player:
                return (row, col)
        return None
    
    # --- MAIN EVAL ---
    def eval(self, main_board, max_depth=2):
        if main_board.isempty():
            # If board is empty, choose a position in the center area
            return random.randint(3, 6), random.randint(3, 6)
            
        if self.level == 0:
            # Random choice
            move = self.rnd(main_board)
            if move is None:  # Safety check
                # If no empty squares, just return something (shouldn't happen)
                print("Warning: No empty squares found for random move")
                return 0, 0
            return move
        else:
            try:
                # Check for immediate win
                win_move = self.find_winning_move(main_board, self.player)
                if win_move:
                    return win_move
                    
                # Check for immediate block
                block_move = self.find_winning_move(main_board, self.opponent)
                if block_move:
                    return block_move
                
                # Limit depth to keep calculation time reasonable
                adjusted_depth = min(max_depth, 2)
                
                # Use minimax for strategic play
                _, move = self.minimax(main_board, True, depth=0, max_depth=adjusted_depth)
                
                # Safety check in case minimax returns None
                if move is None:
                    print("Warning: Minimax returned None")
                    return self.rnd(main_board)
                    
                return move  # row, col
            
            except Exception as e:
                print(f"Error in AI eval: {e}")
                # Fall back to random move if minimax fails
                return self.rnd(main_board)

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1   # 1-cross  # 2-circles
        self.gamemode = 'pvp'  # Default to pvp
        self.running = True
        self.show_lines()
        self.turn_count = 0  # Total turns played
        self.player_moves = 0  # Number of player moves
        self.human_piece = 1  # Default human plays as X (1)

    # --- DRAW METHODS ---
    def show_lines(self):
        screen.fill(BG_COLOR)
        # Draw vertical lines
        for i in range(1, 10):  # for a 10x10 grid, 9 vertical lines
            pygame.draw.line(screen, LINE_COLOR, (i * SQSIZE, 0), (i * SQSIZE, HEIGHT), LINE_WIDTH)
        # Draw horizontal lines
        for i in range(1, 10):  # for a 10x10 grid, 9 horizontal lines
            pygame.draw.line(screen, LINE_COLOR, (0, i * SQSIZE), (WIDTH, i * SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross (X)
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            # draw circle (O)
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    # --- OTHER METHODS ---
    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        # Store current player before changing
        current_player = self.player
        # Switch player
        self.player = self.player % 2 + 1
        self.turn_count += 1  # Increment total turns
        if current_player == self.human_piece:  # If human player just moved
            self.player_moves += 1  # Increment player moves count

    def change_gamemode(self, gamemode):
        self.gamemode = gamemode

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

    def set_player_piece(self, piece):
        """Set whether the human player is X (1) or O (2)"""
        self.human_piece = piece
        # Set AI to use the opposite piece
        self.ai.player = 2 if piece == 1 else 1
        self.ai.opponent = piece

class Menu:
    def __init__(self, game):
        self.game = game
        
    def run(self):
        import tkinter as tk
        
        root = tk.Tk()
        root.title("Game Menu")
        root.geometry("500x500")
        root.config(bg="#FFEB3B")
        
        # Title
        title_label = tk.Label(root, text="Game Menu", font=("Arial", 30, "bold"), bg="#FFEB3B", fg="darkblue")
        title_label.pack(pady=30)
        
        # Button style functions
        def on_enter(e):
            e.widget.config(bg="#4CAF50", fg="white", font=("Arial", 16, "bold"))
        
        def on_leave(e):
            e.widget.config(bg="#f1f1f1", fg="black", font=("Arial", 16))
        
        # PvP Button
        def select_pvp():
            self.game.change_gamemode('pvp')
            root.destroy()
        
        pvp_button = tk.Button(
            root, 
            text="Chơi với người", 
            width=25, 
            height=3, 
            font=("Arial", 16), 
            bg="#f1f1f1", 
            fg="black", 
            relief="flat", 
            bd=0, 
            command=select_pvp
        )
        pvp_button.pack(pady=15)
        pvp_button.bind("<Enter>", on_enter)
        pvp_button.bind("<Leave>", on_leave)
        
        # AI Button
        def select_ai():
            self.game.change_gamemode('ai')
            root.destroy()
            
        ai_button = tk.Button(
            root, 
            text="Chơi với máy", 
            width=25, 
            height=3, 
            font=("Arial", 16), 
            bg="#f1f1f1", 
            fg="black", 
            relief="flat", 
            bd=0, 
            command=select_ai
        )
        ai_button.pack(pady=15)
        ai_button.bind("<Enter>", on_enter)
        ai_button.bind("<Leave>", on_leave)
        
        # Exit Button
        def exit_game():
            root.destroy()
            pygame.quit()
            sys.exit()
            
        exit_button = tk.Button(
            root, 
            text="Thoát", 
            width=25, 
            height=3, 
            font=("Arial", 16), 
            bg="#f1f1f1", 
            fg="black", 
            relief="flat", 
            bd=0, 
            command=exit_game
        )
        exit_button.pack(pady=15)
        exit_button.bind("<Enter>", on_enter)
        exit_button.bind("<Leave>", on_leave)
        
        root.mainloop()

def main():
    # Initialize game
    game = Game()
    board = game.board
    ai = game.ai
    
    # Show menu
    menu = Menu(game)
    menu.run()
    
    # After menu selection, ensure the screen is properly set up
    screen.fill(BG_COLOR)
    game.show_lines()
    pygame.display.update()
    
    # Main game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Key events
            if event.type == pygame.KEYDOWN:
                # r-restart the game
                if event.key == pygame.K_r:
                    game.reset()
                
                # g-change gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode('pvp' if game.gamemode == 'ai' else 'ai')
                    
                # Change AI difficulty
                if event.key == pygame.K_0:
                    ai.level = 0
                elif event.key == pygame.K_1:
                    ai.level = 1
                    
                # Change player piece
                if event.key == pygame.K_x:
                    game.reset()
                    game.set_player_piece(1)  # X
                elif event.key == pygame.K_o:
                    game.reset()
                    game.set_player_piece(2)  # O

            # Mouse click event
            if event.type == pygame.MOUSEBUTTONDOWN and game.running:
                pos = event.pos
                row, col = pos[1] // SQSIZE, pos[0] // SQSIZE
                
                # Ensure the click is within the board boundaries
                if 0 <= row < 10 and 0 <= col < 10:
                    # Only allow player to move if it's their turn
                    if game.player == game.human_piece and board.empty_sqr(row, col):
                        game.make_move(row, col)
                        
                        # Check if game is over after player move
                        if game.isover():
                            game.running = False

        # AI turn
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            # Simple delay to make AI move visible
            pygame.time.delay(300)
            
            try:
                # Calculate move with limited depth based on game progress
                max_depth = 2  # Keep max_depth low for better performance
                row, col = ai.eval(board, max_depth)
                
                # Verify move is valid before making it
                if 0 <= row < 10 and 0 <= col < 10 and board.empty_sqr(row, col):
                    game.make_move(row, col)
                    
                    # Check if game is over after AI move
                    if game.isover():
                        game.running = False
                else:
                    print(f"Invalid AI move: ({row}, {col})")
                    # Choose random valid move as fallback
                    valid_moves = board.get_empty_sqrs()
                    if valid_moves:
                        row, col = random.choice(valid_moves)
                        game.make_move(row, col)
            except Exception as e:
                print(f"Error during AI turn: {e}")
                # Choose random valid move as fallback
                valid_moves = board.get_empty_sqrs()
                if valid_moves:
                    row, col = random.choice(valid_moves)
                    game.make_move(row, col)

        pygame.display.update()

if __name__ == "__main__":
    main()