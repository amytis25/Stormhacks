import pygame as pg
from button import Button

class StartScreen:
    def __init__(self, screen_size):
        self.width, self.height = screen_size
        self.button = Button("Start Game", (self.width // 2 - 100, self.height // 2 - 30), (200, 60))
        self.active = True  # Start screen active flag

    def draw(self, surface):
        surface.fill((150, 0, 200))  # Purple background
        self.button.draw(surface)
        pg.display.flip()

    def handle_events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                return "QUIT"
            if self.button.is_clicked(event):
                self.active = False
                return "START"
        return None
