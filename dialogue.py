import pygame
from multiline_text import MultiLineText


pygame.init()
class Dialogue:
    def __init__(self, window, x, y, height, width, text, shift_x=10, shift_y=10) -> None:
        self.window = window
        self.x = x
        self.y = y
        self.height, self.width = height, width
        self.text = text
        self.shift_x, self.shift_y = shift_x, shift_y
        self.label = MultiLineText(x=self.x+self.shift_x, y=self.y+self.shift_y,
                                    height=22, font='font.ttf', color=(0, 0, 0), text=self.text, window=window)
        
    def show_rect(self):
        pygame.draw.rect(self.window, (255, 255, 255), (self.x, self.y, self.width, self.height), border_radius=20)
        pygame.draw.rect(self.window, (0, 0, 0), (self.x, self.y, self.width, self.height), 3, 20)
        self.label.show_image()

