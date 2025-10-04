
import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
import math 

## Provided Documents and Copilot were to assist in creating and debugging the program 
class App:
    def __init__(self):

        #initialize pygame
        pg.init()
        pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        
        #initialize OpenGL
        glClearColor(1, 0.929, 0.961, 0.5) # Set background color
        glEnable(GL_DEPTH_TEST)  # Enable depth testing for 3D
        
        # Set up perspective projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 50.0) # Field of view, aspect ratio, near and far planes
        glMatrixMode(GL_MODELVIEW)
        
        # Initialize rotation angle
        self.rotation_angle = 0
        
        self.mainLoop()

    def mainLoop(self):
        running = True
        while running:
            #check events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            
            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Draw the cube
            self.draw_cube()
            
            # Draw the pyramid
            self.draw_triangle_left()
            self.draw_triangle_right()
            
            # Update rotation
            self.rotation_angle += 1 # to rotate the objects (animation)
            if self.rotation_angle >= 360:
                self.rotation_angle = 0
            
            pg.display.flip()

            #timing
            self.clock.tick(60)
    
    def draw_cube(self):
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -15.0)  # Move cube away from camera
        glRotatef(self.rotation_angle, 1, 1, 0)  # Rotate around all axes - fixed rotation
        
        # Define cube vertices
        vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], # Back face
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1] # Front face
        ]
        
        # Define faces (vertex indices) and colors
        faces = [
            ([0, 1, 2, 3], (199/255, 159/255, 212/255)),  # Back face - Red
            ([4, 5, 6, 7], (199/255, 159/255, 212/255)),  # Front face - Green
            ([0, 1, 5, 4], (159/255, 186/255, 212/255)),  # Bottom face - Blue
            ([2, 3, 7, 6], (159/255, 186/255, 212/255)),  # Top face - Yellow
            ([0, 3, 7, 4], (159/255, 159/255, 212/255)),  # Left face - Magenta
            ([1, 2, 6, 5], (159/255, 159/255, 212/255))   # Right face - Cyan
        ]
        
        # Draw each face
        for face, color in faces:
            glColor3f(*color)
            glBegin(GL_QUADS)
            for vertex_index in face:
                glVertex3f(*vertices[vertex_index])
            glEnd()
    
    def draw_triangle_left(self):
        glLoadIdentity()
        glTranslatef(-4.0, 0.0, -15.0)  # Position pyramid to the left
        glRotatef(self.rotation_angle, 1, 1, 1)  # Rotate around all axes
        
        # Define pyramid vertices
        # Apex (top point)
        apex = [0.0, 2.0, 0.0]
        
        # Base vertices (square base)
        base = [
            [-1.5, -1.0, 1.5], # Front-left
            [1.5, -1.0, 1.5],  # Front-right
            [1.5, -1.0, -1.5], # Back-right
            [-1.5, -1.0, -1.5] # Back-left
        ]
        
        # Draw pyramid faces
        # Front face (apex + front edge of base) 
        glColor3f(175/255, 205/255, 237/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[0])  # Front-left
        glVertex3f(*base[1])  # Front-right
        glEnd()
        
        # Right face (apex + right edge of base) 
        glColor3f(175/255, 237/255, 209/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[1])  # Front-right
        glVertex3f(*base[2])  # Back-right
        glEnd()
        
        # Back face (apex + back edge of base) 
        glColor3f(175/255, 205/255, 237/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[2])  # Back-right
        glVertex3f(*base[3])  # Back-left
        glEnd()
        
        # Left face (apex + left edge of base) 
        glColor3f(175/255, 237/255, 209/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[3])  # Back-left
        glVertex3f(*base[0])  # Front-left
        glEnd()
        
        # Base (square bottom) 
        glColor3f(84/255, 118/255, 153/255)
        glBegin(GL_QUADS)
        glVertex3f(*base[0])  # Front-left
        glVertex3f(*base[1])  # Front-right
        glVertex3f(*base[2])  # Back-right
        glVertex3f(*base[3])  # Back-left
        glEnd()

    def draw_triangle_right(self):
        glLoadIdentity()
        glTranslatef(4.0, 0.0, -15.0)  # Position pyramid to the right
        glRotatef(self.rotation_angle, -1, 1, -1)  # Rotate around all axes
        
        # Define pyramid vertices
        # Apex (top point)
        apex = [0.0, 2.0, 0.0]
        
        # Base vertices (square base)
        base = [
            [-1.5, -1.0, 1.5],  # Front-left
            [1.5, -1.0, 1.5],   # Front-right
            [1.5, -1.0, -1.5],  # Back-right
            [-1.5, -1.0, -1.5]  # Back-left
        ]
        
        # Draw pyramid faces
        # Front face (apex + front edge of base) 
        glColor3f(175/255, 205/255, 237/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[0])  # Front-left
        glVertex3f(*base[1])  # Front-right
        glEnd()
        
        # Right face (apex + right edge of base) 
        glColor3f(175/255, 237/255, 209/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[1])  # Front-right
        glVertex3f(*base[2])  # Back-right
        glEnd()
        
        # Back face (apex + back edge of base) 
        glColor3f(175/255, 205/255, 237/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[2])  # Back-right
        glVertex3f(*base[3])  # Back-left
        glEnd()
        
        # Left face (apex + left edge of base) 
        glColor3f(175/255, 237/255, 209/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[3])  # Back-left
        glVertex3f(*base[0])  # Front-left
        glEnd()
        
        # Base (square bottom) 
        glColor3f(84/255, 118/255, 153/255)
        glBegin(GL_QUADS)
        glVertex3f(*base[0])  # Front-left
        glVertex3f(*base[1])  # Front-right
        glVertex3f(*base[2])  # Back-right
        glVertex3f(*base[3])  # Back-left
        glEnd()
    
    def quit(self):
        pg.quit()
   
if __name__ == "__main__":
    myApp = App()
                

