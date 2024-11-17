import numpy as np
from game_logic import QuoridorGame, BOARD_SIZE
import copy as cp

class Env():
    def __init__(self):
        pass

    def get_init_board(self):
        return self.get_state(QuoridorGame())

    def get_board_size(self):
        # red_pos blue_pos red_remain_walls blue_remain_walls walls
        return 6 + BOARD_SIZE * BOARD_SIZE * 4
    
    def get_action_size(self):
        return 3 * BOARD_SIZE * BOARD_SIZE

    def get_game(self, state, player):
        game = QuoridorGame()
        game.player = "red" if player == 1 else "blue"
        game.red_pos = (state[0], state[1])
        game.blue_pos = (state[2], state[3])
        game.remain_walls["red"] = state[4]
        game.remain_walls["blue"] = state[5]
        it = 6
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                game.walls[(row, col)] = [state[it], state[it + 1], state[it + 2], state[it + 3]]
                it += 4
        return game
        
    def get_state(self, game : QuoridorGame):
        state = np.zeros(self.get_board_size(), dtype=np.int32)
        state[0], state[1] = game.red_pos
        state[2], state[3] = game.blue_pos
        state[4] = game.remain_walls["red"]
        state[5] = game.remain_walls["blue"]
        it = 6
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                state[it], state[it + 1], state[it + 2], state[it + 3] = game.walls[(row, col)]
                it += 4
        return state

    def get_next_state(self, state, player, action):
        game = self.get_game(state, player)
        if action < BOARD_SIZE * BOARD_SIZE:
            row = action // BOARD_SIZE
            col = action % BOARD_SIZE
            game.move_piece(row, col)
        elif action < 2 * BOARD_SIZE * BOARD_SIZE:
            action -= BOARD_SIZE * BOARD_SIZE
            row = action // BOARD_SIZE
            col = action % BOARD_SIZE
            game.place_horizontal_wall(row, col)
        else:
            action -= 2 * BOARD_SIZE * BOARD_SIZE
            row = action // BOARD_SIZE
            col = action % BOARD_SIZE
            game.place_vertical_wall(row, col)
        game.change_player()
        return (self.get_state(game), -player)
    
    def get_valid_moves(self, state, player):
        actions = []
        game = self.get_game(state, player)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                actions.append(int(game.check_move(row, col)))

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                actions.append(int(game.check_place_horizontal_wall(row, col)))

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                actions.append(int(game.check_place_vertical_wall(row, col)))

        return actions
    
    def is_win(self, state, player):
        game = self.get_game(state, player)
        if player == 1:
            return game.red_pos[0] == BOARD_SIZE - 1
        else:
            return game.blue_pos[0] == 0
        
    def get_reward_for_player(self, state, player):
        if self.is_win(state, player):
            return 1
        if self.is_win(state, -player):
            return -1
        return None
    
    def get_canonical_board(self, state, player):
        game = self.get_game(state, player)
        if player == -1:
            tmp_pos = game.red_pos
            game.red_pos = (BOARD_SIZE - 1 - game.blue_pos[0], BOARD_SIZE - 1 - game.blue_pos[1])
            game.blue_pos = (BOARD_SIZE - 1 - tmp_pos[0], BOARD_SIZE - 1 - tmp_pos[1])
            tmp_remain_walls = game.remain_walls["red"]
            game.remain_walls["red"] = game.remain_walls["blue"]
            game.remain_walls["blue"] = tmp_remain_walls
            walls = cp.deepcopy(game.walls)
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    tmp_walls = walls[(BOARD_SIZE - 1 - row, BOARD_SIZE - 1 - col)]
                    game.walls[(row, col)][0] = tmp_walls[1]
                    game.walls[(row, col)][1] = tmp_walls[0]
                    game.walls[(row, col)][2] = tmp_walls[3]
                    game.walls[(row, col)][3] = tmp_walls[2]
        return self.get_state(game)
    
    def get_real_action(self, action, player):
        if player == -1:
            if action < BOARD_SIZE * BOARD_SIZE:
                row = action // BOARD_SIZE
                col = action % BOARD_SIZE
                action = (BOARD_SIZE - 1 - row) * BOARD_SIZE + BOARD_SIZE - 1 - col
            elif action < 2 * BOARD_SIZE * BOARD_SIZE:
                action -= BOARD_SIZE * BOARD_SIZE
                row = action // BOARD_SIZE
                col = action % BOARD_SIZE
                action = BOARD_SIZE * BOARD_SIZE + (BOARD_SIZE - row) * BOARD_SIZE + BOARD_SIZE - 2 - col
            else:
                action -= 2 * BOARD_SIZE * BOARD_SIZE
                row = action // BOARD_SIZE
                col = action % BOARD_SIZE
                action = 2 * BOARD_SIZE * BOARD_SIZE + (BOARD_SIZE - 2 - row) * BOARD_SIZE + BOARD_SIZE - col
        return action