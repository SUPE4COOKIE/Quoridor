from typing import Any
from secrets import choice

class Bot:
    def __init__(self, bot_id: int, board: Any) -> None:
        """
        Initializes a Bot instance.
        
        :param bot_id: The identifier of the bot.
        :param board: The game board.
        """
        # Save the bot's ID and a reference to the game board
        self.player_id = bot_id
        self.board = board
        
        # Reference to the bot's pawn on the board
        self.pawn = self.board.pawns[self.player_id]

    def play(self) -> None:
        """
        Makes a move for the bot on the game board. The bot can either move its pawn
        to a neighboring tile or place a wall on the board. The action is randomly
        chosen for the bot.
        """
        # Get a list of possible actions the bot can take
        actions = [self.board.get_random_neighbor_tile(self.player_id), self.board.get_random_possible_wall()]
        
        # Securely make a random choice from the possible actions
        result = choice(actions)
        
        # Determine the type of action and execute it
        if result is not None:
            # If result is of the class Tile, it means the bot moves its pawn
            if result.__class__.__name__ == "Tile":
                self.pawn.move(result)
            # If result is a wall placement action
            else:
                # Extract the tile and wall orientation from the result
                wall = result[0].GetWalls()[result[1]] # result[0] is the tile, result[1] is the orientation
                
                # Get the neighboring tile associated with the wall
                neighbor = self.board.get_neighbor(result[0].x_index, result[0].y_index, result[1])
                
                # Execute the wall placement
                wall.place()
                neighbor.place()
