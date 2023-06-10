from Game.elements.tile import Tile
from Game.elements.wall import Wall
from Game.elements.pawn import Pawn

class Board:
    #TODO : const some non changing values
    def __init__(self, struct):
        self.size = struct.BOARD_SIZE
        self.players = struct.NUMBER_OF_PLAYERS
        self.PLAYER_COLORS = struct.PLAYER_COLORS
        self.tiles = []
        self.__init_pawns()
        self.tile_size = 115
        self.__init_tiles()


    def __init_tiles(self):
        for i in range(self.size):
            row = []
            for j in range(self.size):
            
                # Setup wall activity
                top_active = not (i == 0)
                right_active = not (j == self.size - 1)
                bottom_active = not (i == self.size - 1)
                left_active = not (j == 0)
    
                # Setup Wall object, reusing if available
                up = self.tiles[i - 1][j].wall_down if i > 0 else Wall(j * self.tile_size, i * self.tile_size, "horizontal", active=top_active)
                right = Wall((j + 1) * self.tile_size, i * self.tile_size, "vertical", active=right_active)
                down = Wall(j * self.tile_size, (i + 1) * self.tile_size, "horizontal", active=bottom_active)
                left = row[-1].wall_right if j > 0 else Wall(j * self.tile_size, i * self.tile_size, "vertical", active=left_active)
    
                tile = Tile(j * self.tile_size + 20, i * self.tile_size + 20,(j,i), up, right, down, left)
                row.append(tile)
    
            self.tiles.append(row)


    def __init_pawns(self):
        self.pawns = []
        for player_count in range(self.players):
            if player_count == 0:
                x = self.size // 2
                y = self.size - 1
                color = self.PLAYER_COLORS[player_count]
            elif player_count == 1:
                x = self.size // 2
                y = 0
                color = self.PLAYER_COLORS[player_count]
            elif player_count == 2:
                x = self.size - 1
                y = self.size // 2
                color = self.PLAYER_COLORS[player_count]
            else:
                x = 0
                y = self.size // 2
                color = self.PLAYER_COLORS[player_count]
            self.pawns.append(Pawn(x, y, color))


    def draw_walls(self, win): #TODO : Change the name
        for row in self.tiles:
            for tile in row:
                tile.draw(win)
                for pawn in self.pawns:
                    if pawn.x == tile.x_index and pawn.y == tile.y_index:
                        tile.pawn = pawn
                    elif tile.pawn is not None and (pawn.x != tile.x_index or pawn.y != tile.y_index) and tile.pawn == pawn:
                        tile.pawn = None

    def draw_pawns(self, win):
        self.win = win
        for pawn in self.pawns:
            pawn.draw_on_tile(win, self.tiles[pawn.y][pawn.x])

    def get_neighbor(self, x, y, orientation):
        if orientation == 1 or orientation == 3:
            if y < self.size - 1: #TODO : hard coded 6
                return self.tiles[y+1][x].GetWalls()[orientation]
            else:
                return self.tiles[y-1][x].GetWalls()[orientation]
        else:
            if x < self.size - 1:
                return self.tiles[y][x+1].GetWalls()[orientation]
            else:
                return self.tiles[y][x-1].GetWalls()[orientation]
    
    def get_neighbor_tile(self, x, y, orientation):
        if orientation == 1 or orientation == 3:
            if y < self.size - 1: #TODO : hard coded 6
                return self.tiles[y+1][x].GetWalls()[orientation]
            else:
                return self.tiles[y-1][x].GetWalls()[orientation]
        else:
            if x < self.size - 1:
                return self.tiles[y][x+1].GetWalls()[orientation]
            else:
                return self.tiles[y][x-1].GetWalls()[orientation]
    
    def is_move_possible(self, tile, player_number):
        if tile.pawn is None:
            pawn = self.pawns[player_number]
            diff_x = abs(tile.x_index - pawn.x)
            diff_y = abs(tile.y_index - pawn.y)

            is_horizontal_move = (diff_x == 1) and (tile.y_index == pawn.y)
            is_vertical_move = (diff_y == 1) and (tile.x_index == pawn.x)


            # check if there's a wall in the way
            if is_horizontal_move:
                if pawn.x <= tile.x_index: # moving right
                    if tile.x_index <= self.size - 1:
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
                    if tile.y_index <= self.size - 1:
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
            x_diff = tile.x_index - self.pawns[player_number].x #TODO : code repetition
            y_diff = tile.y_index - self.pawns[player_number].y

            # Get the coordinates of the tile behind the other pawn
            next_x = tile.x_index + x_diff
            next_y = tile.y_index + y_diff

            # Check that the tile behind the other pawn exists and doesn't have a pawn on it
            if next_x >= 0 and next_x < self.size and next_y >= 0 and next_y < self.size and self.tiles[next_y][next_x].pawn is None:
                # Check for walls between the player's pawn and the other pawn,
                # as well as between the other pawn and the tile behind it
                if x_diff == 0:  # vertical jump
                    no_wall_between = (not tile.wall_up.placed and not tile.wall_down.placed) if y_diff < 0 else (not tile.wall_down.placed and not self.tiles[next_y][next_x].wall_up.placed)
                else:  # horizontal jump
                    no_wall_between = (not tile.wall_left.placed and not tile.wall_right.placed) if x_diff < 0 else (not tile.wall_right.placed and not self.tiles[next_y][next_x].wall_left.placed)

                if no_wall_between:
                    return True


        return False
    

    def is_wall_placeable(self, tile, orientation):

        neighbor = self.get_neighbor(tile.x_index, tile.y_index, orientation)

        if neighbor.placed:
            return False
        
        if (orientation == 1 or orientation == 3) and tile.wall_down.placed:
            return False
        elif (orientation == 2 or orientation == 0) and tile.wall_right.placed:
            return False
        
        return True
    
    def is_winner(self, player_number):
        if player_number == 0:
            return self.pawns[player_number].y == 0
        elif player_number == 1:
            return self.pawns[player_number].y == self.size - 1
        elif player_number == 2:
            return self.pawns[player_number].x == 0
        else:
            return self.pawns[player_number].x == self.size - 1
    
    def is_move_possible_bfs(self, start_tile, end_tile):
        diff_x = abs(start_tile.x_index - end_tile.x_index)
        diff_y = abs(start_tile.y_index - end_tile.y_index)
        is_horizontal_move = (diff_x == 1) and (start_tile.y_index == end_tile.y_index)
        is_vertical_move = (diff_y == 1) and (start_tile.x_index == end_tile.x_index)

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

        
    def get_possible_neighbors(self, tile):
        neighbors = []
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]

        # check if not out of bounds
        for i in range(4):
            x = tile.x_index + dx[i]
            y = tile.y_index + dy[i]
            if x >= 0 and x < self.size and y >= 0 and y < self.size:
                if self.is_move_possible_bfs(tile, self.tiles[y][x]):
                    neighbors.append(self.tiles[y][x])
        
        return neighbors

    def is_path_to_victory(self, player_number):
        starting_tile = self.tiles[self.pawns[player_number].y][self.pawns[player_number].x]
        reachable_tiles = [starting_tile]
        visited = [[False]*self.size for _ in range(self.size)]
        visited[starting_tile.y_index][starting_tile.x_index] = True

        queue = [starting_tile]

        while queue:
            current_tile = queue.pop(0)

            neighbors = self.get_possible_neighbors(current_tile)

            for neighbor in neighbors:
                if not visited[neighbor.y_index][neighbor.x_index]:
                    queue.append(neighbor)
                    reachable_tiles.append(neighbor)
                    visited[neighbor.y_index][neighbor.x_index] = True
        
        for i in reachable_tiles:
            if player_number == 0:
                if i.y_index == 0:
                    return True

        return False

