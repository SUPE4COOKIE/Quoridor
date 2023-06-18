import pygame
from typing import List, Tuple, Union
from Game.elements.window import NewWindow


class Menu:
    def __init__(self, struct: object) -> None:
        """
        Initialize the Menu class.

        :param struct: An object containing game configuration data such as board sizes, number of players, etc.
        """
        pygame.init()
        self.struct = struct
        self.BOARD_SIZES = struct.BOARD_SIZES # Available board sizes
        self.NUMBERS_OF_PLAYERS = struct.NUMBERS_OF_PLAYERS # Available number of players
        self.NUMBERS_OF_BARRIERS = struct.NUMBERS_OF_BARRIERS  # Multiples of 4 from 4 to 40
        self.MAX_NUMBER_OF_BARRIERS = struct.MAX_NUMBER_OF_BARRIERS # limit the number of barrier based on the board size (index of each)
        self.NUMBERS_OF_BOTS = struct.NUMBERS_OF_BOTS # Available number of bots
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 400
        self.SCREEN = NewWindow(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, "Board Game Menu").get_window()
        self.FONT = pygame.font.Font(None, 36)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.confirm_text = self.FONT.render("Confirm", True, self.WHITE)
        self.confirm_rect = pygame.Rect((self.SCREEN_WIDTH-150, self.SCREEN_HEIGHT-50), (100, 40))
        self.LABEL_FONT = pygame.font.Font(None, 24)
        self.finished = False

    def select_game_options(self) -> Union[Tuple[int, int, int, int], None]:
        """
        Display and handle a menu that allows the player to select various game options.

        :return: A tuple of selected game options, or None if the menu is exited without making a selection.
        """

        clock = pygame.time.Clock()
        selected_board_size_index = 2 # default value of 9x9
        selected_number_of_players_index = 0 # default value of 2 players
        selected_number_of_barriers_index = 4 # default value of 20 barriers
        selected_number_of_bots_index = 0 # default value of 0 bots

        while not self.finished:
            self.SCREEN.fill(self.BLACK)

            # Displaying the labels
            board_size_label = self.LABEL_FONT.render("Board Size", True, self.WHITE)
            self.SCREEN.blit(board_size_label, (self.SCREEN_WIDTH/2 - 230, self.SCREEN_HEIGHT/2 - 150))

            number_of_players_label = self.LABEL_FONT.render("Players", True, self.WHITE)
            self.SCREEN.blit(number_of_players_label, (self.SCREEN_WIDTH/2 - 130, self.SCREEN_HEIGHT/2 - 150))

            number_of_barriers_label = self.LABEL_FONT.render("Barriers", True, self.WHITE)
            self.SCREEN.blit(number_of_barriers_label, (self.SCREEN_WIDTH/2 - 30, self.SCREEN_HEIGHT/2 - 150))

            number_of_bots_label = self.LABEL_FONT.render("Bots", True, self.WHITE)
            self.SCREEN.blit(number_of_bots_label, (self.SCREEN_WIDTH/2 + 70, self.SCREEN_HEIGHT/2 - 150))


            # events handling to select the options
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for index, rect in enumerate(self.board_size_rects):
                        if rect.collidepoint(x, y):
                            selected_board_size_index = index
                    for index, rect in enumerate(self.number_of_players_rects):
                        if rect.collidepoint(x, y):
                            selected_number_of_players_index = index
                    for index, rect in enumerate(self.barriers_rects):
                        if rect.collidepoint(x, y):
                            selected_number_of_barriers_index = index
                    for index, rect in enumerate(self.bots_rects):
                        if rect.collidepoint(x, y):
                            selected_number_of_bots_index = index
                    if self.confirm_rect.collidepoint(x, y):
                        # Once the options has been selected return the values
                        pygame.quit()
                        return (
                            int(self.BOARD_SIZES[selected_board_size_index][0] if self.BOARD_SIZES[selected_board_size_index][0] != '1' else self.BOARD_SIZES[selected_board_size_index][0:2]),
                            int(self.NUMBERS_OF_PLAYERS[selected_number_of_players_index]),
                            int(self.NUMBERS_OF_BARRIERS[selected_number_of_barriers_index]),
                            int(self.NUMBERS_OF_BOTS[selected_number_of_bots_index])
                        )

            # Render the options in the available board size list
            self.board_size_rects = []
            for index, board_size in enumerate(self.BOARD_SIZES):
                if index == selected_board_size_index:
                    text = self.FONT.render(board_size, True, self.GREEN)
                else:
                    text = self.FONT.render(board_size, True, self.WHITE)
                rect = self.SCREEN.blit(text, (self.SCREEN_WIDTH/2 - 220, self.SCREEN_HEIGHT/2 - 100 + index*30))
                self.board_size_rects.append(rect)

            # Render the options in the available number of players list
            self.number_of_players_rects = []
            for index, number_of_players in enumerate(self.NUMBERS_OF_PLAYERS):
                if index == selected_number_of_players_index:
                    text = self.FONT.render(number_of_players, True, self.GREEN)
                else:
                    text = self.FONT.render(number_of_players, True, self.WHITE)
                rect = self.SCREEN.blit(text, (self.SCREEN_WIDTH/2 - 120, self.SCREEN_HEIGHT/2 - 100 + index*30))
                self.number_of_players_rects.append(rect)

            # Render the options in the available number of barriers list
            self.barriers_rects = []
            # The number of barriers is restricted based on the board size
            for i in range(self.MAX_NUMBER_OF_BARRIERS[selected_board_size_index]):
                if i == selected_number_of_barriers_index:
                    text = self.FONT.render(self.NUMBERS_OF_BARRIERS[i], True, self.GREEN)
                else:
                    text = self.FONT.render(self.NUMBERS_OF_BARRIERS[i], True, self.WHITE)
                rect = self.SCREEN.blit(text, (self.SCREEN_WIDTH/2 - 20, self.SCREEN_HEIGHT/2 - 100 + i*30))
                self.barriers_rects.append(rect)

            # Render the options in the available number of bots list
            self.bots_rects = []
            # Restrict the number of bots based on the number of players
            number_of_bots_to_display = 2 if selected_number_of_players_index == 0 else 3
            for i in range(number_of_bots_to_display):
                if i == selected_number_of_bots_index:
                    text = self.FONT.render(self.NUMBERS_OF_BOTS[i], True, self.GREEN)
                else:
                    text = self.FONT.render(self.NUMBERS_OF_BOTS[i], True, self.WHITE)
                rect = self.SCREEN.blit(text, (self.SCREEN_WIDTH/2 + 80, self.SCREEN_HEIGHT/2 - 110 + i*30))
                self.bots_rects.append(rect)

            pygame.draw.rect(self.SCREEN, self.GREEN, self.confirm_rect) # Confirm button
            self.SCREEN.blit(self.confirm_text, self.confirm_rect)
            clock.tick(60)
            pygame.display.update()
