import pygame as pg
from button import Button

class StartScreen:
    def __init__(self, screen_size):
        self.width, self.height = screen_size
        self.button = Button("Start Game", (self.width // 2 - 100, self.height // 2 - 30), (200, 60))
        self.active = True  # Start screen active flag
        self.final_time = None

    def draw(self, surface):
        surface.fill((150, 0, 200))  # Purple background
        self.button.draw(surface)
        # Draw final time if available
        if self.final_time:
            font = pg.font.Font(None, 48)
            text_surface = font.render(f"Final Time: {self.final_time}", True, (255, 255, 255))
            surface.blit(text_surface, (self.width // 2 - text_surface.get_width() // 2, self.height // 2 + 50))
        pg.display.flip()
    def set_final_time(self, time_str):
        self.final_time = time_str

    def handle_events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                return "QUIT"
            if self.button.is_clicked(event):
                self.active = False
                return "START"
        return None
