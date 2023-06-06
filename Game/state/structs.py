
# board struct is represented by an array of arrays that contains dicts for every cells
from asyncio import Queue
class GameStructs:
    def __init__(self) -> None:
        self.input_queue = Queue()
        self.mouse_position_queue = Queue()
        self.hovered_wall = False
        self.placed_wall = False
        self.is_running = True
        self.current_player = 0
        self.PLAYER_COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]
        self.remaining_walls = []

