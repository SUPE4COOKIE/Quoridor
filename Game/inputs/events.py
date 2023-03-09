import pygame
import asyncio

async def event_loop(struct):
    while True:
        # Get the next event from the queue
        event = pygame.event.wait()

        # Process the event
        if event.type == pygame.QUIT:
            # The user closed the window
            quit()

        # check if it's a click
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the left mouse button was clicked
            # TODO check if the click is on one of the element of the state struct
            if event.button == 1:
                # print the position of the click
                await struct.input_queue.put(event.pos)
