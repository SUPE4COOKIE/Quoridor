from Game.elements.window import NewWindow
from Game.inputs.events import event_loop
from Game.state.structs import GameStructs
from pygame import init , draw , quit as pygame_quit
import asyncio


def rect(window):
    draw.rect(window.get_window(), (255, 0, 0), (0, 0, 100, 100))
    draw.rect(window.get_window(), (255, 0, 0), (100, 100, 100, 100))


async def game_logic(struct):
    window = NewWindow(800, 600, 'Game')
    while struct.is_running:
        rect(window)
        window.update()
        if not struct.input_queue.empty():
            print(await struct.input_queue.get())
        await asyncio.sleep(0.1)

async def main():
    struct = GameStructs(queue=asyncio.Queue())
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

if __name__ == '__main__':
    init()
    asyncio.run(main())

    
