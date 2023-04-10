
# board struct is represented by an array of arrays that contains dicts for every cells
from asyncio import Queue
class GameStructs:
    def __init__(self) -> None:
        self.input_queue = Queue()
        self.mouse_position_queue = Queue()
        self.hovered_wall = None
        self.is_running = True
        self.tiles = []

    def create_board(self, SIZE):

        if hasattr(self, 'board'):
            return                 # if the board is already created, return

        if SIZE not in [5, 7, 9, 11]:  # if the size is not in the list of valid sizes, return
            return

        self.tiles = []  # init the tiles array

        self.__init_pawn_position(SIZE)  # init the pawn position

    def __init_pawn_position(self, SIZE):
        self.player_positions = {"player_0": {
            "x": SIZE-1, "y": SIZE//2}, "player_1": {"x": 0, "y": SIZE//2}}
        
        # set the pawn of player 0 to the position to the middle of the last row
        self.board[self.player_positions["player_0"]["x"]
                   ][self.player_positions["player_0"]["y"]]["pawn"] = "red"
        # set the pawn of player 1 to the position to the middle of the first row
        self.board[self.player_positions["player_0"]
                   ["x"]][self.player_positions["player_0"]["y"]]["pawn"] = "green"
