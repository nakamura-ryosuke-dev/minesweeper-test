import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, master, rows=10, cols=10, mines=15):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = []
        self.mines_positions = []
        self.flags = 0
        self.game_over = False
        
        master.title("マインスイーパー")
        master.resizable(False, False)
        
        self.top_frame = tk.Frame(master)
        self.top_frame.pack(fill="x")
        
        self.mine_counter_label = tk.Label(self.top_frame, text=f"残り地雷: {self.mines - self.flags}", font=("Arial", 12))
        self.mine_counter_label.pack(side="left", padx=10, pady=5)
        
        self.reset_button = tk.Button(self.top_frame, text="リセット", command=self.reset_game)
        self.reset_button.pack(side="right", padx=10, pady=5)
        
        self.frame = tk.Frame(master)
        self.frame.pack()
        
        self.create_grid()
        
        self.place_mines()

    def create_grid(self):
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                button = tk.Button(self.frame, width=2, height=1, font=("Arial", 10, "bold"))
                button.grid(row=i, column=j)
                button.bind("<Button-1>", lambda event, r=i, c=j: self.click(r, c))
                button.bind("<Button-3>", lambda event, r=i, c=j: self.right_click(r, c))
                button.config(bg="lightgray", relief="raised")
                button.is_mine = False
                button.is_flagged = False
                button.is_revealed = False
                button.adjacent_mines = 0
                row.append(button)
            self.buttons.append(row)

    def place_mines(self):
        positions = [(i, j) for i in range(self.rows) for j in range(self.cols)]
        self.mines_positions = random.sample(positions, self.mines)
        
        for i, j in self.mines_positions:
            self.buttons[i][j].is_mine = True
            
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.buttons[i][j].is_mine:
                    adjacent_mines = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if 0 <= ni < self.rows and 0 <= nj < self.cols and self.buttons[ni][nj].is_mine:
                                adjacent_mines += 1
                    self.buttons[i][j].adjacent_mines = adjacent_mines

    def click(self, row, col):
        if self.game_over or self.buttons[row][col].is_flagged or self.buttons[row][col].is_revealed:
            return
        
        button = self.buttons[row][col]
        
        if button.is_mine:
            self.reveal_all_mines()
            messagebox.showinfo("ゲームオーバー", "地雷を踏んでしまいました！")
            self.game_over = True
            return
        
        self.reveal_cell(row, col)
        
        self.check_win()

    def reveal_cell(self, row, col):
        button = self.buttons[row][col]
        
        if button.is_revealed or button.is_flagged:
            return
        
        button.is_revealed = True
        button.config(relief="sunken", bg="white")
        
        if button.adjacent_mines > 0:
            colors = ["blue", "green", "red", "purple", "maroon", "turquoise", "black", "gray"]
            button.config(text=str(button.adjacent_mines), fg=colors[button.adjacent_mines-1])
        else:
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    ni, nj = row + di, col + dj
                    if 0 <= ni < self.rows and 0 <= nj < self.cols:
                        self.reveal_cell(ni, nj)

    def right_click(self, row, col):
        if self.game_over or self.buttons[row][col].is_revealed:
            return
        
        button = self.buttons[row][col]
        
        if button.is_flagged:
            button.is_flagged = False
            button.config(text="", bg="lightgray")
            self.flags -= 1
        else:
            button.is_flagged = True
            button.config(text="🚩", fg="red", bg="#d3d3d3")
            self.flags += 1
        
        self.mine_counter_label.config(text=f"残り地雷: {self.mines - self.flags}")
        
        self.check_win()

    def reveal_all_mines(self):
        for i, j in self.mines_positions:
            if not self.buttons[i][j].is_flagged:
                self.buttons[i][j].config(text="💣", bg="red")
        
        for i in range(self.rows):
            for j in range(self.cols):
                if self.buttons[i][j].is_flagged and not self.buttons[i][j].is_mine:
                    self.buttons[i][j].config(text="❌", bg="orange")

    def check_win(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.buttons[i][j].is_mine and not self.buttons[i][j].is_revealed:
                    return
        
        self.game_over = True
        messagebox.showinfo("おめでとう！", "ゲームクリア！")
        
        for i, j in self.mines_positions:
            if not self.buttons[i][j].is_flagged:
                self.buttons[i][j].config(text="🚩", fg="red")

    def reset_game(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].destroy()
        
        self.buttons = []
        self.mines_positions = []
        self.flags = 0
        self.game_over = False
        
        self.mine_counter_label.config(text=f"残り地雷: {self.mines}")
        
        self.create_grid()
        
        self.place_mines()

def set_difficulty(root):
    difficulty_window = tk.Toplevel(root)
    difficulty_window.title("難易度選択")
    difficulty_window.resizable(False, False)
    difficulty_window.grab_set()  # Modal window
    
    tk.Label(difficulty_window, text="難易度を選択してください:", font=("Arial", 12)).pack(pady=10)
    
    difficulties = [
        ("初級", 9, 9, 10),
        ("中級", 16, 16, 40),
        ("上級", 16, 30, 99)
    ]
    
    for name, rows, cols, mines in difficulties:
        tk.Button(
            difficulty_window, 
            text=f"{name} ({rows}x{cols}, 地雷{mines}個)",
            width=20,
            command=lambda r=rows, c=cols, m=mines: start_game(root, difficulty_window, r, c, m)
        ).pack(pady=5)
    
    custom_frame = tk.Frame(difficulty_window)
    custom_frame.pack(pady=10)
    
    tk.Label(custom_frame, text="行:").grid(row=0, column=0)
    rows_entry = tk.Entry(custom_frame, width=5)
    rows_entry.grid(row=0, column=1)
    rows_entry.insert(0, "10")
    
    tk.Label(custom_frame, text="列:").grid(row=0, column=2)
    cols_entry = tk.Entry(custom_frame, width=5)
    cols_entry.grid(row=0, column=3)
    cols_entry.insert(0, "10")
    
    tk.Label(custom_frame, text="地雷:").grid(row=0, column=4)
    mines_entry = tk.Entry(custom_frame, width=5)
    mines_entry.grid(row=0, column=5)
    mines_entry.insert(0, "15")
    
    def start_custom_game():
        try:
            rows = int(rows_entry.get())
            cols = int(cols_entry.get())
            mines = int(mines_entry.get())
            
            if rows < 5 or cols < 5:
                messagebox.showwarning("警告", "行と列は5以上にしてください")
                return
                
            if mines < 1:
                messagebox.showwarning("警告", "地雷は1個以上にしてください")
                return
                
            if mines >= rows * cols:
                messagebox.showwarning("警告", "地雷の数が多すぎます")
                return
                
            start_game(root, difficulty_window, rows, cols, mines)
        except ValueError:
            messagebox.showwarning("警告", "数値を入力してください")
    
    tk.Button(custom_frame, text="カスタム開始", command=start_custom_game).grid(row=0, column=6, padx=5)

def start_game(root, difficulty_window, rows, cols, mines):
    for widget in root.winfo_children():
        widget.destroy()
    
    difficulty_window.destroy()
    
    game = Minesweeper(root, rows, cols, mines)

def main():
    root = tk.Tk()
    root.title("マインスイーパー")
    
    
    set_difficulty(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
