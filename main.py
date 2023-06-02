from Game.elements.window import NewWindow
from Game.inputs.events import event_loop
from Game.state.structs import GameStructs
from pygame import init, draw, quit as pygame_quit
from Game.elements.board import Board
import asyncio

async def game_logic(struct):
    window = NewWindow(925, 925, "Game")
    b = Board(7, 7, 1)
    while struct.is_running:
        b.draw_walls(window.get_window())
        b.draw_pawns(window.get_window())

        if not struct.mouse_position_queue.empty():
            mouse_position = struct.mouse_position_queue.get_nowait()
            for y, row in enumerate(b.tiles):
                for x, tile in enumerate(row):
                    if tile is not None and tile.get_rect().collidepoint(mouse_position):
                        if tile.pawn is None:
                            tile.hover()
                        break
                    for orientation, wall in enumerate(tile.GetWalls()):
                        if wall is not None and wall.get_rect().collidepoint(mouse_position) and wall.active:
                            if struct.hovered_wall == None:
                                struct.hovered_wall = wall
                                neighbor = b.get_neighbor(x, y, orientation)
                                if b.is_wall_placeable(tile, orientation):
                                    wall.hover(window.get_window(), (0, 255, 0))
                                    neighbor.hover(window.get_window(), (0, 255, 0))
                                break
            struct.hovered_wall = None


        if not struct.input_queue.empty():
            inputs = struct.input_queue.get_nowait()
            for y, row in enumerate(b.tiles):
                for x, tile in enumerate(row):
                    if tile is not None and tile.get_rect().collidepoint(inputs):
                        if tile.pawn is None:
                            if b.is_move_possible(tile, 0): #TODO : hard coded 0
                                b.pawns[0].move(tile)
                                break
                    for orientation, wall in enumerate(tile.GetWalls()):
                        if wall is not None and wall.get_rect().collidepoint(inputs) and wall.active:
                            neighbor = b.get_neighbor(x, y, orientation)
                            if b.is_wall_placeable(tile, orientation):
                                wall.click()
                                neighbor.click()
                            break
            
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
