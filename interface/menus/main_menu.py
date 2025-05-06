from constants import game_info
from interface.screens.numbered_menu_screen import NumberedMenuScreen
from interface.screens.screen import Screen


class MainMenu(NumberedMenuScreen):
    """
    The main menu.
    Presented to the player on game start.
    """

    def __init__(self):
        """Initialize the main menu"""
        prompt = f"""{game_info.TITLE}: {game_info.SUBTITLE}
{game_info.VERSION}

Main Menu:"""
        options = [
            "New Game",
            "Load Game",
            "About",
            "Exit"
        ]
        super().__init__(prompt, *options)

    def process_choice(self, choice: int) -> Screen:
        if choice == 1:
            print("Awesome!")
        elif choice == 2:
            print("Very cool")
