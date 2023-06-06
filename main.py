from Game.elements.window import NewWindow
from Game.inputs.events import event_loop
from Game.state.structs import GameStructs
from pygame import init, quit as pygame_quit
from Game.elements.board import Board
from Game.elements.game_info import info
from local_game import LocalGame
import asyncio

async def game_logic(struct) -> None:
    # some menu to give back the number of players and the size of the board
    struct.NUMBER_OF_PLAYERS = 1
    struct.BOARD_SIZE = 7
    struct.INITIAL_WALL_COUNT = 40
    struct.WIDTH = 825
    struct.HEIGHT = 925
    # TODO : implement the choice instead of hard coded values
    window = NewWindow(struct.WIDTH, struct.HEIGHT , "Game")
    infos = info(struct, window.get_window())
    local_game = LocalGame(struct)
    local_game.init_wall_counter()

    b = Board(struct)
    while struct.is_running:
        b.draw_walls(window.get_window())
        b.draw_pawns(window.get_window())
        infos.show()

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
                                        local_game.decrement_wall_counter()
                                        local_game.switch_player_turn()
                                    break
            struct.placed_wall = False
        
            
        window.update()
        await asyncio.sleep(0.01)


async def main():
    struct = GameStructs()
    event_task = asyncio.create_task(event_loop(struct))
    game_logic_task = asyncio.create_task(game_logic(struct))

    try:
        await asyncio.gather(game_logic_task, event_task)
    except asyncio.CancelledError:
        pass
    finally:
        if not game_logic_task.done():
            game_logic_task.cancel()
        if not event_task.done():
            event_task.cancel()
        await asyncio.gather(game_logic_task, event_task, return_exceptions=True)
        pygame_quit()


if __name__ == "__main__":
    init()
    asyncio.run(main())
