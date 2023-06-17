from secrets import choice
class Bot:
    def __init__(self, bot_id, board):
        self.player_id = bot_id
        self.board = board
        self.pawn = self.board.pawns[self.player_id]

    def play(self):
        actions = [self.board.get_random_neighbor_tile(self.player_id), self.board.get_random_possible_wall()]
        result = choice(actions)
        if result is not None and result.__class__.__name__ == "Tile":
            self.pawn.move(result)
        else:
            wall = result[0].GetWalls()[result[1]] # result[0] is the tile, result[1] is the orientation
            neighbor = self.board.get_neighbor(result[0].x_index, result[0].y_index, result[1])
            wall.click()
            neighbor.click()
