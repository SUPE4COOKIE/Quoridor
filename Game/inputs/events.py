import pygame
import asyncio
from typing import Any

async def event_loop(struct: Any) -> None:
    """
    This function handles user inputs and adds them to the input queue.
    :param struct: A data structure containing various game attributes and settings.
    """
    while struct.is_running:
        # Get the list of events from the queue
        events = pygame.event.get()

        for event in events:
            # Process the event
            if event.type == pygame.QUIT:
                struct.is_running = False
                break

            # check if it's a click
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if the left mouse button was clicked
                if event.button == 1:
                    # add the position of the click to the queue
                    await struct.input_queue.put(event.pos)
                    
        struct.mouse_position_queue.put_nowait(pygame.mouse.get_pos()) # Add the mouse position to the queue
        await asyncio.sleep(0.01)
