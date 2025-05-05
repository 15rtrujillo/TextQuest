from collections import deque

import pygame as pg


class TextToAdd:
    """Text to be added to the screen"""

    def __init__(self, text: str):
        """
        An object that stores text to add to the screen
        :param str text: The text to add
        """
        self.text = text
        self.index: int = -1


class TextToTypewrite(TextToAdd):
    """Text to be typewritten to the screen"""

    def __init__(self, text: str, delay: int):
        """
        An object that stores text to typewrite to the screen
        :param str text: The text to add
        :param int delay: The delay between adding each character to the screen (in milliseconds)
        """
        super().__init__(text)
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

    def add(self, text_to_add: TextToAdd):
        """
        Add text to the queue to be added to the screen
        :param TextToAdd text_to_add: The text object to be added to the queue
        """
        self.queue.append(text_to_add)

    def clear(self):
        self.queue.clear()
        self.displayed_lines.clear()

    def update(self):
        """Updates the display based on the text queue."""
        for item in list(self.queue):
            if isinstance(item, TextToTypewrite):
                current_time = pg.time.get_ticks()
                # If we aren't done typing out this item,
                # and enough time has passed, append another letter
                if not item.typing_complete and current_time - item.last_update_time > item.delay:
                    item.current_index += 1
                    item.last_update_time = current_time
                    # If we've reached the end of the text, we're done
                    if item.current_index >= len(item.text):
                        item.typing_complete = True
                # Create the surface
                text_to_render = item.text[:item.current_index]
                text_surface = self.font.render(text_to_render, True, self.text_color)
                # Remove the item if we're done typing it
                if item.typing_complete and item in self.queue:
                    self.queue.remove(item)
                if item.index == -1:
                    self.displayed_lines.append(text_surface)
                    item.index = len(self.displayed_lines) - 1
                else:
                    self.displayed_lines[item.index] = text_surface
            elif isinstance(item, TextToAdd):
                text_surface = self.font.render(item.text, True, self.text_color)
                if item.index == -1:
                    self.displayed_lines.append(text_surface)
                    item.index = len(self.displayed_lines) - 1
                else:
                    self.displayed_lines[item.index] = text_surface
                self.queue.remove(item)

    def draw(self):
        """Draws the currently displayed text on the screen."""
        y_offset = 5
        for line_surface in self.displayed_lines:
            text_rect = line_surface.get_rect(topleft=(self.padding, y_offset))
            self.screen.blit(line_surface, text_rect)
            y_offset += self.line_spacing
