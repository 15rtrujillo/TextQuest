from interface.screens.screen import Screen


class InfoScreen(Screen):
    """A screen that will return to the previous screen once the user presses enter."""

    def __init__(self, *text: str, return_screen: Screen):
        """
        Create a screen that displays text
        :param str text: The text to display
        :param Screen return_screen: The screen that should be displayed after pausing
        """
        super().__init__(*text, "", "Press ENTER to continue...")
        self.return_screen = return_screen

    def process_input(self, user_input: str) -> Screen:
        # We don't care what the user types in
        return self.return_screen
