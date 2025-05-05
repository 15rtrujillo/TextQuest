from interface.text_manager import TextManager, TextToAdd, TextToTypewrite


import pygame as pg


class GameWindow:
    """The main game window"""

    def __init__(self):
        """Create the main game window"""
        self.window_x = 960
        self.window_y = 540
        self.screen = pg.display.set_mode((self.window_x, self.window_y))
        pg.display.set_caption("Epic Quest: Text Quest")
        self.bg_color = "black"
        self.text_color = "white"
        self.font = pg.font.SysFont("Consolas", 20)
        self.input_text = ""
        self.active = True
        self.text_manager = TextManager(self.screen, self.font, self.text_color)

        # Insertion point
        self.insertion_point_visible = True
        self.insertion_point_last_blink = 0
        self.insertion_point_interval = 500
        self.insertion_point_height = self.font.get_linesize() - 18
        self.insertion_point_width = 15

        # Backspace
        self.backspace_held = False
        self.backspace_timer = 0
        self.backspace_delay = 200
        self.backspace_repeat_rate = 50


    def display_text(self, text: str, end: str = "\n"):
        """Adds text to the display log immediately.
        :param str text: The text to add
        :param str end: The character to append to the end of the text"""
        self.text_manager.add(TextToAdd(text, end))

    def display_typewritten_text(self, text: str, delay: int, end: str = "\n"):
        """Adds text to the queue to be displayed with a typewriting effect.
        :param str text: The text to add
        :param int delay: The delay between adding each character to the screen (in milliseconds)
        :param str end: The character to append to the end of the text"""
        self.text_manager.add(TextToTypewrite(text, delay, end))

    def get_text(self) -> str:
        """Gets the current input text and clears the input.
        :rtype: str
        :return: The text the user has entered"""
        submitted_text = self.input_text
        self.input_text = ""
        return submitted_text
    
    def backspace(self):
        """Called when the backspace key is pressed"""
        if self.input_text:
            self.input_text = self.input_text[:-1]

    def key_typed(self, unicode: str):
        """Called when any alphanumeric key is pressed
        :param str unicode: The unicode for the pressed key"""
        self.input_text += unicode

    def update(self):
        """Update the window"""
        current_time = pg.time.get_ticks()

        self.text_manager.update()

        # Blink insertion point
        if current_time - self.insertion_point_last_blink > self.insertion_point_interval:
            self.insertion_point_visible = not self.insertion_point_visible
            self.insertion_point_last_blink = current_time

        # Delete multiple characters
        if self.backspace_held and current_time >= self.backspace_timer and self.input_text:
            self.backspace()
            self.backspace_timer = current_time + self.backspace_repeat_rate

    def draw(self):
        """Draws the screen"""
        self.screen.fill(self.bg_color)
        self.text_manager.draw()

        # Display the input text
        input_surface = self.font.render(f"> {self.input_text}", True, self.text_color)
        input_rect = input_surface.get_rect(bottomleft=(10, self.window_y - 10))
        self.screen.blit(input_surface, input_rect)

        if self.insertion_point_visible:
            cursor_x = input_rect.right + 2
            cursor_y = input_rect.top + 10
            pg.draw.rect(self.screen, self.text_color, (cursor_x, cursor_y, self.insertion_point_width, self.insertion_point_height))
