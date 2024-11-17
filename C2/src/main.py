import torch

from game import Connect2Game
from model import Connect2Model
from trainer import Trainer
import argparse

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

args = {
    'batch_size': 64,
    'numIters': 50,                                # Total number of training iterations
    'num_simulations': 100,                         # Total number of MCTS simulations to run when deciding on a move to play
    'numEps': 100,                                  # Number of full games (episodes) to run during each iteration
    'numItersForTrainExamplesHistory': 20,
    'epochs': 2,                                    # Number of epochs of training per iteration
    'checkpoint_path': 'latest.pth'                 # location to save latest set of weights
}

argp = argparse.ArgumentParser()
argp.add_argument('--reading_params_path',default=None)
argp.add_argument('--writing_params_path',default=None)
Args = argp.parse_args()

game = Connect2Game()
board_size = game.get_board_size()
action_size = game.get_action_size()

model = Connect2Model(board_size, action_size, device)
if Args.reading_params_path:
    model.load_state_dict(torch.load(Args.reading_params_path))
else:
    trainer = Trainer(game, model, args)
    trainer.learn()

if Args.writing_params_path:
    torch.save(model.state_dict(), Args.writing_params_path)