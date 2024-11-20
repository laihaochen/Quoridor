BOARD_SIZE = 9
dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class QuoridorGame:
    def __init__(self):
        self.player = "red" # 当前玩家
        self.red_pos = (0, 4)
        self.blue_pos = (8, 4)
        self.remain_walls = {"red" : 10, "blue": 10} # 每个玩家剩余墙数量
        self.walls = {(row, col) : [0, 0, 0, 0] for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)} # 墙 (row, col, dir)
    
    def reset(self):
        self.__init__()
    
    def change_player(self):
        self.player = "red" if self.player == "blue" else "blue"

    def is_end(self):
        return self.red_pos[0] == BOARD_SIZE - 1 or self.blue_pos[0] == 0

    def is_neighbor(self):
        for i in range(4):
            if self.walls[self.red_pos][i]:
                continue
            if self.red_pos[0] + dir[i][0] == self.blue_pos[0] and self.red_pos[1] + dir[i][1] == self.blue_pos[1]:
                return True
        return False
    
    def get_reachable_positions(self):
        if self.is_end():
            return set()
        reachable_positions = set()
        if self.is_neighbor() or self.player == "red":
            for i in range(4):
                if self.walls[self.red_pos][i]:
                    continue
                if self.red_pos[0] + dir[i][0] == self.blue_pos[0] and self.red_pos[1] + dir[i][1] == self.blue_pos[1]:
                    continue
                if 0 <= self.red_pos[0] + dir[i][0] < BOARD_SIZE and 0 <= self.red_pos[1] + dir[i][1] < BOARD_SIZE:
                    reachable_positions.add((self.red_pos[0] + dir[i][0], self.red_pos[1] + dir[i][1]))
        if self.is_neighbor() or self.player == "blue":
            for i in range(4):
                if self.walls[self.blue_pos][i]:
                    continue
                if self.blue_pos[0] + dir[i][0] == self.red_pos[0] and self.blue_pos[1] + dir[i][1] == self.red_pos[1]:
                    continue
                if 0 <= self.blue_pos[0] + dir[i][0] < BOARD_SIZE and 0 <= self.blue_pos[1] + dir[i][1] < BOARD_SIZE:
                    reachable_positions.add((self.blue_pos[0] + dir[i][0], self.blue_pos[1] + dir[i][1]))
        return reachable_positions
    
    def get_min_distance(self, start_row, start_col, end_line):
        q = [((start_row, start_col), 0)]
        vis = set(q[0])
        while len(q) > 0:
            (row, col), dis = q.pop(0)
            if row == end_line:
                return dis
            for i in range(4):
                if self.walls[(row, col)][i]:
                    continue
                new_row = row + dir[i][0]
                new_col = col + dir[i][1]
                if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                    if (new_row, new_col) not in vis:
                        vis.add((new_row, new_col))
                        q.append(((new_row, new_col), dis + 1))
        return -1
    
    def can_reach_end(self, pawn):
        if pawn == "red":
            row, col = self.red_pos
            end_line = 8
        else:
            row, col = self.blue_pos
            end_line = 0
        return self.get_min_distance(row, col, end_line) != -1
    
    def check_move(self, row, col):
        return (row, col) in self.get_reachable_positions()
    
    def check_build_horizontal_wall(self, row, col):
        if self.remain_walls[self.player] == 0:
            return False
        if not(0 < row < BOARD_SIZE and 0 <= col < BOARD_SIZE - 1):
            return False
        if self.walls[(row, col)][0] or self.walls[(row, col + 1)][0] or (self.walls[(row - 1, col + 1)][2] and self.walls[(row, col + 1)][2]):
            return False
        self.walls[(row, col)][0] = 1
        self.walls[(row - 1, col)][1] = 1
        self.walls[(row, col + 1)][0] = 1
        self.walls[(row - 1, col + 1)][1] = 1
        flag = self.can_reach_end("red") and self.can_reach_end("blue")
        self.walls[(row, col)][0] = 0
        self.walls[(row - 1, col)][1] = 0
        self.walls[(row, col + 1)][0] = 0
        self.walls[(row - 1, col + 1)][1] = 0
        return flag
            
    def check_build_vertical_wall(self, row, col):
        if self.remain_walls[self.player] == 0:
            return False
        if not(0 <= row < BOARD_SIZE - 1 and 0 < col < BOARD_SIZE):
            return False
        if (self.walls[(row + 1, col - 1)][0] and self.walls[(row + 1, col)][0]) or self.walls[(row, col)][2] or self.walls[(row + 1, col)][2]:
            return False
        self.walls[(row, col)][2] = 1
        self.walls[(row, col - 1)][3] = 1
        self.walls[(row + 1, col)][2] = 1
        self.walls[(row + 1, col - 1)][3] = 1
        flag = self.can_reach_end("red") and self.can_reach_end("blue")
        self.walls[(row, col)][2] = 0
        self.walls[(row, col - 1)][3] = 0
        self.walls[(row + 1, col)][2] = 0
        self.walls[(row + 1, col - 1)][3] = 0
        return flag
        
    def move_pawn(self, row, col):
        if not self.check_move(row, col):
            return False
        if self.player == "red":
            self.red_pos = (row, col)
        else:
            self.blue_pos = (row, col)
        return True

    def build_horizontal_wall(self, row, col, typ=1):
        if typ and not self.check_build_horizontal_wall(row, col):
            return False
        self.walls[(row, col)][0] = typ
        self.walls[(row - 1, col)][1] = typ
        self.walls[(row, col + 1)][0] = typ
        self.walls[(row - 1, col + 1)][1] = typ
        self.remain_walls[self.player] += -1 if typ == 1 else 1
        return True

    def build_vertical_wall(self, row, col, typ=1):
        if typ and not self.check_build_vertical_wall(row, col):
            return False
        self.walls[(row, col)][2] = typ
        self.walls[(row, col - 1)][3] = typ
        self.walls[(row + 1, col)][2] = typ
        self.walls[(row + 1, col - 1)][3] = typ
        self.remain_walls[self.player] += -1 if typ == 1 else 1
        return True