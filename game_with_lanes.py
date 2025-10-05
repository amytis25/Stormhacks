"""
Example of how to add lane markers to your main game
This shows how to integrate the lane_markers.py into base.py
"""

import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *

# Import our custom modules
from shapes import Shapes
from controls import GameControls
from lane_markers import LaneMarkers

class GameWithLaneMarkers:
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
        
        # Initialize lane markers
        self.lane_markers = LaneMarkers()
        
        # Position streaming variables
        self.frame_count = 0
        self.position_update_interval = 10

        self.mainLoop()

    def mainLoop(self):
        running = True
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
            
            # Stream position data (constantly updating)
            self.frame_count += 1
            if self.frame_count % self.position_update_interval == 0:
                self.print_position_stream(cube_x, cube_y, cube_distance)

            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Draw lane markers FIRST (so they appear behind other objects)
            self.lane_markers.draw_all_lane_markers()  # All lane marking elements
            # OR use one of these alternatives:
            # self.lane_markers.draw_minimal_lane_markers()  # Just divider boxes
            # self.lane_markers.draw_simple_lane_ground()     # Just ground strips
            
            # Draw the cube using the shapes module
            self.shapes.draw_cube(cube_x, cube_y, cube_distance, self.rotation_angle)
            
            # Draw the pyramids (optional)
            # self.shapes.draw_triangle_left(self.rotation_angle)
            # self.shapes.draw_triangle_right(self.rotation_angle)
            
            # Update rotation
            self.rotation_angle += 1 # to rotate the objects (animation)
            if self.rotation_angle >= 360:
                self.rotation_angle = 0
            
            pg.display.flip()
            self.clock.tick(60)
    
    def print_position_stream(self, cube_x, cube_y, cube_distance):
        """Print a constant stream of object positions"""
        # Get detailed control status
        control_status = self.controls.get_control_status()
        
        print(f"FRAME {self.frame_count:05d} | "
              f"Cube Position: X={cube_x:+6.2f}, Y={cube_y:+6.2f}, Z={cube_distance:+6.2f} | "
              f"Rotation: {self.rotation_angle:03.0f}° | "
              f"Lane: {control_status['lane_name']} | "
              f"State: {control_status['movement_state']}")
        
        # If jumping or crouching, show timer info
        if control_status['is_jumping']:
            print(f"          >>> JUMPING: Timer={control_status['jump_timer']}/30")
        elif control_status['is_crouching']:
            print(f"          >>> CROUCHING: Timer={control_status['crouch_timer']}/30")
    
    def quit(self):
        pg.quit()

if __name__ == "__main__":
    print("Game with Lane Markers")
    print("======================")
    print("Controls:")
    print("- Arrow Keys or WASD: Move between lanes, jump, and crouch")
    print("- Lane markers will help you see the three lanes clearly")
    print("\nLane Markers Include:")
    print("- Ground strips in different colors for each lane")
    print("- Divider boxes between lanes")
    print("- Lane marker boxes below the cube")
    print("- Boundary walls on the sides")
    print("\nStarting game...")
    
    myApp = GameWithLaneMarkers()
