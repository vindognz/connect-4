import pygame

class MenuManager:
    def __init__(self, display, bg_color):
        self.display = display
        self.bg_color = bg_color
        self.current_menu = None
        self.event_handlers = {}
        self.draw_handlers = {}

    # switch menu, and clear the screen
    def change_menu(self, name):
        if name not in self.draw_handlers:
            raise ValueError(f"Menu: '{name} not registered")
        self.current_menu = name
        self.display.fill(self.bg_color)

    # register a menus event and draw functions
    def register_menu(self, name, event_handler, draw_handler):
        self.event_handlers[name] = event_handler
        self.draw_handlers[name] = draw_handler

    # pass event to the menu handler
    def handle_event(self, event):
        if self.current_menu in self.event_handlers:
            self.event_handlers[self.current_menu](event)

    # draw the current menu
    def draw(self):
        if self.current_menu in self.draw_handlers:
            self.draw_handlers[self.current_menu]()
