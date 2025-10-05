import pygame as pg
import serial
import json
import threading
import time

class ArduinoControls:
    def __init__(self, port='COM3', baudrate=115200):
        """
        Arduino-based controls for the game
        
        Controls mapping:
        - Close distance on ultrasonic sensor = DOWN movement (crouch)
        - Far distance on ultrasonic sensor = UP movement (jump)
        - Middle distance on ultrasonic sensor = MIDDLE position (neutral)
        - Right on joystick (X+) = RIGHT lane switch
        - Left on joystick (X-) = LEFT lane switch
        - Joystick button = Special action (if needed)
        """
        # Define lanes (x positions for the cube)
        self.lanes = [-5.0, 0.0, 5.0]  # Left, Center, Right
        self.current_lane = 1  # Start in the center lane (index 1)

        # Jump and crouch state
        self.is_jumping = False
        self.is_crouching = False
        self.jump_timer = 0
        self.crouch_timer = 0
        
        # Position variables
        self.cube_x = 0.0
        self.cube_y = 0.0
        self.cube_distance = -15.0
        
        # Arduino communication
        self.serial_port = None
        self.running = False
        self.arduino_thread = None
        
        # Sensor data
        self.joystick_x = 0
        self.joystick_y = 0
        self.joystick_button = False
        self.ultrasonic_distance = 100.0  # Default distance
        
        # Control thresholds
        self.joystick_threshold = 50  # Deadzone for joystick
        self.distance_close_threshold = 10.0  # Close distance for crouch (cm)
        self.distance_far_threshold = 30.0    # Far distance for jump (cm)
        # Middle area: between 10cm and 30cm = neutral position
        
        # Initialize Arduino connection
        self.connect_arduino(port, baudrate)
        
    def connect_arduino(self, port, baudrate):
        """Connect to Arduino and start reading data"""
        try:
            self.serial_port = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            self.running = True
            self.arduino_thread = threading.Thread(target=self._read_arduino_data)
            self.arduino_thread.daemon = True
            self.arduino_thread.start()
            print(f"Connected to Arduino on {port}")
        except Exception as e:
            print(f"Failed to connect to Arduino: {e}")
            print("Using keyboard fallback controls")
    
    def _read_arduino_data(self):
        """Background thread to read data from Arduino"""
        joystick_data = {}
        
        while self.running and self.serial_port:
            try:
                if self.serial_port.in_waiting > 0:
                    line = self.serial_port.readline().decode('utf-8').strip()
                    
                    # Parse joystick data
                    if line.startswith("X:"):
                        try:
                            self.joystick_x = int(line.split(":")[1])
                        except:
                            pass
                    elif line.startswith("Y:"):
                        try:
                            self.joystick_y = int(line.split(":")[1])
                        except:
                            pass
                    elif line.startswith("Button pressed"):
                        self.joystick_button = True
                    elif line.startswith("Button not pressed"):
                        self.joystick_button = False
                    elif line.startswith("Distance:"):
                        try:
                            self.ultrasonic_distance = float(line.split(":")[1].strip())
                        except:
                            pass
                            
            except Exception as e:
                print(f"Error reading Arduino data: {e}")
                time.sleep(0.1)
    
    def handle_events(self, events):
        """Handle discrete events - for Arduino, this processes sensor state changes"""
        # Check joystick for lane switching (discrete actions) - ONLY LEFT/RIGHT
        if abs(self.joystick_x) > self.joystick_threshold:
            if self.joystick_x > self.joystick_threshold:  # Right
                if self.current_lane < 2:  # Ensure we don't go out of bounds
                    self.current_lane += 1
                    time.sleep(0.3)  # Debounce
            elif self.joystick_x < -self.joystick_threshold:  # Left
                if self.current_lane > 0:  # Ensure we don't go out of bounds
                    self.current_lane -= 1
                    time.sleep(0.3)  # Debounce
        
        # Check ultrasonic sensor for vertical movements based on distance zones
        if self.ultrasonic_distance < self.distance_close_threshold and not self.is_crouching:
            # Close distance = crouch (DOWN)
            self.is_crouching = True
            self.crouch_timer = 10  # Number of frames the crouch lasts
        elif self.ultrasonic_distance > self.distance_far_threshold and not self.is_jumping:
            # Far distance = jump (UP)
            self.is_jumping = True
            self.jump_timer = 10  # Number of frames the jump lasts
        # Middle distance (between thresholds) = neutral position (no action)
    
    def handle_continuous_input(self):
        """Handle continuous input - Arduino sensors provide continuous data"""
        # The Arduino sensors are read continuously in the background thread
        # This method can be used for any continuous processing if needed
        pass
    
    def update_movement(self):
        """Update movement animations (jump, crouch, lane switching)"""
        # Handle jump
        if self.is_jumping:
            if self.jump_timer > 7:  # First phase of the jump (going up)
                self.cube_y += 0.4
            elif self.jump_timer > 3:  # Pause at the top
                pass  # Do nothing, stay at the top
            elif self.jump_timer > 0:  # Second phase of the jump (going down)
                self.cube_y -= 0.4
            self.jump_timer -= 1
            if self.jump_timer == 0:  # End of jump
                self.is_jumping = False

        # Handle crouch
        if self.is_crouching:
            if self.crouch_timer > 7:  # First phase of the crouch (going down)
                self.cube_y -= 0.4
            elif self.crouch_timer > 3:  # Pause at the bottom
                pass  # Do nothing, stay at the bottom
            elif self.crouch_timer > 0:  # Second phase of the crouch (going up)
                self.cube_y += 0.4
            self.crouch_timer -= 1
            if self.crouch_timer == 0:  # End of crouch
                self.is_crouching = False
                        
        # Update cube's x position based on the current lane
        self.cube_x = self.lanes[self.current_lane]
    
    def get_cube_position(self):
        """Return the current cube position"""
        return self.cube_x, self.cube_y, self.cube_distance
    
    def get_sensor_status(self):
        """Get current sensor readings for debugging"""
        return {
            'joystick_x': self.joystick_x,
            'joystick_y': self.joystick_y,
            'joystick_button': self.joystick_button,
            'ultrasonic_distance': self.ultrasonic_distance,
            'distance_zone': self._get_distance_zone(),
            'current_lane': self.current_lane,
            'is_jumping': self.is_jumping,
            'is_crouching': self.is_crouching
        }
    
    def _get_distance_zone(self):
        """Get the current distance zone for debugging"""
        if self.ultrasonic_distance < self.distance_close_threshold:
            return "CLOSE (crouch)"
        elif self.ultrasonic_distance > self.distance_far_threshold:
            return "FAR (jump)"
        else:
            return "MIDDLE (neutral)"
    
    def cleanup(self):
        """Clean up Arduino connection"""
        self.running = False
        if self.arduino_thread:
            self.arduino_thread.join(timeout=1)
        if self.serial_port:
            self.serial_port.close()
            print("Arduino connection closed")

