import pygame


class MultiLineText:
    def __init__(self, text, font, color, x, y, height, window):
        self.window = window

        self.font = pygame.font.Font(font, height)
        self.color = color
        self.lines = text.split('\n')
        self.x = x
        self.y = y
        self.height = height

    def show_image(self):
        for i, line in enumerate(self.lines):
            text_surface = self.font.render(line, True, self.color)
            self.window.blit(text_surface, (self.x, self.y + i * self.height))