import tkinter as tk

from game_logic import QuoridorGame
from game_UI import QuoridorUI
from bot import Bot

root = tk.Tk()
root.title("Quoridor")
root.geometry("900x600")

game = QuoridorGame()
UI = QuoridorUI(root, game)
bot = Bot()

def update_draw():
    if UI.ai_first != 0 and not game.is_end() and UI.in_main_frame:
        current_player = 1 if game.player == "red" else -1
        if current_player == UI.ai_first:
            UI.disable_button()
            action = bot.play(game)
            UI.get_next_game(action)
            UI.enable_button()
            
    UI.root.after(400, update_draw)

def play_game():
    update_draw()
    UI.root.mainloop()

play_game()