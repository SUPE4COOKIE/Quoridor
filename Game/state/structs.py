from asyncio import Queue
class GameStructs:
    def __init__(self) -> None:
        self.input_queue = Queue() # Queue of inputs from the user
        self.mouse_position_queue = Queue() # Queue of mouse positions
        self.hovered_wall = False # Flag to avoid double hover
        self.placed_wall = False # Flag to avoid double wall placement
        self.is_running = True # Flag to stop the game
        self.WIDTH = 825 # Game window width
        self.HEIGHT = 925 # Game window height
        self.BOARD_SIZES = ["5x5", "7x7", "9x9", "11x11"] # Available board sizes
        self.NUMBERS_OF_BARRIERS = [str(i) for i in range(4, 41, 4)]  # Multiples of 4 from 4 to 40 for available number of barriers
        self.NUMBERS_OF_PLAYERS = ["2", "4"] # Available number of players
        self.NUMBERS_OF_BOTS = ["0", "1", "2"] # Available number of bots
        self.MAX_NUMBER_OF_BARRIERS = {0: 2, 1: 4, 2: 7, 3: 10} # limit the number of barrier based on the board size (index of each)
        # Tile sizes for each board size
        self.TILE_SIZES = {
            5: 141,
            7: 95,
            9: 70,
            11: 53
        }
        # Wall width for each board size
        self.WALL_WIDTH = {
            5: 180,
            7: 135,
            9: 110,
            11: 85
        }

        self.WALL_HEIGHT = 20 # Wall height
        self.current_player = 0 # Current player index
        self.WIN_MESSAGE = "Player {} wins!" # Win message
        self.PLAYER_COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)] # Player colors List
        self.remaining_walls = [] # Remaining walls for each player
        self.bot_instances = {} # Dict of bot instances

