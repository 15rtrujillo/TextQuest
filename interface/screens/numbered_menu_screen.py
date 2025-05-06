from abc import abstractmethod

from interface.screens.error_screen import InfoScreen
from interface.screens.screen import Screen


class NumberedMenuScreen(Screen):
    """A numbered menu where the user can select a specific option"""

    def __init__(self, prompt: str, *options: str):
        """
        Create a menu that displays a list of numbered options to the user
        :param str prompt: The text for the menu, not including the options
        :param tuple[str] options: The possible options the user can select.
        Do not number the options.
        """
        self.number_of_choices = len(options)
        super().__init__(*(prompt.split("\n") + [f"{i + 1}. {options[i]}" for i in range(self.number_of_choices)]))

    @abstractmethod
    def process_choice(self, choice: int) -> Screen:
        """
        Handle input from the user
        :param int choice: The user's numerical input
        :rtype: Screen
        :return: The next screen to transition to
        """
        pass

    def process_input(self, user_input: str) -> Screen:
        try:
            int_input = int(user_input)
            if int_input in range(1, self.number_of_choices + 1):
                return self.process_choice(int_input)
            else:
                return InfoScreen(f"Please enter a number within the range 1-{self.number_of_choices}", return_screen=self)
        except ValueError:
            return InfoScreen(f"Please enter a number", return_screen=self)
