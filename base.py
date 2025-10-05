import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
import math 
from sphere_manager import SphereManager

# Import our custom modules
from shapes import Shapes
from controls import GameControls
# from character import Character  # Comment out if this file doesn't exist
from lane_markers import LaneMarkers

'''
from arduino_controls import ArduinoControls

# Initialize with your Arduino's COM port
controls = ArduinoControls(port='COM3', baudrate=115200)
'''
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
        
        # Initialize game controls
        self.controls = GameControls()
        
        # Initialize shapes renderer
        self.shapes = Shapes()
        
        # Initialize sphere manager
        self.sphere_manager = SphereManager()

        self.lane_markers = LaneMarkers()

        # Initialize character (comment out if character.py doesn't exist)
        # self.character = Character("character.png")
        
        self.mainLoop()

    def mainLoop(self):
        running = True

    # Sphere positions managed by SphereManager

        while running:
            # Get all events
            events = pg.event.get()
            
            # Check for quit events
            for event in events:
                if event.type == pg.QUIT:
                    running = False
            
            # Handle game controls
            self.controls.handle_events(events)
            self.controls.handle_continuous_input()
            self.controls.update_movement()
            
            # Get cube position from controls
            cube_x, cube_y, cube_distance = self.controls.get_cube_position()

            # Refresh screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Get cube position from controls
            cube_x, cube_y, cube_distance = self.controls.get_cube_position()

            # Draw the cube using the shapes module
            self.shapes.draw_cube(cube_x, cube_y, cube_distance, self.rotation_angle)
            
            # Update and draw spheres using SphereManager
            self.sphere_manager.update_positions()
            self.sphere_manager.draw_spheres(self.shapes, self.rotation_angle)

            # Draw lane markers
            self.lane_markers.draw_all_lane_markers()

            # Update rotation
           # self.rotation_angle += 1
            #if self.rotation_angle >= 360:
            self.rotation_angle = 0
            
            pg.display.flip()

            # Timing
            self.clock.tick(60)
    
    def quit(self):
        pg.quit()

   
if __name__ == "__main__":
    myApp = App()