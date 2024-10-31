import tkinter as tk
import time

BOARD_SIZE = 9
CELL_SIZE = 60

# 当前操作模式 ("move_piece" 表示移动棋子, 'place_horizontal_wall' 表示放置横向墙, 'place_vertical_wall' 表示放置竖向墙)
current_mode = "move_piece"

# 当前玩家
player = "red"

# 当前玩家能走的所有位置以及对应对象的 id
reachable_positions = set()

# 四个可走方向，依次为上下左右
dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# 墙 (row, col, dir)
walls = {(row, col) : [0, 0, 0, 0] for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)}

# 画布上的墙
canvas_walls = []

# 每个玩家剩余墙数量
remain_walls = {"red" : 10, "blue": 10}

# 游戏结束文字
game_over_text = None

root = tk.Tk()
root.title("Quoridor")
root.geometry("200x100")

# 开始界面
start_frame = tk.Frame(root)
button_start_game = tk.Button(start_frame, text="开始游戏！", command=lambda: show_main_frame())
button_start_game.pack(padx=30, pady=30)

# 主界面
main_frame = tk.Frame(root)

# 棋盘 
chess_board = tk.Frame(main_frame)
chess_board.pack(padx = 20, pady = 20)


# 标行号
row_canvas = tk.Canvas(chess_board, width=CELL_SIZE // 2, height=BOARD_SIZE * CELL_SIZE)
row_canvas.grid(row=0,column=0)

for row in range(BOARD_SIZE):
    row_canvas.create_text(CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 2, text=f"{row + 1}", font=("Arial", 12))

# 标列号
col_canvas = tk.Canvas(chess_board, width=BOARD_SIZE * CELL_SIZE, height=CELL_SIZE // 2)
col_canvas.grid(row=1,column=1)

for col in range(BOARD_SIZE):
    col_canvas.create_text(col * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 4, text=f"{chr(col + 65)}", font=("Arial", 12))

canvas = tk.Canvas(chess_board, width=BOARD_SIZE * CELL_SIZE, height=BOARD_SIZE * CELL_SIZE)
canvas.grid(row=0,column=1)

# 添加棋盘
for row in range(BOARD_SIZE):
    for col in range(BOARD_SIZE):
        x1 = row * CELL_SIZE
        y1 = col * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        if col == 0:
            canvas.create_rectangle(x1, y1, x2, y2, width=2, fill="skyblue",outline="black")
        elif col == BOARD_SIZE - 1:
            canvas.create_rectangle(x1, y1, x2, y2, width=2, fill="lightsalmon",outline="black")
        else:
            canvas.create_rectangle(x1, y1, x2, y2, width=2, fill="white",outline="black")

canvas.create_line(0, 3, CELL_SIZE * BOARD_SIZE, 3, fill="black", width=2)
canvas.create_line(3, 0, 3, CELL_SIZE * BOARD_SIZE, fill="black", width=2)

# 在 (row, col) 处绘制颜色为 color 的圆圈
def draw_circle(row, col, color, tag):
    x = row * CELL_SIZE
    y = col * CELL_SIZE
    return canvas.create_oval(y + 10, x + 10, y + CELL_SIZE - 10, x + CELL_SIZE - 10, fill=color,outline=color, tag=tag)

# 添加棋子
piece_red = draw_circle(0, BOARD_SIZE // 2, "red", "piece")
piece_blue = draw_circle(BOARD_SIZE - 1, BOARD_SIZE // 2, "blue", "piece")

# 获取圆圈的当前格子位置
def get_circle_grid_position(piece):
    x1, y1, x2, y2 = canvas.coords(piece)  
    col = int(x1 // CELL_SIZE)
    row = int(y1 // CELL_SIZE)
    return row, col

# 判断红色，蓝色棋子是否相邻
def is_neighbor():
    red_row, red_col = get_circle_grid_position(piece_red)
    blue_row, blue_col = get_circle_grid_position(piece_blue)
    for i in range(4):
        if walls[(red_row, red_col)][i]:
            continue
        if red_row + dir[i][0] == blue_row and red_col + dir[i][1] == blue_col:
            return True
    return False

# 求出所有当前棋子可以移动的位置
def get_reachable_positions():
    global reachable_positions
    reachable_positions = set()
    red_row, red_col = get_circle_grid_position(piece_red)
    blue_row, blue_col = get_circle_grid_position(piece_blue)
    if is_neighbor() or player == "red":
        for i in range(4):
            if red_row + dir[i][0] == blue_row and red_col + dir[i][1] == blue_col:
                continue
            if walls[(red_row, red_col)][i]:
                continue
            if 0 <= red_row + dir[i][0] < BOARD_SIZE and 0 <= red_col + dir[i][1] < BOARD_SIZE:
                reachable_positions.add((red_row + dir[i][0], red_col + dir[i][1]))
    if is_neighbor() or player == "blue":
        for i in range(4):
            if walls[(blue_row, blue_col)][i]:
                continue
            if blue_row + dir[i][0] == red_row and blue_col + dir[i][1] == red_col:
                continue
            if 0 <= blue_row + dir[i][0] < BOARD_SIZE and 0 <= blue_col + dir[i][1] < BOARD_SIZE:
                reachable_positions.add((blue_row + dir[i][0], blue_col + dir[i][1]))
    for position in reachable_positions:
        if player == "red":
            draw_circle(position[0], position[1], "salmon", "preview_piece")
        else:
            draw_circle(position[0], position[1], "deepskyblue", "preview_piece")
    return reachable_positions
            
# 控制面板
control_board = tk.Frame(main_frame)
control_board.pack(side="bottom", pady = 30)

# 显示当前模式
label_now_mode = tk.Label(main_frame, text="当前模式：移动")
label_now_mode.pack(padx=50)

# 墙放置模式选择
button_place_horizontal_wall = tk.Button(control_board, text="放置横向墙", command=lambda: set_mode("place_horizontal_wall"))
button_place_horizontal_wall.grid(row=0, column=0)

button_place_vertical_wall = tk.Button(control_board, text="放置竖向墙", command=lambda: set_mode("place_vertical_wall"))
button_place_vertical_wall.grid(row=0, column=1)

# 移动模式选择
button_move_mode = tk.Button(control_board, text="移动", command=lambda: set_mode("move_piece"))
button_move_mode.grid(row=0, column=2)

# 显示当前玩家
label_now_player = tk.Label(main_frame, text="当前玩家：红色", fg="red")
label_now_player.pack(padx=50)

# 显示每个玩家剩余墙的数量
label_red_remain_walls = tk.Label(main_frame, text=f"红色剩余墙数量：{remain_walls['red']}", fg="red")
label_red_remain_walls.pack(side="left", padx=50)
label_blue_remain_walls = tk.Label(main_frame, text=f"蓝色剩余墙数量：{remain_walls['blue']}", fg="blue")
label_blue_remain_walls.pack(side="right", padx=50)

# 改变当前玩家函数
def change_player():
    global player
    player = "red" if player == "blue" else "blue"
    if player == "red":
        label_now_player.config(text="当前玩家：红色", fg="red")
    else:
        label_now_player.config(text="当前玩家：蓝色", fg="blue")
    set_mode("move_piece")

# 选择模式函数
def set_mode(mode):
    global current_mode
    current_mode = mode
    if current_mode == "move_piece":
        label_now_mode.config(text="当前模式：移动")
    elif current_mode == "place_horizontal_wall":
        label_now_mode.config(text="当前模式：放置横向墙")
    else:
        label_now_mode.config(text="当前模式：放置竖向墙")
    if current_mode != "move_piece":
        canvas.delete("preview_piece")
    else:
        canvas.delete("preview_wall")
        get_reachable_positions()

# 判断游戏是否结束
def is_end():
    red_row, red_col = get_circle_grid_position(piece_red)
    blue_row, blue_col = get_circle_grid_position(piece_blue)
    if red_row == BOARD_SIZE - 1:
        return True
    if blue_row == 0:
        return True
    return False

# 移动棋子并检验是否可以移动
def move_piece(event):
    if current_mode != "move_piece":
        return
    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE
    if (row, col) not in reachable_positions:
        return
    canvas.delete("preview_piece")
    now_peice = piece_red if player == "red" else piece_blue
    canvas.coords(now_peice, col * CELL_SIZE + 10, row * CELL_SIZE + 10, (col + 1) * CELL_SIZE - 10, (row + 1) * CELL_SIZE - 10)
    if is_end():
        game_end()
        return
    change_player()

# 判断当前棋子是否能走到终点
def can_reach_end(piece):
    q = [get_circle_grid_position(piece)]
    vis = set(q[0])
    while len(q) > 0:
        row, col = q.pop()
        if piece == piece_red:
            if row == BOARD_SIZE - 1:
                return True
        else:
            if row == 0:
                return True
        for i in range(4):
            if walls[(row, col)][i]:
                continue
            new_row = row + dir[i][0]
            new_col = col + dir[i][1]
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                if (new_row, new_col) not in vis:
                    vis.add((new_row, new_col))
                    q.append((new_row, new_col))
    return False

# 判断当前墙能否放置
def check_place_wall(x, y):
    if current_mode == "move_piece":
        return False
    if remain_walls[player] == 0:
        return False
    if current_mode == "place_horizontal_wall":
        row = (y + CELL_SIZE // 2) // CELL_SIZE
        col = (x - CELL_SIZE // 2) // CELL_SIZE
        if not(0 < row < BOARD_SIZE and 0 <= col < BOARD_SIZE - 1):
            return False
        if walls[(row, col)][0] or walls[(row, col + 1)][0] or (walls[(row - 1, col + 1)][2] and walls[(row, col + 1)][2]):
            return False
        walls[(row, col)][0] = 1
        walls[(row - 1, col)][1] = 1
        walls[(row, col + 1)][0] = 1
        walls[(row - 1, col + 1)][1] = 1
        flag = can_reach_end(piece_red) and can_reach_end(piece_blue)
        walls[(row, col)][0] = 0
        walls[(row - 1, col)][1] = 0
        walls[(row, col + 1)][0] = 0
        walls[(row - 1, col + 1)][1] = 0
        return flag
    else:
        row = (y - CELL_SIZE // 2) // CELL_SIZE
        col = (x + CELL_SIZE // 2) // CELL_SIZE
        if not(0 <= row < BOARD_SIZE - 1 and 0 < col < BOARD_SIZE):
            return False
        if (walls[(row + 1, col - 1)][0] and walls[(row + 1, col)][0]) or walls[(row, col)][2] or walls[(row + 1, col)][2]:
            return False
        walls[(row, col)][2] = 1
        walls[(row, col - 1)][3] = 1
        walls[(row + 1, col)][2] = 1
        walls[(row + 1, col - 1)][3] = 1
        flag = can_reach_end(piece_red) and can_reach_end(piece_blue)
        walls[(row, col)][2] = 0
        walls[(row, col - 1)][3] = 0
        walls[(row + 1, col)][2] = 0
        walls[(row + 1, col - 1)][3] = 0
        return flag

# 放置墙的提示函数
def show_wall_preview(event):
    x, y = event.x, event.y
    canvas.delete("preview_wall")
    if not check_place_wall(x, y):
        return
    # 先清除之前的提示
    # 根据当前模式显示墙的位置
    if current_mode == "place_horizontal_wall":
        row = (y + CELL_SIZE // 2) // CELL_SIZE
        col = (x - CELL_SIZE // 2) // CELL_SIZE
        canvas.create_line(
            col * CELL_SIZE, row * CELL_SIZE,
            (col + 2) * CELL_SIZE, row * CELL_SIZE, width=5, fill="gray", tags="preview_wall"
        )
    elif current_mode == "place_vertical_wall":
        row = (y - CELL_SIZE // 2) // CELL_SIZE
        col = (x + CELL_SIZE // 2) // CELL_SIZE
        canvas.create_line(
            col * CELL_SIZE, row * CELL_SIZE,
            col * CELL_SIZE, (row + 2) * CELL_SIZE, width=5, fill="gray", tags="preview_wall"
        )

# 放置横向墙
def place_horizontal_wall(event):
    global remain_walls
    x, y = event.x, event.y
    if not check_place_wall(x, y) or current_mode != "place_horizontal_wall":
        return
    row = (y + CELL_SIZE // 2) // CELL_SIZE
    col = (x - CELL_SIZE // 2) // CELL_SIZE
    walls[(row, col)][0] = 1
    walls[(row - 1, col)][1] = 1
    walls[(row, col + 1)][0] = 1
    walls[(row - 1, col + 1)][1] = 1
    canvas_walls.append(canvas.create_line(
        col * CELL_SIZE, row * CELL_SIZE,
        (col + 2) * CELL_SIZE, row * CELL_SIZE, width=10, fill="black"
    ))
    remain_walls[player] -= 1
    if player == "red":
        label_red_remain_walls.config(text=f"红色剩余墙数量：{remain_walls['red']}", fg="red")
    else:
        label_blue_remain_walls.config(text=f"蓝色剩余墙数量：{remain_walls['blue']}", fg="blue")
    change_player()

# 放置竖向墙
def place_vertical_wall(event):
    global remain_walls
    x, y = event.x, event.y
    if not check_place_wall(x, y) or current_mode != "place_vertical_wall":
        return
    row = (y - CELL_SIZE // 2) // CELL_SIZE
    col = (x + CELL_SIZE // 2) // CELL_SIZE
    walls[(row, col)][2] = 1
    walls[(row, col - 1)][3] = 1
    walls[(row + 1, col)][2] = 1
    walls[(row + 1, col - 1)][3] = 1
    canvas_walls.append(canvas.create_line(
        col * CELL_SIZE, row * CELL_SIZE,
        col * CELL_SIZE, (row + 2) * CELL_SIZE, width=10, fill="black"
    ))
    remain_walls[player] -= 1
    if player == "red":
        label_red_remain_walls.config(text=f"红色剩余墙数量：{remain_walls['red']}", fg="red")
    else:
        label_blue_remain_walls.config(text=f"蓝色剩余墙数量：{remain_walls['blue']}", fg="blue")
    change_player()

def handle_event(event):
    if current_mode == "move_piece":
        move_piece(event)
    elif current_mode == "place_horizontal_wall":
        place_horizontal_wall(event)
    elif current_mode == "place_vertical_wall":
        place_vertical_wall(event)


# 绑定鼠标与事件
canvas.bind("<Button-1>", handle_event)
canvas.bind("<Motion>", show_wall_preview)

button_restart = tk.Button(main_frame, text="重新开始", command=lambda: reset())
button_restart.pack()

def reset():
    global current_mode, player, reachable_positions, walls, remain_walls, canvas_walls, piece_red, piece_blue, game_over_text
    current_mode = "move_piece"
    player = "red"
    reachable_positions = set()
    walls = {(row, col) : [0, 0, 0, 0] for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)}
    remain_walls = {"red" : 10, "blue": 10}
    canvas.delete("preview_piece")
    for wall in canvas_walls:
        canvas.delete(wall)
    canvas_walls = []
    canvas.coords(piece_red, 4 * CELL_SIZE + 10, 10, 5 * CELL_SIZE - 10, CELL_SIZE - 10)
    canvas.coords(piece_blue, 4 * CELL_SIZE + 10, 8 * CELL_SIZE + 10, 5 * CELL_SIZE - 10, 9 * CELL_SIZE - 10)
    label_red_remain_walls.config(text=f"红色剩余墙数量：{remain_walls['red']}", fg="red")
    label_blue_remain_walls.config(text=f"蓝色剩余墙数量：{remain_walls['blue']}", fg="blue")
    if game_over_text:
        canvas.delete(game_over_text)
    enable_button()
    get_reachable_positions()

# 显示目标 Frame 的函数
def show_start_frame():
    start_frame.pack(fill="both", expand=True) 

def show_main_frame():
    start_frame.pack_forget()  
    main_frame.pack(fill="both", expand=True)  
    root.geometry("700x800")
    reset()

show_start_frame()

# 禁用按钮
def disable_button():
    button_move_mode.config(state="disabled")
    button_place_horizontal_wall.config(state="disabled")
    button_place_vertical_wall.config(state="disabled")

# 启用按钮
def enable_button():
    button_move_mode.config(state="normal")
    button_place_horizontal_wall.config(state="normal")
    button_place_vertical_wall.config(state="normal")

# 游戏结束
def game_end():
    global game_over_text
    disable_button()
    root.after(300, lambda: None)
    game_over_text = canvas.create_text(270, 250, text=f"{player} wins!", font=("Arial", 50), anchor="center", fill=player)

root.mainloop()
