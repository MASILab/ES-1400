import tkinter as tk
from tkinter import messagebox
import random
import pickle

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []
        self.create_widgets()
        self.q_table = self.load_q_table()
        self.epsilon = 0.1  # Exploration factor
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.previous_state = None
        self.previous_action = None

        # Train the agent with self-play for 10 games
        self.train(10)
        self.status_label.config(text="Training completed. You can start playing!")

    def create_widgets(self):
        self.status_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.status_label.grid(row=0, column=0, columnspan=3)

        for i in range(9):
            button = tk.Button(self.root, text="", font=("Arial", 24), width=5, height=2,
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=(i // 3) + 1, column=i % 3)
            self.buttons.append(button)

    def on_button_click(self, index):
        if self.board[index] == "" and self.current_player == "X":
            self.make_move(index, "X")
            if not self.check_winner() and "" in self.board:
                self.root.after(500, self.computer_move)

    def make_move(self, index, player):
        self.board[index] = player
        self.update_board()
        if self.check_winner():
            if player == "X":
                messagebox.showinfo("Tic Tac Toe", f"Player {player} wins!")
                self.update_q_table(-1)
            else:
                messagebox.showinfo("Tic Tac Toe", f"Computer wins!")
                self.update_q_table(1)
            self.reset_game()
        elif "" not in self.board:
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            self.update_q_table(0)
            self.reset_game()
        else:
            self.current_player = "O" if player == "X" else "X"

    def computer_move(self):
        state = self.get_state(self.board)
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice([i for i in range(9) if self.board[i] == ""])
        else:
            q_values = [self.q_table.get((state, i), 0) for i in range(9)]
            action = self.best_action(q_values)

        while self.board[action] != "":
            action = random.choice([i for i in range(9) if self.board[i] == ""])

        self.make_move(action, "O")

        if self.previous_state is not None and self.previous_action is not None:
            self.update_q_value(self.previous_state, self.previous_action, state, 0)

        self.previous_state = state
        self.previous_action = action

    def best_action(self, q_values):
        max_value = max(q_values)
        return random.choice([i for i, q in enumerate(q_values) if q == max_value])

    def get_state(self, board):
        return tuple(board)

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

    def update_q_table(self, reward):
        if self.previous_state is not None and self.previous_action is not None:
            self.update_q_value(self.previous_state, self.previous_action, self.get_state(self.board), reward)
        self.save_q_table()

    def update_q_value(self, state, action, next_state, reward):
        q_value = self.q_table.get((state, action), 0)
        available_actions = [a for a in range(9) if next_state[a] == ""]
        if available_actions:
            max_next_q_value = max([self.q_table.get((next_state, a), 0) for a in available_actions])
        else:
            max_next_q_value = 0
        self.q_table[(state, action)] = q_value + self.learning_rate * (reward + self.discount_factor * max_next_q_value - q_value)

    def reset_game(self):
        self.board = [""] * 9
        self.update_board()
        self.current_player = "X"
        self.previous_state = None
        self.previous_action = None

    def update_board(self):
        for i in range(9):
            self.buttons[i].config(text=self.board[i])

    def load_q_table(self):
        try:
            with open("q_table.pkl", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def save_q_table(self):
        with open("q_table.pkl", "wb") as f:
            pickle.dump(self.q_table, f)

    def train(self, episodes):
        for episode in range(episodes):
            print(f"Training episode {episode + 1}/{episodes}")
            self.status_label.config(text=f"Training episode {episode + 1}/{episodes}")
            self.board = [""] * 9
            self.update_board()
            self.current_player = "X"
            self.previous_state = None
            self.previous_action = None
            while "" in self.board and not self.check_winner():
                if self.current_player == "X":
                    available_moves = [i for i in range(9) if self.board[i] == ""]
                    action = random.choice(available_moves)
                    self.board[action] = "X"
                    self.update_board()
                    if self.previous_state is not None and self.previous_action is not None:
                        self.update_q_value(self.previous_state, self.previous_action, self.get_state(self.board), 0)
                    self.previous_state = self.get_state(self.board)
                    self.previous_action = action
                    if self.check_winner():
                        self.update_q_table(-1)
                        print(f"Episode {episode + 1}: X wins")
                        self.status_label.config(text=f"Episode {episode + 1}: X wins")
                        break
                    self.current_player = "O"
                else:
                    available_moves = [i for i in range(9) if self.board[i] == ""]
                    action = random.choice(available_moves)
                    self.board[action] = "O"
                    self.update_board()
                    if self.previous_state is not None and self.previous_action is not None:
                        self.update_q_value(self.previous_state, self.previous_action, self.get_state(self.board), 0)
                    self.previous_state = self.get_state(self.board)
                    self.previous_action = action
                    if self.check_winner():
                        self.update_q_table(1)
                        print(f"Episode {episode + 1}: O wins")
                        self.status_label.config(text=f"Episode {episode + 1}: O wins")
                        break
                    self.current_player = "X"
                self.root.update()
                self.root.after(500)
            if "" not in self.board:
                self.update_q_table(0)
                print(f"Episode {episode + 1}: Tie")
                self.status_label.config(text=f"Episode {episode + 1}: Tie")
            self.root.update()
            self.root.after(1500)  # Show result for 1.5 seconds before resetting the game
            self.reset_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
