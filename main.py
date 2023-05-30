from Game.elements.window import NewWindow
from Game.inputs.events import event_loop
from Game.state.structs import GameStructs
from pygame import init, draw, quit as pygame_quit
from Game.elements.board import Board
import asyncio

async def game_logic(struct):
    window = NewWindow(825, 825, "Game")
    while struct.is_running:
        b = Board(7, 7, 2)
        b.draw_walls(window.get_window())
        b.draw_pawns(window.get_window())

        if not struct.mouse_position_queue.empty():
            mouse_position = struct.mouse_position_queue.get_nowait()
            for row in b.tiles:
                for tile in row:
                    for wall in tile.GetWalls():
                        if wall is not None and wall.get_rect().collidepoint(mouse_position) and wall.active:
                            if struct.hovered_wall == None:
                                struct.hovered_wall = wall
                                wall.hover(window.get_window(), (0, 255, 0))
                                break
            struct.hovered_wall = None


        if not struct.input_queue.empty():
            inputs = struct.input_queue.get_nowait()
            for pawn in b.pawns:
                if pawn is not None and pawn.get_circle().collidepoint(inputs):
                    print("pawn clicked")
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
