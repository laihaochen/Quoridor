import tkinter as tk
from tkinter import scrolledtext
from game_logic import *
from PIL import Image, ImageTk

CELL_SIZE = 60

class QuoridorUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.red_pawn_image = Image.open("images/ustc_red.png")
        self.red_pawn_image = self.red_pawn_image.resize((CELL_SIZE - 10, CELL_SIZE - 10))
        self.red_pawn_image = ImageTk.PhotoImage(self.red_pawn_image)
        self.blue_pawn_image = Image.open("images/ustc_blue.png")
        self.blue_pawn_image = self.blue_pawn_image.resize((CELL_SIZE - 10, CELL_SIZE - 10))
        self.blue_pawn_image = ImageTk.PhotoImage(self.blue_pawn_image)
        self.current_mode = "move_pawn"
        self.ai_first = 0
        self.in_main_frame = 0 
        self.canvas_walls = [] # 画布上的墙
        self.game_over_text = None # 游戏结束文字
        self.draw_start_frame()
        self.main_frame = tk.Frame(root)
        self.draw_canvas()
        self.draw_board()
        self.draw_pawn()
        self.draw_control_board()

    def reset(self):
        self.game.reset()
        self.current_mode = "move_pawn"
        self.canvas.delete("preview_pawn")
        for wall in self.canvas_walls:
            self.canvas.delete(wall)
        self.canvas_walls = []
        self.canvas.coords(self.pawn_red, 4 * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 2)
        self.canvas.coords(self.pawn_blue, 4 * CELL_SIZE + CELL_SIZE // 2, 8 * CELL_SIZE + CELL_SIZE // 2)
        if self.game_over_text:
            self.canvas.delete(self.game_over_text)
            self.game_over_text = None
        self.enable_button()
        self.draw_reachable_positions()

    def set_ai_mode(self):
        self.ai_first += 1
        if self.ai_first == 2:
            self.ai_first -= 3
        if self.ai_first == 0:
            self.button_ai_mode.config(text="当前AI模式：没有 AI")
        elif self.ai_first == 1:
            self.button_ai_mode.config(text="当前AI模式：AI 先手")
        else:
            self.button_ai_mode.config(text="当前AI模式：AI 后手")

    def draw_start_frame(self):
        self.start_frame = tk.Frame(self.root)

        # 创建带滚动条的文本框
        self.text_area = scrolledtext.ScrolledText(self.start_frame, wrap=tk.WORD, width=60, height=20, font=("Arial", 12))
        self.text_area.pack(padx=10, pady=10, fill="both", expand=True)

        long_text1 = """
        游戏胜利目标很简单，将自己的棋子，移动到对面的底线即可。第一个到达对面的玩家胜利。
        
        放置墙壁：每个墙壁长度为2，用于放在格子之间，可以阻挡棋子通行。
        墙壁可以竖着放，也可以横着放。墙壁不可以垂直交叉放置（成为一个➕形状），同一方向的墙壁不能重叠放置。
        
        下图有1个水平墙壁和1个竖直墙壁：

        """
        self.text_area.insert(tk.END, long_text1)

        example_image1 = Image.open("images/example_image1.png")  
        example_image1 = example_image1.resize((200, 200), Image.Resampling.LANCZOS)  
        self.photo_example_image1 = ImageTk.PhotoImage(example_image1) 

        self.text_area.image_create(tk.END, image=self.photo_example_image1)

        long_text2 = """

        放置墙壁后，墙壁在本局游戏中都不能被移动、拆除，任何人都不能跨越墙壁移动。
        放置墙壁时，不能封死任何一名玩家的路线，需要保证放置墙壁后，每个玩家都至少有一条通路到达对面底线。

        移动棋子：棋子可以上下左右移动一个格子。
        当相邻一格是敌人的棋子时，可以跳过去，移动到敌人棋子的旁边一格空地（只能跳一次），跳跃时，依然无法跨越墙壁。
        
        如下图，蓝色棋子本回合可以移动到6个位置之一。

        """
        self.text_area.insert(tk.END, long_text2)

        example_image2 = Image.open("images/example_image2.png") 
        example_image2 = example_image2.resize((200, 200), Image.Resampling.LANCZOS)  
        self.photo_example_image2 = ImageTk.PhotoImage(example_image2)

        self.text_area.image_create(tk.END, image=self.photo_example_image2)
        
        self.text_area.config(state="disabled")

        self.button_ai_mode = tk.Button(self.start_frame, text=f"当前AI模式：没有 AI", command=lambda: self.set_ai_mode())
        self.button_ai_mode.pack(side="left", padx=150, pady=20)
        self.button_start_game = tk.Button(self.start_frame, text="开始游戏！", command=lambda: self.show_init_main_frame())
        self.button_start_game.pack(side="right", padx=150, pady=20)
        self.start_frame.pack(fill="both", expand=True) 
    
    def show_init_main_frame(self):
        self.start_frame.pack_forget()  
        self.main_frame.pack(fill="both", expand=True)  
        self.root.geometry("700x800")
        self.reset()
        self.in_main_frame = 1

    def draw_canvas(self):
        # 棋盘 
        self.chess_board = tk.Frame(self.main_frame)
        self.chess_board.pack(padx = 20, pady = 20)
        
        # 标行号
        self.row_index = tk.Canvas(self.chess_board, width=CELL_SIZE // 2, height=BOARD_SIZE * CELL_SIZE)
        self.row_index.grid(row=0,column=0)

        for row in range(BOARD_SIZE):
            self.row_index.create_text(CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 2, text=f"{row + 1}", font=("Arial", 12))

        # 标列号
        self.col_index = tk.Canvas(self.chess_board, width=BOARD_SIZE * CELL_SIZE, height=CELL_SIZE // 2)
        self.col_index.grid(row=1,column=1)

        for col in range(BOARD_SIZE):
            self.col_index.create_text(col * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 4, text=f"{chr(col + 65)}", font=("Arial", 12))

        self.canvas = tk.Canvas(self.chess_board, width=BOARD_SIZE * CELL_SIZE, height=BOARD_SIZE * CELL_SIZE)
        self.canvas.grid(row=0,column=1)

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = row * CELL_SIZE
                y1 = col * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                if col == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, width=2, fill="skyblue", outline="black")
                elif col == BOARD_SIZE - 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, width=2, fill="lightsalmon", outline="black")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, width=2, fill="white", outline="black")

        self.canvas.create_line(0, 3, CELL_SIZE * BOARD_SIZE, 3, fill="black", width=2)
        self.canvas.create_line(3, 0, 3, CELL_SIZE * BOARD_SIZE, fill="black", width=2)

    def draw_circle(self, row, col, color, tag):
        x = row * CELL_SIZE
        y = col * CELL_SIZE
        return self.canvas.create_oval(y + 10, x + 10, y + CELL_SIZE - 10, x + CELL_SIZE - 10, fill=color,outline=color, tag=tag)

    def load_pawn_picture(self, row, col, color):
        x = row * CELL_SIZE
        y = col * CELL_SIZE
        image = self.blue_pawn_image if color == "blue" else self.red_pawn_image
        return self.canvas.create_image(y + CELL_SIZE // 2, x + CELL_SIZE // 2, image=image, anchor="center")
    
    def draw_pawn(self):
        self.pawn_red = self.load_pawn_picture(0, BOARD_SIZE // 2, "red")
        self.pawn_blue = self.load_pawn_picture(BOARD_SIZE - 1, BOARD_SIZE // 2, "blue")
        
    def draw_control_board(self):
        # 控制面板
        self.control_board = tk.Frame(self.main_frame)
        self.control_board.pack(side="bottom", pady = 30)

        # 显示当前模式
        self.label_now_mode = tk.Label(self.main_frame, text="当前模式：移动")
        self.label_now_mode.pack(padx=50)

        # 墙放置模式选择
        self.button_build_horizontal_wall = tk.Button(self.control_board, text="放置横向墙", command=lambda: self.set_mode("build_horizontal_wall"))
        self.button_build_horizontal_wall.grid(row=0, column=0)

        self.button_build_vertical_wall = tk.Button(self.control_board, text="放置竖向墙", command=lambda: self.set_mode("build_vertical_wall"))
        self.button_build_vertical_wall.grid(row=0, column=1)

        # 移动模式选择
        self.button_move_mode = tk.Button(self.control_board, text="移动", command=lambda: self.set_mode("move_pawn"))
        self.button_move_mode.grid(row=0, column=2)

        # 显示当前玩家
        self.label_now_player = tk.Label(self.main_frame, text="当前玩家：红色", fg="red")
        self.label_now_player.pack(padx=50)

        # 显示每个玩家剩余墙的数量
        self.label_red_remain_walls = tk.Label(self.main_frame, text=f"红色剩余墙数量：{self.game.remain_walls['red']}", fg="red")
        self.label_red_remain_walls.pack(side="left", padx=20, pady=10)
        self.label_blue_remain_walls = tk.Label(self.main_frame, text=f"蓝色剩余墙数量：{self.game.remain_walls['blue']}", fg="blue")
        self.label_blue_remain_walls.pack(side="right", padx=20, pady=10)

        # 绑定鼠标与事件
        self.canvas.bind("<Button-1>", self.get_action_from_mouse)
        self.canvas.bind("<Motion>", self.show_wall_preview)

        button_restart = tk.Button(self.main_frame, text="重新开始", command=lambda: self.reset())
        button_restart.pack()

    def draw_reachable_positions(self):
        reachable_positions = self.game.get_reachable_positions()
        for position in reachable_positions:
            if self.game.player == "red":
                self.draw_circle(position[0], position[1], "salmon", "preview_pawn")
            else:
                self.draw_circle(position[0], position[1], "deepskyblue", "preview_pawn")

    # 选择模式函数
    def set_mode(self, mode):
        self.current_mode = mode
        if self.current_mode == "move_pawn":
            self.label_now_mode.config(text="当前模式：移动")
        elif self.current_mode == "build_horizontal_wall":
            self.label_now_mode.config(text="当前模式：放置横向墙")
        else:
            self.label_now_mode.config(text="当前模式：放置竖向墙")
        if self.current_mode != "move_pawn":
            self.canvas.delete("preview_pawn")
        else:
            self.canvas.delete("preview_wall")
            self.draw_reachable_positions()

    # 改变当前玩家函数
    def change_player(self):
        self.game.change_player()
        if self.game.player == "red":
            self.label_now_player.config(text="当前玩家：红色", fg="red")
        else:
            self.label_now_player.config(text="当前玩家：蓝色", fg="blue")
        self.label_red_remain_walls.config(text=f"红色剩余墙数量：{self.game.remain_walls['red']}", fg="red")
        self.label_blue_remain_walls.config(text=f"蓝色剩余墙数量：{self.game.remain_walls['blue']}", fg="blue")
        self.set_mode("move_pawn")

    # 禁用按钮
    def disable_button(self):
        self.button_move_mode.config(state="disabled")
        self.button_build_horizontal_wall.config(state="disabled")
        self.button_build_vertical_wall.config(state="disabled")

    # 启用按钮
    def enable_button(self):
        self.button_move_mode.config(state="normal")
        self.button_build_horizontal_wall.config(state="normal")
        self.button_build_vertical_wall.config(state="normal")

    # 游戏结束
    def game_end(self):
        self.disable_button()
        self.root.after(300, lambda: None)
        text = "红方胜利！" if self.game.player == "red" else "蓝方胜利！"
        self.game_over_text = self.canvas.create_text(270, 250, text=text, font=("Arial", 50), anchor="center", fill=self.game.player)
    
    # 放置墙的提示函数
    def show_wall_preview(self, event):
        x, y = event.x, event.y
        self.canvas.delete("preview_wall")
        # 先清除之前的提示
        # 根据当前模式显示墙的位置
        if self.current_mode == "build_horizontal_wall":
            row = (y + CELL_SIZE // 2) // CELL_SIZE
            col = (x - CELL_SIZE // 2) // CELL_SIZE
            if self.game.check_build_horizontal_wall(row, col):
                self.canvas.create_line(
                    col * CELL_SIZE, row * CELL_SIZE,
                    (col + 2) * CELL_SIZE, row * CELL_SIZE, width=5, fill="gray", tags="preview_wall"
                )
        elif self.current_mode == "build_vertical_wall":
            row = (y - CELL_SIZE // 2) // CELL_SIZE
            col = (x + CELL_SIZE // 2) // CELL_SIZE
            if self.game.check_build_vertical_wall(row, col):
                self.canvas.create_line(
                    col * CELL_SIZE, row * CELL_SIZE,
                    col * CELL_SIZE, (row + 2) * CELL_SIZE, width=5, fill="gray", tags="preview_wall"
                )
    
    def move_pawn(self, row, col):
        now_peice = self.pawn_red if self.game.player == "red" else self.pawn_blue
        if self.game.move_pawn(row, col):
            self.canvas.delete("preview_pawn")
            self.canvas.coords(now_peice, col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
            return True
        return False

    def mouse_move_pawn_action(self, event):
        if self.game.is_end():
            return None
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        return row * BOARD_SIZE + col

    def build_horizontal_wall(self, row, col):
        if self.game.build_horizontal_wall(row, col):
            self.canvas_walls.append(self.canvas.create_line(
                col * CELL_SIZE, row * CELL_SIZE,
                (col + 2) * CELL_SIZE, row * CELL_SIZE, width=10, fill="black"
            ))
            return True
        return False

    def mouse_build_horizontal_wall_action(self, event):
        x, y = event.x, event.y
        row = (y + CELL_SIZE // 2) // CELL_SIZE
        col = (x - CELL_SIZE // 2) // CELL_SIZE
        return BOARD_SIZE * BOARD_SIZE + row * BOARD_SIZE + col
    
    def build_vertical_wall(self, row, col):
        if self.game.build_vertical_wall(row, col):
            self.canvas_walls.append(self.canvas.create_line(
                col * CELL_SIZE, row * CELL_SIZE,
                col * CELL_SIZE, (row + 2) * CELL_SIZE, width=10, fill="black"
            ))
            return True
        return False

    def mouse_build_vertical_wall_action(self, event):
        x, y = event.x, event.y
        row = (y - CELL_SIZE // 2) // CELL_SIZE
        col = (x + CELL_SIZE // 2) // CELL_SIZE
        return 2 * BOARD_SIZE * BOARD_SIZE + row * BOARD_SIZE + col

    def get_action_from_mouse(self, event):
        current_player = 1 if self.game.player == "red" else -1
        if self.ai_first != 0 and current_player == self.ai_first:
            return
        action = None
        if self.current_mode == "move_pawn":
            action = self.mouse_move_pawn_action(event)
        elif self.current_mode == "build_horizontal_wall":
            action = self.mouse_build_horizontal_wall_action(event)
        elif self.current_mode == "build_vertical_wall":
            action = self.mouse_build_vertical_wall_action(event)
        self.get_next_game(action)

    def get_next_game(self, action):
        if action == None:
            return
        successful_move = None
        if action < BOARD_SIZE * BOARD_SIZE:
            self.set_mode("move_pawn")
            row = action // BOARD_SIZE
            col = action % BOARD_SIZE
            successful_move = self.move_pawn(row, col)
        elif action < 2 * BOARD_SIZE * BOARD_SIZE:
            self.set_mode("build_horizontal_wall")
            action -= BOARD_SIZE * BOARD_SIZE
            row = action // BOARD_SIZE
            col = action % BOARD_SIZE
            successful_move = self.build_horizontal_wall(row, col)
        else:
            self.set_mode("build_vertical_wall")
            action -= 2 * BOARD_SIZE * BOARD_SIZE
            row = action // BOARD_SIZE
            col = action % BOARD_SIZE
            successful_move = self.build_vertical_wall(row, col)
        if self.game.is_end():
            self.game_end()
        if successful_move:
            self.change_player()
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quoridor")
    root.geometry("900x600")

    game = QuoridorGame()
    UI = QuoridorUI(root, game)
    UI.root.mainloop()