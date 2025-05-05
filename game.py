import pygame as pg

from interface.game_window import GameWindow
from model.entity.player import Player
from model.world.world import World


class Game:
    """The game engine"""
    TICK_RATE: int = 100

    def __init__(self):
        """Create an instance of the game engine"""
        self.world: World = World()
        self.player: Player | None = None
        self.window: GameWindow = GameWindow()
        self.running = True

    def run(self):
        """Run the main game loop"""
        while self.running:
            current_time = pg.time.get_ticks()

            # Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.window.get_text()
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


def parse_int_input(text_to_parse: str, number_of_choices: int = 0) -> int:
    """
    Parses int input
    :param str text_to_parse: The text to parse
    :param int number_of_choices: If this is not 0, the parsed int will be range checked form one to this value
    (inclusive)
    :rtype: int
    :return: The user's input as an int. -1 will be returned if the input is invalid in some way
    """
    try:
        int_input = int(text_to_parse)
        if number_of_choices == -1:
            return int_input
        if int_input in range(1, number_of_choices + 1):
            return int_input
        else:
            return -1
    except ValueError:
        return -1


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
