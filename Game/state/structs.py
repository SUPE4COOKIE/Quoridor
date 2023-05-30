
# board struct is represented by an array of arrays that contains dicts for every cells
from asyncio import Queue
class GameStructs:
    def __init__(self) -> None:
        self.input_queue = Queue()
        self.mouse_position_queue = Queue()
        self.hovered_wall = None
        self.is_running = True
        self.tiles = []
