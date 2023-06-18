from Game.elements.tile import Tile
from Game.elements.wall import Wall
from Game.elements.pawn import Pawn
from secrets import choice
from typing import Any, List, Tuple, Union
from pygame import Surface

class Board:
    def __init__(self, struct: Any) -> None:
        """
        Initialize the Board class which represents the game board.

        :param struct: An object containing game configuration data.
        """
        self.SIZE = struct.BOARD_SIZE
        self.PLAYERS = struct.NUMBER_OF_PLAYERS
        self.PLAYER_COLORS = struct.PLAYER_COLORS
        self.tiles = []  # List to store tiles on the board
        self.__init_pawns()
        self.WALL_WIDTH = struct.WALL_WIDTH[self.SIZE]
        self.WALL_HEIGHT = struct.WALL_HEIGHT
        self.TILE_SIZE = struct.TILE_SIZES[self.SIZE] + self.WALL_HEIGHT
        self.__init_tiles()


    def __init_tiles(self) -> None:
        """
        Initialize tiles on the board along with walls.
        """
        for i in range(self.SIZE):
            row = []
            for j in range(self.SIZE):
                # Determine which sides can have active walls
                top_active = i != 0
                right_active = j != self.SIZE - 1
                bottom_active = i != self.SIZE - 1
                left_active = j != 0

                # Setup Wall objects, reusing if available
                up = self.tiles[i - 1][j].wall_down if i > 0 else Wall(
                    j * self.TILE_SIZE, i * self.TILE_SIZE, self.WALL_WIDTH, self.WALL_HEIGHT, "horizontal", active=top_active
                )
                right = Wall(
                    (j + 1) * self.TILE_SIZE, i * self.TILE_SIZE, self.WALL_WIDTH, self.WALL_HEIGHT, "vertical", active=right_active
                )
                down = Wall(
                    j * self.TILE_SIZE, (i + 1) * self.TILE_SIZE, self.WALL_WIDTH, self.WALL_HEIGHT, "horizontal", active=bottom_active
                )
                left = row[-1].wall_right if j > 0 else Wall(
                    j * self.TILE_SIZE, i * self.TILE_SIZE, self.WALL_WIDTH, self.WALL_HEIGHT, "vertical", active=left_active
                )

                # Create tile and append to row
                tile = Tile(j * self.TILE_SIZE + self.WALL_HEIGHT, i * self.TILE_SIZE + self.WALL_HEIGHT,
                            self.TILE_SIZE, (j, i), up, right, down, left, self.WALL_HEIGHT)
                row.append(tile)

            self.tiles.append(row)


    def __init_pawns(self) -> None:
        """
        Initialize pawns for each player on the board.
        """
        self.pawns = []
        for player_count in range(self.PLAYERS):
            # Set the starting positions (at the center of their side) and their colors for pawns depending on the player number
            if player_count == 0:
                x = self.SIZE // 2
                y = self.SIZE - 1
                color = self.PLAYER_COLORS[player_count]
            elif player_count == 1:
                x = self.SIZE // 2
                y = 0
                color = self.PLAYER_COLORS[player_count]
            elif player_count == 2:
                x = self.SIZE - 1
                y = self.SIZE // 2
                color = self.PLAYER_COLORS[player_count]
            else:
                x = 0
                y = self.SIZE // 2
                color = self.PLAYER_COLORS[player_count]
            self.pawns.append(Pawn(x, y, color))


    def draw_tiles(self, win: Surface) -> None:
        """
        Draw tiles and pawns on the given surface.

        :param win: Surface on which to draw.
        """
        for row in self.tiles:
            for tile in row:
                tile.draw(win)
                for pawn in self.pawns:
                    # Assign pawn to tile if coordinates match
                    if pawn.x == tile.x_index and pawn.y == tile.y_index:
                        tile.pawn = pawn
                    # Remove pawn from tile if it moved elsewhere
                    elif tile.pawn and (pawn.x != tile.x_index or pawn.y != tile.y_index) and tile.pawn == pawn:
                        tile.pawn = None

    def draw_pawns(self, win: Surface) -> None:
        """
        Draw pawns on the given surface.

        :param win: Surface on which to draw.
        """
        self.win = win
        for pawn in self.pawns:
            pawn.draw_on_tile(win, self.tiles[pawn.y][pawn.x])

    
    def get_neighbor(self, x: int, y: int, orientation: int) -> Wall:
        """
        Get the neighboring tile's wall of the tile at the given coordinates and orientation.
    
        :param x: The x coordinate of the tile.
        :param y: The y coordinate of the tile.
        :param orientation: The orientation (0 to 3).
        :return: The neighboring tile's wall.
        """
        # Check if the orientation is vertical
        if orientation == 1 or orientation == 3:
            # If not on the last row, return wall from tile below, otherwise from tile above
            if y < self.SIZE - 1:
                return self.tiles[y + 1][x].GetWalls()[orientation]
            else:
                return self.tiles[y - 1][x].GetWalls()[orientation]
        else:  # Horizontal orientation
            # If not in the last column, return wall from tile to the right, otherwise from tile to the left
            if x < self.SIZE - 1:
                return self.tiles[y][x + 1].GetWalls()[orientation]
            else:
                return self.tiles[y][x - 1].GetWalls()[orientation]
    
    def is_move_possible(self, tile: Tile, player_number: int) -> bool:
        """
        Check if a move is possible for the given player's pawn to the specified tile.

        :param tile: The tile to which the move is being checked.
        :param player_number: The number of the player.
        :return: True if move is possible, False otherwise.
        """
        # If the tile does not have a pawn
        if tile.pawn is None:
            pawn = self.pawns[player_number]
            diff_x = abs(tile.x_index - pawn.x)
            diff_y = abs(tile.y_index - pawn.y)

            # Check if the move is horizontal or vertical and only by one step
            is_horizontal_move = (diff_x == 1) and (tile.y_index == pawn.y)
            is_vertical_move = (diff_y == 1) and (tile.x_index == pawn.x)


            # check if there's a wall in the way
            if is_horizontal_move:
                if pawn.x <= tile.x_index: # moving right
                    if tile.x_index <= self.SIZE - 1:
                        return not tile.wall_left.placed
                    else:
                        return False
                else: # moving left
                    if tile.x_index >= 0:
                        return not tile.wall_right.placed
                    else:
                        return False
            elif is_vertical_move:
                if pawn.y <= tile.y_index: # moving down
                    if tile.y_index <= self.SIZE - 1:
                        return not tile.wall_up.placed
                    else:
                        return False
                else: # moving up
                    if tile.y_index >= 0:
                        return not tile.wall_down.placed
                    else:
                        return False

            if is_horizontal_move or is_vertical_move:
                return True
        
        else:
            # If a pawn is present, the player can possibly jump over
            # the pawn if there is a tile behind the pawn.
            # Determine the direction of the other pawn relative to the player's pawn
            x_diff = tile.x_index - self.pawns[player_number].x
            y_diff = tile.y_index - self.pawns[player_number].y

            # Get the coordinates of the tile behind the other pawn
            next_x = tile.x_index + x_diff
            next_y = tile.y_index + y_diff

            # Check that the tile behind the other pawn exists and doesn't have a pawn on it
            if next_x >= 0 and next_x < self.SIZE and next_y >= 0 and next_y < self.SIZE and self.tiles[next_y][next_x].pawn is None:
                # Check for walls between the player's pawn and the other pawn,
                # as well as between the other pawn and the tile behind it
                if x_diff == 0:  # vertical jump
                    no_wall_between = (not tile.wall_up.placed and not tile.wall_down.placed) if y_diff < 0 else (not tile.wall_down.placed and not self.tiles[next_y][next_x].wall_up.placed)
                else:  # horizontal jump
                    no_wall_between = (not tile.wall_left.placed and not tile.wall_right.placed) if x_diff < 0 else (not tile.wall_right.placed and not self.tiles[next_y][next_x].wall_left.placed)

                if no_wall_between:
                    return True


        return False
    

    def is_wall_placeable(self, tile: Tile, orientation: int) -> bool:
        """
        Check if a wall can be placed at the given tile and orientation.

        :param tile: The tile where the wall is to be placed.
        :param orientation: The orientation of the wall (0 to 3).
        :return: True if the wall can be placed, False otherwise.
        """
        # Check if the neighboring wall is already placed
        neighbor = self.get_neighbor(tile.x_index, tile.y_index, orientation)
        if neighbor.placed:
            return False
        
        # Check if the wall is active
        if not tile.GetWalls()[orientation].active:
            return False
        
         # Check if a wall exists in the perpendicular direction
        if (orientation == 1 or orientation == 3) and tile.wall_down.placed:
            return False
        elif (orientation == 2 or orientation == 0) and tile.wall_right.placed:
            return False
        
        return True
    
    def is_winner(self, player_number: int) -> bool:
        """
        Check if a given player has won.

        :param player_number: The player number.
        :return: True if the player has won, False otherwise.
        """
        # Depending on the player number, check if the player's pawn has reached 
        # the target row or column.
        if player_number == 0:
            return self.pawns[player_number].y == 0
        elif player_number == 1:
            return self.pawns[player_number].y == self.SIZE - 1
        elif player_number == 2:
            return self.pawns[player_number].x == 0
        else:
            return self.pawns[player_number].x == self.SIZE - 1
    
    def is_move_possible_bfs(self, start_tile: Tile, end_tile: Tile) -> bool:
        """
        Check if it is possible to move from a start tile to an end tile used for BFS later.
    
        :param start_tile: The start tile.
        :param end_tile: The end tile.
        :return: True if the move is possible, False otherwise.
        """

        diff_x = abs(start_tile.x_index - end_tile.x_index) 
        diff_y = abs(start_tile.y_index - end_tile.y_index)

        # Check if the move is horizontal or vertical and only by one step
        is_horizontal_move = (diff_x == 1) and (start_tile.y_index == end_tile.y_index)
        is_vertical_move = (diff_y == 1) and (start_tile.x_index == end_tile.x_index)

        # Check if there is a wall in the way
        if is_horizontal_move:
            if start_tile.x_index < end_tile.x_index: # moving right
                return not start_tile.wall_right.placed
            else: # moving left
                return not start_tile.wall_left.placed
        elif is_vertical_move:
            if start_tile.y_index < end_tile.y_index: # moving down
                return not start_tile.wall_down.placed
            else: # moving up
                return not start_tile.wall_up.placed
        return False

        
    def get_possible_neighbors(self, tile: Tile) -> List[Tile]:
        """
        Get all possible neighboring tiles of a given tile.

        :param tile: The tile to find neighbors of.
        :return: A list of neighboring tiles.
        """
        neighbors = []
        dx = [-1, 1, 0, 0] # x direction to go through
        dy = [0, 0, -1, 1] # y direction to go through

        # check if the move is possible to any tiles arround the current tile
        for i in range(4):
            x = tile.x_index + dx[i]
            y = tile.y_index + dy[i]
            if x >= 0 and x < self.SIZE and y >= 0 and y < self.SIZE: # check if the tile is in the board
                if self.is_move_possible_bfs(tile, self.tiles[y][x]):
                    neighbors.append(self.tiles[y][x])
        
        return neighbors

    def is_path_to_victory_for_all_players(self) -> bool:
        """
        Check if there is a path to victory for all players.

        :return: True if there is a path to victory for all players, False otherwise.
        """
        for player_number in range(self.PLAYERS):
            starting_tile = self.tiles[self.pawns[player_number].y][self.pawns[player_number].x] # current player position
            reachable_tiles = [starting_tile] # tiles that can be reached from the current player position
            visited = [[False]*self.SIZE for _ in range(self.SIZE)] # 2D array to keep track of visited tiles
            visited[starting_tile.y_index][starting_tile.x_index] = True # mark the starting tile as visited

            queue = [starting_tile] # queue to keep track of tiles to visit

            while queue:
                current_tile = queue.pop(0) # get the first tile in the queue

                neighbors = self.get_possible_neighbors(current_tile) # get all possible neighbors of the current tile

                for neighbor in neighbors:
                    if not visited[neighbor.y_index][neighbor.x_index]: # check if the neighbor has not been visited
                        queue.append(neighbor) # add the neighbor to the queue
                        reachable_tiles.append(neighbor) # add the neighbor to the reachable tiles
                        visited[neighbor.y_index][neighbor.x_index] = True # mark the neighbor as visited

            player_reached_target = False

            for i in reachable_tiles:
                # Check if Player 0 has reached the top row
                if player_number == 0:
                    if i.y_index == 0:
                        player_reached_target = True
                        break

                # Check if Player 1 has reached the bottom row
                elif player_number == 1:
                    if i.y_index == self.SIZE - 1:
                        player_reached_target = True
                        break

                # Check if Player 2 has reached the leftmost column
                elif player_number == 2:
                    if i.x_index == 0:
                        player_reached_target = True
                        break

                # Check if Player 3 has reached the rightmost column
                else:
                    if i.x_index == self.SIZE - 1:
                        player_reached_target = True
                        break

            if not player_reached_target:
                return False

        return True



    def get_random_neighbor_tile(self, player: int) -> Tile:
        """
        Get a random neighbor tile of a given player's pawn.

        :param player: The player number.
        :return: A randomly selected neighboring tile.
        """
        # Getting current position of the player's pawn
        x, y = self.pawns[player].x, self.pawns[player].y
        
        # Getting possible neighbor tiles
        neighbors = self.get_possible_neighbors(self.tiles[y][x])
        
        # Securely and randomly selecting a neighbor
        return choice(neighbors)

    def get_random_possible_wall(self) -> Tuple[Tile, int]:
        """
        Get a random possible wall placement.
    
        :return: A tuple containing a randomly selected tile and orientation.
        """
        # List to store tiles with possible wall placements
        possible_walls = []
        
        # Iterate through all tiles
        for row in self.tiles:
            for tile in row:
                # Check each orientation (0 to 3)
                for orientation in range(4):
                    # Check if a wall can be placed at this orientation
                    if self.is_wall_placeable(tile, orientation):
                        possible_walls.append((tile, orientation))
        
        # Securely and randomly selecting a tile and orientation for wall placement
        return choice(possible_walls)