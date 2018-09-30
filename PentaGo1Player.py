import PentaGoEngine
import RandomAI
import Alphabeta

if __name__ == '__main__':
    app = PentaGoEngine.PentaGo(
    ai_delay = 20,
    red_player = Alphabeta.minimax,
    # red_player = RandomAI.choose_move,
    # blue_player = RandomAI.choose_move
    blue_player = Alphabeta.minimax
    # blue_player = None
    )

    app.game_loop()
