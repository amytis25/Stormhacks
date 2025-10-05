import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
import math 
from sphere_manager import SphereManager

# Import our custom modules
from shapes import Shapes
from arduino_controls import ArduinoControls, KeyboardFallbackControls
# from character import Character  # Comment out if this file doesn't exist
from lane_markers import LaneMarkers
from game_timer import GameTimer

## Arduino-enabled version of the game
from start_screen import StartScreen
from button import Button  # Make sure both files are in the same directory

class ArduinoApp:
    def __init__(self, arduino_port='COM3', arduino_baudrate=115200):
        # Initialize pygame
        pg.init()
        self.screen = pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption("Log Roller Game - Arduino Controls")
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
        
        # Try to initialize Arduino controls first, fallback to keyboard
        try:
            print(f"Attempting to connect to Arduino on {arduino_port}...")
            self.controls = ArduinoControls(port=arduino_port, baudrate=arduino_baudrate)
            self.using_arduino = True
            print("✅ Arduino controls initialized successfully!")
        except Exception as e:
            print(f"❌ Arduino connection failed: {e}")
            print("🎮 Falling back to keyboard controls...")
            self.controls = KeyboardFallbackControls()
            self.using_arduino = False
        
        self.shapes = Shapes()
        
        # Initialize character (comment out if character.py doesn't exist)
        # self.character = Character("character.png")
        
        self.lane_markers = LaneMarkers()
        self.sphere_manager = SphereManager() # Initialize sphere manager
        
        # Initialize game timer
        self.game_timer = GameTimer()
        
        # Display control information
        self.display_control_info()
        
        self.mainLoop()

    def display_control_info(self):
        """Display information about current control method"""
        print("\n" + "="*60)
        print("CONTROL INFORMATION")
        print("="*60)
        
        if self.using_arduino:
            print("🎮 ARDUINO CONTROLS ACTIVE")
            print("Controls:")
            print("  📏 Ultrasonic Sensor:")
            print("    - Close distance (< 10cm) = CROUCH")
            print("    - Far distance (> 30cm) = JUMP")
            print("    - Middle distance (10-30cm) = NEUTRAL")
            print("  🕹️ Joystick:")
            print("    - Left = Move to LEFT lane")
            print("    - Right = Move to RIGHT lane")
            print("    - Button = Special action (if implemented)")
        else:
            print("⌨️ KEYBOARD CONTROLS ACTIVE")
            print("Controls:")
            print("    - LEFT/A = Move to LEFT lane")
            print("    - RIGHT/D = Move to RIGHT lane")
            print("    - UP/W = JUMP")
            print("    - DOWN/S = CROUCH")
        
        print("="*60)
        print("🎯 Goal: Avoid the obstacles and survive as long as possible!")
        print("⏱️ Timer: Shows your survival time in MM:SS:mmm format")
        print("="*60 + "\n")

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
        frame_count = 0

        while running:
            # Get all events
            events = pg.event.get()
            
            # Check for quit events
            for event in events:
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    # Additional keyboard shortcuts
                    if event.key == pg.K_r:  # R key to reset timer
                        self.game_timer.reset_timer()
                        print("Timer reset!")
                    elif event.key == pg.K_p:  # P key to pause/resume timer
                        if self.game_timer.is_paused:
                            self.game_timer.resume_timer()
                            print("Timer resumed!")
                        else:
                            self.game_timer.pause_timer()
                            print("Timer paused!")
                    elif event.key == pg.K_i:  # I key to show sensor info (Arduino only)
                        if self.using_arduino and hasattr(self.controls, 'get_sensor_status'):
                            status = self.controls.get_sensor_status()
                            print(f"Arduino Status: {status}")
            
            # Handle game controls
            self.controls.handle_events(events)
            self.controls.handle_continuous_input()
            self.controls.update_movement()
            
            # Get cube position from controls
            cube_x, cube_y, cube_distance = self.controls.get_cube_position()

            # Refresh screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Draw the cube using the shapes module
            self.shapes.draw_cube(cube_x, cube_y, cube_distance, self.rotation_angle)
            
            # Update and draw objects (wall and spheres) using SphereManager
            self.sphere_manager.update_positions()
            self.sphere_manager.draw_objects(self.shapes, self.rotation_angle)

            # Collision detection logic (using Arduino control lane positions)
            cube_lane = None
            if abs(cube_x - (-5.0)) < 0.5:  # Left lane at -5.0
                cube_lane = 'left'
            elif abs(cube_x - 0.0) < 0.5:   # Center lane at 0.0
                cube_lane = 'middle'
            elif abs(cube_x - 5.0) < 0.5:   # Right lane at 5.0
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
                        # Hit a wall - game over
                        self.game_timer.end_timer()
                        final_time = self.game_timer.format_time(self.game_timer.get_elapsed_time())
                        self.start_screen.set_final_time(final_time)
                        pg.display.flip()
                        pg.time.wait(1000)
                        self.show_start_screen()
                        return
                    else:
                        # Hit a sphere - check Y collision too
                        if abs(cube_y - obj_y) < (cube_radius + 1.5):
                            self.game_timer.end_timer()
                            final_time = self.game_timer.format_time(self.game_timer.get_elapsed_time())
                            self.start_screen.set_final_time(final_time)
                            pg.display.flip()
                            pg.time.wait(1000)
                            self.show_start_screen()
                            return

            # Draw lane markers
            self.lane_markers.draw_all_lane_markers()

            # Draw timer on top (last, so it appears over everything)
            self.game_timer.draw_timer()

            # Update rotation
            # self.rotation_angle += 1
            # if self.rotation_angle >= 360:
            self.rotation_angle = 0
            
            # Display Arduino sensor info periodically (every 60 frames = 1 second)
            if self.using_arduino and hasattr(self.controls, 'get_sensor_status'):
                frame_count += 1
                if frame_count % 60 == 0:  # Every second
                    status = self.controls.get_sensor_status()
                    print(f"Arduino: Joystick=({status.get('joystick_x', 'N/A'):+4}, {status.get('joystick_y', 'N/A'):+4}), "
                          f"Distance={status.get('ultrasonic_distance', 'N/A'):5.1f}cm, "
                          f"Lane={status.get('lane_name', 'N/A')}, "
                          f"State={status.get('movement_state', 'N/A')}")
            
            pg.display.flip()

            # Timing
            self.clock.tick(60)
    
    def quit(self):
        """Clean up resources"""
        if self.using_arduino and hasattr(self.controls, 'cleanup'):
            self.controls.cleanup()
        pg.quit()