# Keyboard fallback controls (when Arduino is not connected)
class KeyboardFallbackControls:
    def __init__(self):
        """Fallback to keyboard controls if Arduino is not available"""
        # Define lanes (x positions for the cube)
        self.lanes = [-5.0, 0.0, 5.0]  # Left, Center, Right
        self.current_lane = 1  # Start in the center lane (index 1)

        # Jump and crouch state
        self.is_jumping = False
        self.is_crouching = False
        self.jump_timer = 0
        self.crouch_timer = 0
        
        # Position variables
        self.cube_x = 0.0
        self.cube_y = 0.0
        self.cube_distance = -15.0
        
    def handle_events(self, events):
        """Handle keyboard events as fallback"""
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT or event.key == pg.K_a:  # Move to the left lane
                    if self.current_lane > 0:  # Ensure we don't go out of bounds
                        self.current_lane -= 1
                if event.key == pg.K_RIGHT or event.key == pg.K_d:  # Move to the right lane
                    if self.current_lane < 2:  # Ensure we don't go out of bounds
                        self.current_lane += 1
                if event.key == pg.K_UP or event.key == pg.K_w:  # Jump
                    if not self.is_jumping:  # Prevent double jumps
                        self.is_jumping = True
                        self.jump_timer = 10  # Number of frames the jump lasts
                if event.key == pg.K_DOWN or event.key == pg.K_s:  # Crouch
                    if not self.is_crouching:  # Prevent double crouches
                        self.is_crouching = True
                        self.crouch_timer = 10  # Number of frames the crouch lasts
    
    def handle_continuous_input(self):
        """Handle continuous input for fallback"""
        pass
    
    def update_movement(self):
        """Update movement animations (same as Arduino version)"""
        # Handle jump
        if self.is_jumping:
            if self.jump_timer > 7:  # First phase of the jump (going up)
                self.cube_y += 0.4
            elif self.jump_timer > 3:  # Pause at the top
                pass  # Do nothing, stay at the top
            elif self.jump_timer > 0:  # Second phase of the jump (going down)
                self.cube_y -= 0.4
            self.jump_timer -= 1
            if self.jump_timer == 0:  # End of jump
                self.is_jumping = False

        # Handle crouch
        if self.is_crouching:
            if self.crouch_timer > 7:  # First phase of the crouch (going down)
                self.cube_y -= 0.4
            elif self.crouch_timer > 3:  # Pause at the bottom
                pass  # Do nothing, stay at the bottom
            elif self.crouch_timer > 0:  # Second phase of the crouch (going up)
                self.cube_y += 0.4
            self.crouch_timer -= 1
            if self.crouch_timer == 0:  # End of crouch
                self.is_crouching = False
                        
        # Update cube's x position based on the current lane
        self.cube_x = self.lanes[self.current_lane]
    
    def get_cube_position(self):
        """Return the current cube position"""
        return self.cube_x, self.cube_y, self.cube_distance
    
    def cleanup(self):
        """No cleanup needed for keyboard controls"""
        pass
