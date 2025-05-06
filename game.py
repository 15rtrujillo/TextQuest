import pygame as pg

from interface.game_window import GameWindow
from interface.menus.main_menu import MainMenu
from interface.screens.screen import Screen
from model.entity.player import Player
from model.world.world import World


class Game:
    """The game engine"""
    TICK_RATE: int = 100

    def __init__(self):
        """Create an instance of the game engine"""
        self.world = World()
        self.window = GameWindow()
        self.player: Player | None = None
        self.current_screen: Screen = MainMenu()
        self.next_screen: Screen | None = None
        self.running = True

        self.display_current_screen()

    def run(self):
        """Run the main game loop"""
        while self.running:
            current_time = pg.time.get_ticks()

            # Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                        self.process_input(self.window.get_text())
                    elif event.key == pg.K_BACKSPACE:
                        self.window.backspace_held = True
                        self.window.backspace()
                        # If backspace is held for longer than backspace_delay ms,
                        # we want to start deleting multiple characters
                        self.window.backspace_timer = current_time + self.window.backspace_delay
                    else:
                        self.window.key_typed(event.unicode)
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_BACKSPACE:
                        self.window.backspace_held = False

            # Updates
            self.window.update()

            # Drawing
            self.window.draw()
            pg.display.flip()

        pg.quit()

    def display_current_screen(self):
        self.window.clear()
        for line in self.current_screen.text:
            self.window.display_text(line)

    def process_input(self, user_input: str):
        if self.current_screen:
            self.next_screen = self.current_screen.process_input(user_input)
            if self.next_screen:
                self.current_screen = self.next_screen
                self.next_screen = None
                self.display_current_screen()
        else:
            raise RuntimeError("No current screen")


def validate_text_input(text_to_validate: str, allowed_responses: list[str],
                        case_sensitive: bool = False, partial_match: bool = False) -> bool:
    """
    Validates text input
    :param str text_to_validate: The text to validate
    :param list[str] allowed_responses: If this is not None, the user's input will be checked against a list of
    allowed responses. If the user enters an invalid response, they will be prompted to try again
    :param bool case_sensitive: All string comparisons will be case-sensitive if this is set
    :param bool partial_match: Checks if the text is a substring of one of the allowed responses
    :rtype: bool
    :return: True if the input is valid according to the conditions specified, False otherwise
    """
    # If we don't care about validating the response
    # But then what is the point of calling this function?
    if allowed_responses is None:
        return True

    for allowed_response in allowed_responses:
        if case_sensitive:
            if partial_match and text_to_validate in allowed_response:
                return True

            elif text_to_validate == allowed_response:
                return True

        else:
            if partial_match and text_to_validate.casefold() in allowed_response.casefold():
                return True

            elif text_to_validate.casefold() == allowed_response.casefold():
                return True

    return False
