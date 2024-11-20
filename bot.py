from game_logic import *

class Bot:
    def move(self, game):
        mn = 1000
        action = None
        end_line = BOARD_SIZE - 1 if game.player == "red" else 0
        for row, col in game.get_reachable_positions():
                dis = game.get_min_distance(row, col, end_line)
                if mn > dis:
                    mn = dis
                    action = row * BOARD_SIZE + col
        return action
    
    def build(self, game):
        if game.remain_walls[game.player] == 0:
            return None
        my_row, my_col = game.red_pos if game.player == "red" else game.blue_pos
        opponent_row, opponent_col = game.red_pos if game.player == "blue" else game.blue_pos
        my_end_line = BOARD_SIZE - 1 if game.player == "red" else 0
        opponent_end_line = BOARD_SIZE - 1 if game.player == "blue" else 0
        my_dis = game.get_min_distance(my_row, my_col, my_end_line)
        opponent_dis = game.get_min_distance(opponent_row, opponent_col, opponent_end_line)
        mx = opponent_dis - my_dis
        action = None
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                    if game.check_build_horizontal_wall(row, col):
                        game.build_horizontal_wall(row, col)
                        now_my_dis = game.get_min_distance(my_row, my_col, my_end_line)
                        now_opponent_dis = game.get_min_distance(opponent_row, opponent_col, opponent_end_line)
                        if mx < now_opponent_dis - now_my_dis:
                            mx = now_opponent_dis - now_my_dis
                            action = BOARD_SIZE * BOARD_SIZE + row * BOARD_SIZE + col
                        game.build_horizontal_wall(row, col, typ=0)

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                    if game.check_build_vertical_wall(row, col):
                        game.build_vertical_wall(row, col)
                        now_my_dis = game.get_min_distance(my_row, my_col, my_end_line)
                        now_opponent_dis = game.get_min_distance(opponent_row, opponent_col, opponent_end_line)
                        if mx < now_opponent_dis - now_my_dis:
                            mx = now_opponent_dis - now_my_dis
                            action = 2 * BOARD_SIZE * BOARD_SIZE + row * BOARD_SIZE + col
                        game.build_vertical_wall(row, col, typ=0)
        return action

    def play(self, game):
        action = self.build(game)
        if action:
            return action
        else:
            return self.move(game)