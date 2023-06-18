from Game.elements.window import NewWindow
from Game.inputs.events import event_loop
from Game.state.structs import GameStructs
from pygame import init, quit as pygame_quit
from Game.elements.board import Board
from Game.elements.game_info import info
from Game.game_events.local_game import LocalGame
from Game.elements.menu import Menu
from Game.elements.win_popup import WinPopup
from typing import Any
import asyncio


async def game_logic(struct: Any) -> None:
    """
    Executes the game logic. This function initializes game properties, renders
    the board and game elements, and handles user inputs and AI moves.
    
    This function is asynchronous and should be called within an event loop.
    
    :param struct: A data structure containing various game attributes and settings.
    """
    
    # Initialize game properties through a menu selection
    game_properties = Menu(struct).select_game_options()
    
    # Create a local game instance and initialize the board size, number of players, walls, and wall counter
    local_game = LocalGame(struct)
    local_game.init_board_size(game_properties[0])
    local_game.init_number_of_players(game_properties[1])
    local_game.init_number_of_walls(game_properties[2])
    local_game.init_wall_counter()
    
    # Create a new window for the game
    window = NewWindow(struct.WIDTH, struct.HEIGHT, "Game")
    
    # Initialize game information to be displayed on the screen
    infos = info(struct, window.get_window())

    # Create a game board
    b = Board(struct)
    
    # Initialize AI bots if any
    local_game.init_bots(game_properties[3], b)
    
    # Main game loop
    while struct.is_running:
        
        # Draw board tiles
        b.draw_tiles(window.get_window())
        
        # Draw player pawns
        b.draw_pawns(window.get_window())
        
        # Display game info
        infos.show()

        # If it's AI bot's turn, make the bot play and switch turn
        if local_game.get_player_turn() in struct.bot_instances.keys():
            struct.bot_instances[local_game.get_player_turn()].play()
            local_game.switch_player_turn()

        # Handle mouse hover logic
        if not struct.mouse_position_queue.empty():
            mouse_position = struct.mouse_position_queue.get_nowait() # Get mouse position from the queue
            # Iterate through the board tiles
            for y, row in enumerate(b.tiles):
                for x, tile in enumerate(row):
                    if tile is not None and tile.get_rect().collidepoint(mouse_position):
                        # Highlight tile under the mouse if it's empty
                        if tile.pawn is None:
                            tile.hover()
                        break

                    # Handle wall hover logic
                    if local_game.get_wall_counter() > 0: # If there are walls left to place
                        for orientation, wall in enumerate(tile.GetWalls()):
                            # If wall is active, check if it can be placed
                            if wall is not None and wall.get_rect().collidepoint(mouse_position) and wall.active:
                                if struct.hovered_wall == False: # If no wall is hovered to avoid double hover
                                    struct.hovered_wall = True
                                    neighbor = b.get_neighbor(x, y, orientation) # Get the neighbor tile to make a wall of size 2
                                    if b.is_wall_placeable(tile, orientation):
                                        # Highlight the wall and its neighbor if it can be placed
                                        wall.hover(window.get_window())
                                        neighbor.hover(window.get_window())
                                    break
            struct.hovered_wall = False # Reset the flag to allow hovering again
        
        # Handle mouse clicks and input logic
        if not struct.input_queue.empty():
            inputs = struct.input_queue.get_nowait() # Get mouse click inputs from the queue
            # Iterate through the board tiles
            for y, row in enumerate(b.tiles):
                for x, tile in enumerate(row):
                    # If a tile is clicked and it's empty, move the player pawn to that tile
                    if tile is not None and tile.get_rect().collidepoint(inputs):
                        if b.is_move_possible(tile, local_game.get_player_turn()):
                            b.pawns[local_game.get_player_turn()].move(tile)

                            if b.is_winner(local_game.get_player_turn()): # If the player has won, display a win message and end the game
                                WinPopup(__file__).display(struct.WIN_MESSAGE.format(local_game.get_player_turn() + 1))
                                local_game.game_over()
                                break

                            local_game.switch_player_turn()
                            break
                    
                    # Handle wall placement logic
                    if local_game.get_wall_counter() > 0: # If there are walls left to place
                        if struct.placed_wall == False: # If no wall is placed to avoid double placement
                            for orientation, wall in enumerate(tile.GetWalls()): # Iterate through the walls of the tile

                                if wall is not None and wall.get_rect().collidepoint(inputs) and wall.active:
                                    neighbor = b.get_neighbor(x, y, orientation) # Get the neighbor tile to make a wall of size 2
                                    if b.is_wall_placeable(tile, orientation):
                                        struct.placed_wall = True # Set the flag to avoid double placement
                                        wall.place()
                                        neighbor.place()
                                        # Remove the wall if it block a player's path to victory
                                        if not b.is_path_to_victory_for_all_players():
                                            wall.remove()
                                            neighbor.remove()
                                            break
                                        local_game.decrement_wall_counter()
                                        local_game.switch_player_turn()
                                    break

            struct.placed_wall = False
        
        # Update the window and sleep for a short duration
        window.update()
        await asyncio.sleep(0.01)


async def main() -> None:
    """
    The main entry point for the game.

    This function creates two tasks to run concurrently: an event loop task and a game logic task.
    It then waits for both tasks to complete.

    If either task raises an exception, this function cancels both tasks and waits for them to complete again
    with return_exceptions=True to suppress any exceptions.

    Finally, this function calls pygame_quit to cleanly exit the Pygame application.
    """
    # Create a GameStructs object to hold the game state
    struct = GameStructs()

    # Create tasks for the event loop and game logic
    event_task = asyncio.create_task(event_loop(struct))
    game_logic_task = asyncio.create_task(game_logic(struct))

    try:
        # Wait for both tasks to complete
        await asyncio.gather(game_logic_task, event_task)
    except asyncio.CancelledError:
        pass
    finally:
        # If either task is not done, cancel it
        if not game_logic_task.done():
            game_logic_task.cancel()
        if not event_task.done():
            event_task.cancel()

        # Wait for both tasks to complete again with return_exceptions=True to suppress any exceptions
        await asyncio.gather(game_logic_task, event_task, return_exceptions=True)

        # Cleanly exit the Pygame application
        pygame_quit()


if __name__ == "__main__":
    init()
    asyncio.run(main())
