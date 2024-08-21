import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []
        self.create_widgets()

    def create_widgets(self):
        for i in range(9):
            button = tk.Button(self.root, text="", font=("Arial", 24), width=5, height=2,
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

    def on_button_click(self, index):
        if self.board[index] == "" and self.current_player == "X":
            self.make_move(index, "X")
            if not self.check_winner() and "" in self.board:
                self.root.after(500, self.computer_move)

    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player)
        if self.check_winner():
            messagebox.showinfo("Tic Tac Toe", f"Player {player} wins!")
            self.reset_game()
        elif "" not in self.board:
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            self.reset_game()
        else:
            self.current_player = "O" if player == "X" else "X"

    def computer_move(self):
        available_moves = [i for i, x in enumerate(self.board) if x == ""]
        move = random.choice(available_moves)
        self.make_move(move, "O")

    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != "":
                return True
        return False

    def reset_game(self):
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="")
        self.current_player = "X"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
