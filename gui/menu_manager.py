import pygame

class MenuManager:
    def __init__(self, display, bg_colour, menus=None):
        self.display = display
        self.bg_colour = bg_colour
        self.menus = menus or {}
        self.current_menu = None

    def change_menu(self, name):
        if name not in self.menus:
            raise ValueError(f"Menu '{name}' not registered")
        self.current_menu = name

    def register_menu(self, name, buttons=None, draw=None):
        self.menus[name] = {
            "buttons": buttons or [],
            "draw": draw
        }

    def handle_event(self, event):
        if not self.current_menu:
            return
        buttons = self.menus[self.current_menu]["buttons"]

        # handle dynamic buttons (function returning list)
        if callable(buttons):
            buttons = buttons()

        for b in buttons:
            b.handle_event(event)

    def draw(self):
        if not self.current_menu:
            return
        buttons = self.menus[self.current_menu]["buttons"]
        draw_callback = self.menus[self.current_menu]["draw"]

        if callable(buttons):
            buttons = buttons()

        for b in buttons:
            b.draw(self.display)

        if draw_callback:
            draw_callback(self.display)
