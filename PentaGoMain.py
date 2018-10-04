import PentaGoEngine
import RandomAI
import Minimax

'''Comment and uncomment the arguments depending on what confirguaration
you want'''

if __name__ == '__main__':
    app = PentaGoEngine.PentaGo(
    ai_delay = 20,
    # red_player = None, # Human plays red
    red_player = Minimax.minimax, # Minimax AI plays red
    # red_player = RandomAI.choose_move, # Random AI plays red
    blue_player = None, # Human plays blue
    # blue_player = Minimax.minimax, # Minimax AI plays blue
    # blue_player = RandomAI.choose_move # Random AI plays blue
    )

    app.game_loop()
