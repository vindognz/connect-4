import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, action, font, font_size, extra_data = None, rounding = 0):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.current_color = color
        self.action = action
        self.font = pygame.font.Font(font, font_size)
        self.extra_data = extra_data
        self.rounding = rounding

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=self.rounding)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def update_color(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action(self)
            
        self.update_color()
