from collections import deque


import pygame as pg


class TextToAdd:
    """Text to be added to the screen"""

    def __init__(self, text: str, end: str = "\n"):
        """
        An object that stores text to add to the screen
        :param str text: The text to add
        :param str end: The character to append to the end of the text
        """
        self.text = text
        self.end = end
        self.total_delay = 0

class TextToTypewrite(TextToAdd):
    """Text to be typewritten to the screen"""

    def __init__(self, text: str, delay: int, end: str = "\n"):
        """
        An object that stores text to typewrite to the screen
        :param str text: The text to add
        :param int delay: The delay between adding each character to the screen (in milliseconds)
        :param str end: The character to append to the end of the text
        """
        super().__init__(text, end)
        self.delay = delay
        self.current_index = 0
        self.last_update_time = 0
        self.typing_complete = False

class TextManager:
    """An object to manage the text that gets added to the screen"""

    def __init__(self, screen: pg.Surface, font: pg.font.Font, text_color: str):
        """
        Create a new Text Manager
        :param pg.Surface screen: The PyGame screen surface
        :param pg.font.Font font: The font to use for rendering text
        :param str text_color: The color of the text
        """
        self.screen = screen
        self.font = font
        self.text_color = text_color
        self.queue: deque[TextToAdd] = deque()
        self.displayed_lines: list[pg.Surface] = []
        self.line_spacing = 25
        self.padding = 10

    def add(self, text_obj: TextToAdd):
        """
        Add text to the queue to be added to the screen
        :param TextToAdd text_obj: The text object to be added to the queue
        """
        self.queue.append(text_obj)

    def update(self):
        """Updates the display based on the text queue."""
        new_lines = []
        for item in list(self.queue):  # Iterate over a copy to allow removal
            if isinstance(item, TextToTypewrite):
                current_time = pg.time.get_ticks()
                if not item.typing_complete and current_time - item.last_update_time > item.delay:
                    item.current_index += 1
                    item.last_update_time = current_time
                    if item.current_index >= len(item.text):
                        item.typing_complete = True
                text_to_render = item.text[:item.current_index] + (item.end if item.typing_complete else "")
                text_surface = self.font.render(text_to_render, True, self.text_color)
                if item.typing_complete and item in self.queue:
                    self.queue.remove(item)
                new_lines.append(text_surface)
            elif isinstance(item, TextToAdd):
                text_surface = self.font.render(item.text + item.end, True, self.text_color)
                new_lines.append(text_surface)
                self.queue.remove(item)
        self.displayed_lines.extend(new_lines)

    def draw(self):
        """Draws the currently displayed text on the screen."""
        y_offset = self.screen.get_height() - 100  # Start drawing text above the input box
        for line_surface in reversed(self.displayed_lines):
            text_rect = line_surface.get_rect(bottomleft=(self.padding, y_offset))
            self.screen.blit(line_surface, text_rect)
            y_offset -= self.line_spacing