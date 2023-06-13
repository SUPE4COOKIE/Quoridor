
from asyncio import Queue
class GameStructs:
    def __init__(self) -> None:
        self.input_queue = Queue()
        self.mouse_position_queue = Queue()
        self.hovered_wall = False
        self.placed_wall = False
        self.is_running = True
        self.BOARD_SIZES = ["5x5", "7x7", "9x9", "11x11"]
        self.NUMBERS_OF_BARRIERS = [str(i) for i in range(4, 41, 4)]  # Multiples of 4 from 4 to 40
        self.NUMBERS_OF_PLAYERS = ["2", "4"]
        self.NUMBERS_OF_BOTS = ["0", "1", "2"]
        self.MAX_NUMBER_OF_BARRIERS = {0: 2, 1: 4, 2: 7, 3: 10} # limit the number of barrier based on the board size (index of each)
        self.TILE_SIZES = {
            5: 120,
            7: 95,
            9: 70,
            11: 45
        }
        self.WALL_WIDTH = {
            5: 155,
            7: 135,
            9: 110,
            11: 85
        }
        self.WALL_HEIGHT = 20
        self.current_player = 0
        self.PLAYER_COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]
        self.remaining_walls = []