class RegularApp:
    """Regular keyboard-only version for compatibility"""
    def __init__(self):
        # This is the same as the original base.py but organized
        from controls import GameControls
        
        # Initialize pygame
        pg.init()
        self.screen = pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption("Log Roller Game - Keyboard Controls")
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
        
        self.lane_markers = LaneMarkers()
        self.sphere_manager = SphereManager()
        self.game_timer = GameTimer()
        
        print("🎮 KEYBOARD CONTROLS: LEFT/RIGHT=lanes, UP=jump, DOWN=crouch")
        
        self.mainLoop()

    def show_start_screen(self):
        surface = pg.display.set_mode((800, 600))
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
        self.screen = pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)

    def mainLoop(self):
        running = True
        while running:
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.game_timer.reset_timer()
            
            self.controls.handle_events(events)
            self.controls.handle_continuous_input()
            self.controls.update_movement()
            
            cube_x, cube_y, cube_distance = self.controls.get_cube_position()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.shapes.draw_cube(cube_x, cube_y, cube_distance, self.rotation_angle)
            self.sphere_manager.update_positions()
            self.sphere_manager.draw_objects(self.shapes, self.rotation_angle)
            self.lane_markers.draw_all_lane_markers()
            self.game_timer.draw_timer()
            
            self.rotation_angle = 0
            pg.display.flip()
            self.clock.tick(60)
    
    def quit(self):
        pg.quit()

if __name__ == "__main__":
    import sys
    
    print("🎮 LOG ROLLER GAME")
    print("==================")
    print("Choose control method:")
    print("1. Arduino Controls (requires Arduino connected)")
    print("2. Keyboard Controls (fallback)")
    print("3. Auto-detect (try Arduino first, fallback to keyboard)")
    
    # Check command line arguments
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("\nEnter choice (1/2/3) or press Enter for auto-detect: ").strip()
    
    if choice == "1":
        # Force Arduino mode
        print("🔌 Forcing Arduino controls...")
        myApp = ArduinoApp()
    elif choice == "2":
        # Force keyboard mode
        print("⌨️ Using keyboard controls...")
        myApp = RegularApp()
    else:
        # Auto-detect (default)
        print("🔍 Auto-detecting controls...")
        myApp = ArduinoApp()  # Will automatically fallback to keyboard if Arduino fails
