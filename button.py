import pygame as pg

class Button:
    def __init__(self, text, pos, size, font_size=36, bg_color=(180, 100, 255), text_color=(255, 255, 255)):
        self.text = text
        self.pos = pos
        self.size = size
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = pg.font.Font(None, font_size)
        self.rect = pg.Rect(pos, size)

    def draw(self, surface):
        pg.draw.rect(surface, self.bg_color, self.rect, border_radius=12)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
