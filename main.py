from Game.interface.window import NewWindow
from Game.inputs.events import event_loop
from Game.state.structs import GameStructs
from pygame import init , draw
import asyncio


def rect(window):
    draw.rect(window.get_window(), (255, 0, 0), (0, 0, 100, 100))
    draw.rect(window.get_window(), (255, 0, 0), (100, 100, 100, 100))


async def game_logic(struct):
    window = NewWindow(800, 600, 'Game')
    while True:
        rect(window)
        window.update()
        if not struct.input_queue.empty():
            print("test")
            print(await struct.input_queue.get())
        await asyncio.sleep(0.1)

async def main():
    struct = GameStructs(queue=asyncio.Queue())
    event_task = asyncio.create_task(event_loop(struct)) # create the event loop task
    try:
        await game_logic(struct) # Run the main game loop
    finally: # Cancel the event loop task if the main loop exits
        event_task.cancel() # Cancel the event loop task
    await event_task # Wait for the event loop task to exit

if __name__ == '__main__':
    init()
    asyncio.run(main())
    
