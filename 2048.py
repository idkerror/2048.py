import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.board = [[0]*5 for _ in range(5)]
        self.add_new_tile()
        self.add_new_tile()
        self.create_gui()
        self.update_gui()
        self.master.bind("<Key>", self.on_key_press)

    def create_gui(self):
        self.frame = tk.Frame(self.master)
        self.frame.grid()
        
        self.tiles = [[None]*5 for _ in range(5)]
        for i in range(5):
            for j in range(5):
                self.tiles[i][j] = tk.Label(self.frame, text="", width=6, height=3, font=("Helvetica", 24), bg="lightgrey", borderwidth=2, relief="groove")
                self.tiles[i][j].grid(row=i, column=j, padx=5, pady=5)

    def add_new_tile(self):
        empty_tiles = [(i, j) for i in range(5) for j in range(5) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = random.choice([2, 4])

    def update_gui(self):
        for i in range(5):
            for j in range(5):
                value = self.board[i][j]
                self.tiles[i][j].config(text=str(value) if value != 0 else "", bg=self.get_tile_color(value))
        self.master.update_idletasks()

    def get_tile_color(self, value):
        colors = {
            0: "lightgrey",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
        }
        return colors.get(value, "#3c3a32")

    def slide_left(self):
        moved = False
        for row in self.board:
            new_row = [i for i in row if i != 0]
            new_row += [0] * (5 - len(new_row))
            for i in range(4):
                if new_row[i] == new_row[i + 1] and new_row[i] != 0:
                    new_row[i] *= 2
                    new_row[i + 1] = 0
                    moved = True
            new_row = [i for i in new_row if i != 0]
            new_row += [0] * (5 - len(new_row))
            for i in range(5):
                if row[i] != new_row[i]:
                    moved = True
                row[i] = new_row[i]
        return moved

    def rotate_board_clockwise(self):
        self.board = [list(row) for row in zip(*self.board[::-1])]

    def move(self, direction):
        moved = False
        if direction == "left":
            moved = self.slide_left()
        elif direction == "right":
            self.rotate_board_clockwise()
            self.rotate_board_clockwise()
            moved = self.slide_left()
            self.rotate_board_clockwise()
            self.rotate_board_clockwise()
        elif direction == "up":
            self.rotate_board_clockwise()
            self.rotate_board_clockwise()
            self.rotate_board_clockwise()
            moved = self.slide_left()
            self.rotate_board_clockwise()
        elif direction == "down":
            self.rotate_board_clockwise()
            moved = self.slide_left()
            self.rotate_board_clockwise()
            self.rotate_board_clockwise()
            self.rotate_board_clockwise()
        if moved:
            self.add_new_tile()
            self.update_gui()
            if self.check_game_over():
                self.game_over()

    def check_game_over(self):
        for row in self.board:
            if 0 in row:
                return False
        for i in range(5):
            for j in range(4):
                if self.board[i][j] == self.board[i][j + 1]:
                    return False
                if self.board[j][i] == self.board[j + 1][i]:
                    return False
        return True

    def game_over(self):
        game_over_label = tk.Label(self.frame, text="Game Over!", font=("Helvetica", 24), bg="red")
        game_over_label.grid(row=2, column=0, columnspan=5, pady=10)

    def on_key_press(self, event):
        key_mapping = {
            "Left": "left",
            "Right": "right",
            "Up": "up",
            "Down": "down",
        }
        if event.keysym in key_mapping:
            self.move(key_mapping[event.keysym])

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
