import pygame as pg
from OpenGL.GL import *

class Character:
    def __init__(self, image_path):
        self.texture = self.load_texture(image_path)

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
        self.width = width
        self.height = height
        return texture_id

    def draw(self, x, y, z):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glPushMatrix()
        glTranslatef(x, y, z)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-1, -1, 0)
        glTexCoord2f(1, 0); glVertex3f(1, -1, 0)
        glTexCoord2f(1, 1); glVertex3f(1, 1, 0)
        glTexCoord2f(0, 1); glVertex3f(-1, 1, 0)
        glEnd()
        glPopMatrix()
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)