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
from game_timer import GameTimer

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
        self.start_screen = StartScreen((800, 600))
        self.show_start_screen()

    def game_setup(self):
        self.screen = pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption("Log Roller Game")
        self.clock = pg.time.Clock()
        self.background = pg.image.load("background.png").convert()

        # OpenGL setup
        glClearColor(1, 0.929, 0.961, 0.5)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

        self.rotation_angle = 0
        self.controls = GameControls()
        self.shapes = Shapes()
        # self.character = Character("character.png")  # Uncomment if needed
        self.lane_markers = LaneMarkers()
        self.sphere_manager = SphereManager()
        self.game_timer = GameTimer()

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

        # After start, set up the game and start main loop
        self.game_setup()
        self.mainLoop()

    def mainLoop(self):
        running = True
        while running:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    running = False
            self.controls.handle_events(events)
            self.controls.handle_continuous_input()
            self.controls.update_movement()
            cube_x, cube_y, cube_distance = self.controls.get_cube_position()
            self.screen.blit(self.background, (0, 0))
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            cube_x, cube_y, cube_distance = self.controls.get_cube_position()
            self.shapes.draw_cube(cube_x, cube_y, cube_distance, self.rotation_angle)
            self.sphere_manager.update_positions()
            self.sphere_manager.draw_objects(self.shapes, self.rotation_angle)
            cube_lane = None
            if abs(cube_x - (-4.0)) < 0.5:
                cube_lane = 'left'
            elif abs(cube_x - 0.0) < 0.5:
                cube_lane = 'middle'
            elif abs(cube_x - 4.0) < 0.5:
                cube_lane = 'right'
            collision_threshold = 2.0
            objects = [
                ('left', self.sphere_manager.left_sphere_z, self.sphere_manager.left_sphere_y, self.sphere_manager.left_is_wall),
                ('middle', self.sphere_manager.middle_sphere_z, self.sphere_manager.middle_sphere_y, self.sphere_manager.middle_is_wall),
                ('right', self.sphere_manager.right_sphere_z, self.sphere_manager.right_sphere_y, self.sphere_manager.right_is_wall)
            ]
            cube_radius = 1.0
            for lane, obj_z, obj_y, is_wall in objects:
                if cube_lane == lane and abs(obj_z - cube_distance) < collision_threshold:
                    if is_wall:
                        self.game_timer.end_timer()
                        final_time = self.game_timer.format_time(self.game_timer.get_elapsed_time())
                        self.start_screen.set_final_time(final_time)
                        pg.display.flip()
                        pg.time.wait(1000)
                        self.show_start_screen()
                        return
                    else:
                        if abs(cube_y - obj_y) < (cube_radius + 1.5):
                            self.game_timer.end_timer()
                            final_time = self.game_timer.format_time(self.game_timer.get_elapsed_time())
                            self.start_screen.set_final_time(final_time)
                            pg.display.flip()
                            pg.time.wait(1000)
                            self.show_start_screen()
                            return
            self.lane_markers.draw_all_lane_markers()
            self.game_timer.draw_timer()
            self.rotation_angle = 0
            pg.display.flip()
            self.clock.tick(60)
    def quit(self):
        pg.quit()

   
if __name__ == "__main__":
    myApp = App()