import tkinter as tk
from tkinter import messagebox
import random
import copy

class LightsOutGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Lights Out")
        self.root.geometry("400x500")
        self.root.resizable(True, True)
        
        # Game state
        self.grid_size = 5
        self.grid = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.original_grid = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.move_history = []
        self.game_won = False
        
        # Create UI
        self.create_ui()
        
        # Start new game
        self.new_game()
    
    def create_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Grid frame
        grid_frame = tk.Frame(main_frame)
        grid_frame.pack(pady=(0, 20))
        
        # Create light buttons
        self.light_buttons = []
        for i in range(self.grid_size):
            row_buttons = []
            for j in range(self.grid_size):
                btn = tk.Button(
                    grid_frame,
                    width=4,
                    height=2,
                    command=lambda row=i, col=j: self.on_light_click(row, col),
                    bg='black',
                    activebackground='yellow',
                    relief=tk.RAISED,
                    borderwidth=2
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(btn)
            self.light_buttons.append(row_buttons)
        
        # Controls frame
        controls_frame = tk.Frame(main_frame)
        controls_frame.pack()
        
        # New Game button
        self.new_game_btn = tk.Button(
            controls_frame,
            text="New Game",
            command=self.new_game,
            width=10
        )
        self.new_game_btn.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        self.reset_btn = tk.Button(
            controls_frame,
            text="Reset",
            command=self.reset_game,
            width=10
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Undo button
        self.undo_btn = tk.Button(
            controls_frame,
            text="Undo",
            command=self.undo_move,
            width=10
        )
        self.undo_btn.pack(side=tk.LEFT, padx=5)
        
        # Win message label
        self.win_label = tk.Label(
            main_frame,
            text="You Win!",
            font=("Arial", 16, "bold"),
            fg="green"
        )
        self.win_label.pack(pady=(10, 0))
        self.win_label.pack_forget()  # Hide initially
    
    def toggle_cell(self, grid, row, col):
        """Toggle a cell and its orthogonal neighbors. Used for both generation and moves."""
        if row < 0 or row >= self.grid_size or col < 0 or col >= self.grid_size:
            return
        
        # Define orthogonal neighbors
        neighbors = [
            (row, col),      # center
            (row - 1, col),  # up
            (row + 1, col),  # down
            (row, col - 1),  # left
            (row, col + 1),  # right
        ]
        
        for nr, nc in neighbors:
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                grid[nr][nc] = not grid[nr][nc]
    
    def generate_puzzle(self):
        """Generate a random solvable puzzle by applying random moves from all-off state."""
        # Start with all lights off
        grid = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Apply random moves until we get a puzzle with at least one light on
        while True:
            # Clear grid
            grid = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
            # Apply random number of random moves
            num_moves = random.randint(10, 30)  # Random number of moves for variety
            for _ in range(num_moves):
                row = random.randint(0, self.grid_size - 1)
                col = random.randint(0, self.grid_size - 1)
                self.toggle_cell(grid, row, col)
            
            # Check if puzzle has at least one light on
            has_on_light = any(any(row) for row in grid)
            if has_on_light:
                break
        
        return grid
    
    def new_game(self):
        """Generate a fresh puzzle and make it the new reset state."""
        # Generate new puzzle
        new_puzzle = self.generate_puzzle()
        self.grid = copy.deepcopy(new_puzzle)
        self.original_grid = copy.deepcopy(new_puzzle)
        
        # Clear move history and hide win message
        self.move_history = []
        self.game_won = False
        self.win_label.pack_forget()
        
        # Update display
        self.update_display()
    
    def reset_game(self):
        """Reset to the original puzzle state."""
        self.grid = copy.deepcopy(self.original_grid)
        self.move_history = []
        self.game_won = False
        self.win_label.pack_forget()
        self.update_display()
    
    def undo_move(self):
        """Undo the most recent move."""
        if not self.move_history:
            return
        
        # Restore previous grid state
        previous_grid = self.move_history.pop()
        self.grid = previous_grid
        
        # If we were won and undoing brings us back, we're no longer won
        # Check win state
        self.check_win()
        
        self.update_display()
    
    def on_light_click(self, row, col):
        """Handle light button click."""
        if self.game_won:
            return
        
        # Save current state to move history before changing
        self.move_history.append(copy.deepcopy(self.grid))
        
        # Apply move
        self.toggle_cell(self.grid, row, col)
        
        # Update display and check win
        self.update_display()
        self.check_win()
    
    def check_win(self):
        """Check if all lights are off (win condition)."""
        all_off = all(not light for row in self.grid for light in row)
        if all_off and not self.game_won:
            self.game_won = True
            self.win_label.pack()
        elif not all_off and self.game_won:
            # This can happen after undo from won state
            self.game_won = False
            self.win_label.pack_forget()
        elif all_off and self.game_won:
            # Already won, keep message
            pass
    
    def update_display(self):
        """Update all light button colors based on current grid state."""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j]:
                    # Light is on - yellow
                    self.light_buttons[i][j].config(bg='yellow')
                else:
                    # Light is off - black
                    self.light_buttons[i][j].config(bg='black')

def main():
    root = tk.Tk()
    game = LightsOutGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
