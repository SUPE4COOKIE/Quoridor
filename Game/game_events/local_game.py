from typing import Any
from Game.game_events.bot_play import Bot

class LocalGame:
    def __init__(self, struct: Any) -> None:
        """
        Initializes a LocalGame instance.
        
        :param struct: A data structure containing various game attributes and settings.
        """
        # Save a reference to the struct object containing game settings
        self.struct = struct

    def switch_player_turn(self) -> None:
        """
        Switches to the next player's turn.
        """
        # Update current player by cycling through the players
        self.struct.current_player = (self.struct.current_player + 1) % self.struct.NUMBER_OF_PLAYERS

    def get_player_turn(self) -> int:
        """
        Returns the index of the current player whose turn it is.
        
        :return: Index of the current player.
        """
        return self.struct.current_player
    
    def init_wall_counter(self) -> None:
        """
        Initializes the wall counter for each player.
        """
        # Populate remaining_walls list with the initial wall count for each player
        for _ in range(self.struct.NUMBER_OF_PLAYERS):
            self.struct.remaining_walls.append(self.struct.INITIAL_WALL_COUNT)

    def decrement_wall_counter(self) -> None:
        """
        Decrements the wall counter of the current player.
        """
        # Decrement the number of walls remaining for the current player
        self.struct.remaining_walls[self.get_player_turn()] -= 1
    
    def get_wall_counter(self) -> int:
        """
        Returns the number of walls remaining for the current player.
        
        :return: Number of walls remaining for the current player.
        """
        return self.struct.remaining_walls[self.get_player_turn()]
    
    def init_board_size(self, size: int) -> None:
        """
        Initializes the board size.
        
        :param size: The size of the board.
        """
        # Set the board size in the struct object
        self.struct.BOARD_SIZE = size

    def init_number_of_players(self, number: int) -> None:
        """
        Initializes the number of players in the game.
        
        :param number: The number of players.
        """
        # Set the number of players in the struct object
        self.struct.NUMBER_OF_PLAYERS = number
    
    def init_number_of_walls(self, number: int) -> None:
        """
        Initializes the number of walls in the game.
        
        :param number: The number of walls.
        """
        # Set the initial number of walls in the struct object
        self.struct.INITIAL_WALL_COUNT = number

    def init_bots(self, number: int, board: Any) -> None:
        """
        Initializes AI bots in the game.
        
        :param number: The number of bots.
        :param board: The game board.
        """
        # Create bot instances and save them in the struct object
        for i in range(1, number + 1):
            self.struct.bot_instances[i] = Bot(i, board)
    
    def game_over(self) -> None:
        """
        Ends the game by setting is_running to False.
        """
        # Set is_running to False, indicating the game is over
        self.struct.is_running = False
