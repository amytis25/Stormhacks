import pygame as pg
from OpenGL.GL import *

class Background:
    def __init__(self, image_path, window_size):
        self.texture = self.load_texture(image_path)
        self.scroll_offset = 0
        self.window_width, self.window_height = window_size

    def load_texture(self, filename):
        image = pg.image.load(filename)
        image = pg.transform.flip(image, False, True)
        image_data = pg.image.tostring(image, "RGBA", True)
        width, height = image.get_rect().size

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.image_height = height
        return texture_id

    def update(self, speed=2):
        self.scroll_offset = (self.scroll_offset + speed) % self.image_height

    def draw(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.window_width, 0, self.window_height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        scroll = self.scroll_offset / self.image_height
        glBegin(GL_QUADS)
        glTexCoord2f(0, scroll); glVertex2f(0, 0)
        glTexCoord2f(1, scroll); glVertex2f(self.window_width, 0)
        glTexCoord2f(1, scroll + 1); glVertex2f(self.window_width, self.window_height)
        glTexCoord2f(0, scroll + 1); glVertex2f(0, self.window_height)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)