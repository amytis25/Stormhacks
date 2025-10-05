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
from start_screen import StartScreen
from button import Button  # Make sure both files are in the same directory

class App:
    def __init__(self):
        # Initialize pygame
        pg.init()
        self.screen = pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption("Log Roller Game")
        self.clock = pg.time.Clock()
        
        # Show start screen
        self.start_screen = StartScreen((800, 600))
        self.show_start_screen()

        # Continue OpenGL setup after start
        glClearColor(1, 0.929, 0.961, 0.5)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        
        self.rotation_angle = 0
        self.controls = GameControls()
        self.shapes = Shapes()
        
        

        # Initialize character (comment out if character.py doesn't exist)
        # self.character = Character("character.png")
        
        self.lane_markers = LaneMarkers()
        self.sphere_manager = SphereManager() # Initialize sphere manager
        #self.character = Character("character.png")

        self.mainLoop()

    def show_start_screen(self):
        surface = pg.display.set_mode((800, 600))  # Temporarily disable OpenGL for start screen
        showing = True
        while showing:
            events = pg.event.get()
            result = self.start_screen.handle_events(events)
            self.start_screen.draw(surface)
            if result == "QUIT":
                pg.quit()
                exit()
            elif result == "START":
                showing = False

        # Recreate OpenGL context
        self.screen = pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)

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
            
            # Update and draw objects (wall and spheres) using SphereManager
            self.sphere_manager.update_positions()
            self.sphere_manager.draw_objects(self.shapes, self.rotation_angle)

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