from Game.elements.window import NewWindow
from Game.inputs.events import event_loop
from Game.state.structs import GameStructs
from pygame import init, quit as pygame_quit
from Game.elements.board import Board
from Game.elements.game_info import info
from Game.game_events.local_game import LocalGame
from Game.elements.menu import Menu
import asyncio


async def game_logic(struct) -> None:
    
    game_propreties = Menu(struct).select_game_options()
    local_game = LocalGame(struct)
    local_game.init_board_size(game_propreties[0])
    local_game.init_number_of_players(game_propreties[1])
    local_game.init_number_of_walls(game_propreties[2])
    local_game.init_wall_counter()
    
    window = NewWindow(struct.WIDTH, struct.HEIGHT , "Game")
    infos = info(struct, window.get_window())

    b = Board(struct)
    local_game.init_bots(game_propreties[3],b)
    while struct.is_running:
        b.draw_walls(window.get_window())
        b.draw_pawns(window.get_window())
        infos.show()


        if local_game.get_player_turn() in struct.bot_instances.keys():
            struct.bot_instances[local_game.get_player_turn()].play()
            local_game.switch_player_turn()

        if not struct.mouse_position_queue.empty():
            mouse_position = struct.mouse_position_queue.get_nowait()
            for y, row in enumerate(b.tiles):
                for x, tile in enumerate(row):
                    if tile is not None and tile.get_rect().collidepoint(mouse_position):
                        if tile.pawn is None:
                            tile.hover()
                        break
                    if local_game.get_wall_counter() > 0:
                        for orientation, wall in enumerate(tile.GetWalls()):
                            if wall is not None and wall.get_rect().collidepoint(mouse_position) and wall.active:
                                if struct.hovered_wall == False:
                                    struct.hovered_wall = True
                                    neighbor = b.get_neighbor(x, y, orientation)
                                    if b.is_wall_placeable(tile, orientation):
                                        wall.hover(window.get_window(), (0, 255, 0))
                                        neighbor.hover(window.get_window(), (0, 255, 0))
                                    break
            struct.hovered_wall = False

        #TODO : merge both input queues in one function
        #TODO : replace all struct.something operation with local game operation
        if not struct.input_queue.empty():
            inputs = struct.input_queue.get_nowait()
            for y, row in enumerate(b.tiles):
                for x, tile in enumerate(row):
                    if tile is not None and tile.get_rect().collidepoint(inputs):
                        if b.is_move_possible(tile, local_game.get_player_turn()):
                            b.pawns[local_game.get_player_turn()].move(tile)
                            if b.is_winner(local_game.get_player_turn()):
                                print("Player {} wins".format(local_game.get_player_turn()))
                            local_game.switch_player_turn()
                            break
                    if local_game.get_wall_counter() > 0:
                        if struct.placed_wall == False:
                            for orientation, wall in enumerate(tile.GetWalls()):
                                if wall is not None and wall.get_rect().collidepoint(inputs) and wall.active:
                                    neighbor = b.get_neighbor(x, y, orientation)
                                    if b.is_wall_placeable(tile, orientation):
                                        struct.placed_wall = True
                                        wall.click()
                                        neighbor.click()
                                        print(b.is_path_to_victory(local_game.get_player_turn()), local_game.get_player_turn())
                                        local_game.decrement_wall_counter()
                                        local_game.switch_player_turn()
                                    break
            struct.placed_wall = False
        
            
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
