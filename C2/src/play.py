import torch

from game import Connect2Game
from model import Connect2Model
from trainer import Trainer

from monte_carlo_tree_search import MCTS

import argparse

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

game = Connect2Game()
board_size = game.get_board_size()
action_size = game.get_action_size()

model = Connect2Model(board_size, action_size, device)

argp = argparse.ArgumentParser()
argp.add_argument('--reading_params_path',default=None)
Args = argp.parse_args()

args = {
        'batch_size': 64,
        'numIters': 50,                                # Total number of training iterations
        'num_simulations': 100,                         # Total number of MCTS simulations to run when deciding on a move to play
        'numEps': 100,                                  # Number of full games (episodes) to run during each iteration
        'numItersForTrainExamplesHistory': 20,
        'epochs': 2,                                    # Number of epochs of training per iteration
        'checkpoint_path': 'latest.pth'                 # location to save latest set of weights
    }

if Args.reading_params_path:
    model.load_state_dict(torch.load(Args.reading_params_path))
else:
    trainer = Trainer(game, model, args)
    trainer.learn()

mcts = MCTS(game, model, args)

# usage python src/play.py --reading_params_path model.params


def play_game():
    ai_first = int(input("请选择 AI 是否先手: ")) * 2 - 1
    current_player = 1  # 假设AI先手
    state = game.get_init_board()  # 初始状态

    while True:
        print("当前棋盘状态：")
        game.display(state, current_player)  # 显示当前棋盘

        if current_player == ai_first:
            # AI 回合
            canonical_board = game.get_canonical_board(state, current_player)
            root = mcts.run(model, canonical_board, to_play=1)  # 使用mcts获取根节点
            action = root.select_action(temperature=0)  # 根据访问次数选择最佳动作

            print("AI选择了动作：", action)

        else:
            # 人类回合
            valid_moves = game.get_valid_moves(state)
            print("合法动作：", [i for i, valid in enumerate(valid_moves) if valid])
            
            while True:
                try:
                    action = int(input("请选择一个合法的动作: "))
                    if valid_moves[action] == 1:
                        break
                    else:
                        print("非法动作，请选择其他动作。")
                except (ValueError, IndexError):
                    print("请输入有效的数字。")

        # 执行动作并更新状态
        state, current_player = game.get_next_state(state, current_player, action)

        # 检查游戏是否结束
        reward = game.get_reward_for_player(state, ai_first)
        if reward is not None:
            print("当前棋盘状态：")
            game.display(state, current_player)  # 显示当前棋盘
            if reward == 1:
                print("AI赢了！")
            elif reward == -1:
                print("人类玩家赢了！")
            else:
                print("平局！")
            break

play_game()