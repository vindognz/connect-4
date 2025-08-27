import pygame
from pathlib import Path

class Button:
    def __init__(self, x, y, width, height, text, colour, hover_colour, text_colour, action, font, font_size, extra_data=None, rounding=0, outline_colour=None, outline_width=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        self.current_colour = colour
        self.action = action
        self.extra_data = extra_data
        self.rounding = rounding
        self.outline_colour = outline_colour
        self.outline_width = outline_width

        if isinstance(font, pygame.font.Font):
            self.font = font
        elif isinstance(font, (str, Path)):
            if font_size is None:
                raise ValueError("font_size must be given when passing a font path")
            self.font = pygame.font.Font(str(font), font_size)
        else:
            self.font = pygame.font.Font(None, font_size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_colour, self.rect, border_radius=self.rounding)
        
        if self.outline_colour and self.outline_width > 0:
            pygame.draw.rect(screen, self.outline_colour, self.rect, width=self.outline_width, border_radius=self.rounding)

        if self.text:
            text_surface = self.font.render(self.text, True, self.text_colour)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def update_colour(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.current_colour = self.hover_colour
        else:
            self.current_colour = self.colour

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            if self.action:
                self.action(self)
        self.update_colour()
