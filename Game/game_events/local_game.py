class LocalGame:
    def __init__(self, struct):
        self.struct = struct # save reference to the struct

    def switch_player_turn(self):
        self.struct.current_player = (self.struct.current_player + 1) % self.struct.NUMBER_OF_PLAYERS

    def get_player_turn(self):
        return self.struct.current_player
    
    def init_wall_counter(self):
        for _ in range(self.struct.NUMBER_OF_PLAYERS):
            self.struct.remaining_walls.append(self.struct.INITIAL_WALL_COUNT)

    def decrement_wall_counter(self):
        self.struct.remaining_walls[self.get_player_turn()] -= 1
    
    def get_wall_counter(self):
        return self.struct.remaining_walls[self.get_player_turn()]
    
    def init_board_size(self,size):
        self.struct.BOARD_SIZE = size

    def init_number_of_players(self, number):
        self.struct.NUMBER_OF_PLAYERS = number
    
    def init_number_of_walls(self, number):
        self.struct.INITIAL_WALL_COUNT = number
