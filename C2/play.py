import torch

from environment import Env
from model import QuoridorModel
from trainer import Trainer

from monte_carlo_tree_search import MCTS

import argparse

import tkinter as tk

from game_logic import QuoridorGame
from game_UI import QuoridorUI

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

env = Env()
board_size = env.get_board_size()
action_size = env.get_action_size()

model = QuoridorModel(board_size, action_size, device)

argp = argparse.ArgumentParser()
argp.add_argument('--reading_params_path',default=None)
Args = argp.parse_args()

args = {
    'batch_size': 64,
    'numIters': 20,                                # Total number of training iterations
    'num_simulations': 20,                         # Total number of MCTS simulations to run when deciding on a move to play
    'numEps': 30,                                  # Number of full games (episodes) to run during each iteration
    'numItersForTrainExamplesHistory': 20,
    'epochs': 2,                                    # Number of epochs of training per iteration
    'checkpoint_path': 'latest.pth'                 # location to save latest set of weights
}

assert Args.reading_params_path

checkpoint = torch.load(Args.reading_params_path, map_location=torch.device('cpu'))

# 然后从checkpoint字典中提取'state_dict'部分，并将其加载到模型
model.load_state_dict(checkpoint['state_dict'])

# model.load_state_dict(torch.load(Args.reading_params_path, map_location=torch.device('cpu')))

mcts = MCTS(env, model, args)

root = tk.Tk()
root.title("Quoridor")
root.geometry("900x600")

game = QuoridorGame()
UI = QuoridorUI(root, game)

# usage:  python play.py --reading_params_path model.params

def update_draw():
    if UI.ai_first != 0 and not UI.game.is_end() and UI.in_main_frame:
        current_player = 1 if UI.game.player == "red" else -1
        if current_player == UI.ai_first:
            UI.disable_button()
            state = env.get_state(UI.game)
            canonical_board = env.get_canonical_board(state, current_player)
            node = mcts.run(model, canonical_board, 1)  
            action = env.get_real_action(node.select_action(temperature=0), current_player)
            UI.root.after(200, lambda: None)
            UI.get_next_game(action)
            UI.enable_button()
            
    UI.root.after(50, update_draw)

def play_game():

    update_draw()

    UI.root.mainloop()

play_game()