# Game.inputs.events
import pygame
import asyncio

async def event_loop(struct):
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
                    # print the position of the click
                    await struct.input_queue.put(event.pos)
        await asyncio.sleep(0.01)
