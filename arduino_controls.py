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
        
        # Control thresholds - specialized for limited joystick range (-1 to -3)
        self.joystick_threshold = 1  # Very sensitive - any change from center triggers
        self.joystick_center_x = -2  # Middle of your range (-1 to -3)
        self.joystick_center_y = -2  # Assume same for Y
        self.joystick_min = -3       # Your joystick's minimum value
        self.joystick_max = -1       # Your joystick's maximum value
        
        # Lane switching state tracking
        self.last_joystick_x = 0
        self.lane_switch_cooldown = 0  # Prevent rapid switching
        
        self.distance_close_threshold = 10.0  # Close distance for crouch (cm)
        self.distance_far_threshold = 30.0    # Far distance for jump (cm)
        # Middle area: between 10cm and 30cm = neutral position
        
        # Initialize Arduino connection
        self.connect_arduino(port, baudrate)
        
    def connect_arduino(self, port, baudrate):
        """Connect to Arduino and start reading data"""
        try:
            print(f"Attempting to connect to Arduino on {port} at {baudrate} baud...")
            self.serial_port = serial.Serial(port, baudrate, timeout=1)
            print("Serial port opened successfully!")
            time.sleep(2)  # Wait for Arduino to initialize
            print("Waiting for Arduino to initialize...")
            
            # Clear any initial garbage data
            self.serial_port.flushInput()
            
            self.running = True
            self.arduino_thread = threading.Thread(target=self._read_arduino_data)
            self.arduino_thread.daemon = True
            self.arduino_thread.start()
            print(f"✅ Connected to Arduino on {port}")
            print("🔍 Starting Arduino data monitoring...")
        except Exception as e:
            print(f"❌ Failed to connect to Arduino: {e}")
            print("🎮 Using keyboard fallback controls")
    
    def _read_arduino_data(self):
        """Background thread to read data from Arduino"""
        joystick_data = {}
        print("Arduino data reader thread started...")
        
        while self.running and self.serial_port:
            try:
                if self.serial_port.in_waiting > 0:
                    line = self.serial_port.readline().decode('utf-8').strip()
                    print(f"DEBUG: Received from Arduino: '{line}'")  # Debug output
                    
                    # Parse joystick data
                    if line.startswith("X:"):
                        try:
                            self.joystick_x = int(line.split(":")[1])
                            print(f"DEBUG: Set joystick_x = {self.joystick_x}")
                        except Exception as e:
                            print(f"DEBUG: Failed to parse X: {e}")
                    elif line.startswith("Y:"):
                        try:
                            self.joystick_y = int(line.split(":")[1])
                            print(f"DEBUG: Set joystick_y = {self.joystick_y}")
                        except Exception as e:
                            print(f"DEBUG: Failed to parse Y: {e}")
                    elif line.startswith("Button pressed"):
                        self.joystick_button = True
                        print("DEBUG: Button pressed")
                    elif line.startswith("Button not pressed"):
                        self.joystick_button = False
                        print("DEBUG: Button not pressed")
                    elif line.startswith("Distance:"):
                        try:
                            self.ultrasonic_distance = float(line.split(":")[1].strip())
                            print(f"DEBUG: Set distance = {self.ultrasonic_distance}")
                        except Exception as e:
                            print(f"DEBUG: Failed to parse Distance: {e}")
                    else:
                        print(f"DEBUG: Unknown line format: '{line}'")
                else:
                    # No data waiting, small delay
                    time.sleep(0.01)
                            
            except Exception as e:
                print(f"Error reading Arduino data: {e}")
                time.sleep(0.1)
    
    def handle_events(self, events):
        """Handle discrete events - for Arduino, this processes sensor state changes"""
        # Reduce cooldown timer
        if self.lane_switch_cooldown > 0:
            self.lane_switch_cooldown -= 1
        
        # Debug current values
        print(f"DEBUG: joystick_x={self.joystick_x} (range: {self.joystick_min} to {self.joystick_max})")
        print(f"DEBUG: center={self.joystick_center_x}, cooldown={self.lane_switch_cooldown}")
        
        # Specialized joystick handling for limited range (-1 to -3)
        if self.lane_switch_cooldown == 0:  # Only if not in cooldown
            if self.joystick_x <= self.joystick_min:  # At -3 (full left)
                print(f"DEBUG: FULL LEFT detected! X={self.joystick_x}")
                if self.current_lane > 0:  # Can move left
                    self.current_lane -= 1
                    self.lane_switch_cooldown = 20  # 20 frames cooldown
                    print(f"DEBUG: Moved to lane {self.current_lane} (LEFT)")
                    
            elif self.joystick_x >= self.joystick_max:  # At -1 (full right)
                print(f"DEBUG: FULL RIGHT detected! X={self.joystick_x}")
                if self.current_lane < 2:  # Can move right
                    self.current_lane += 1
                    self.lane_switch_cooldown = 20  # 20 frames cooldown
                    print(f"DEBUG: Moved to lane {self.current_lane} (RIGHT)")
                    
            elif self.joystick_x == self.joystick_center_x:  # At -2 (center)
                print(f"DEBUG: CENTER position detected! X={self.joystick_x}")
            
            else:
                print(f"DEBUG: Unexpected joystick value: {self.joystick_x}")
        
        # Ultrasonic sensor for CONTINUOUS vertical position mapping
        self._map_distance_to_position()
        
    def _map_distance_to_position(self):
        """Map ultrasonic distance to cube Y position continuously"""
        # Define distance mapping ranges
        min_distance = 5.0   # Closest distance (cube at lowest position)
        max_distance = 50.0  # Farthest distance (cube at highest position)
        
        # Define Y position ranges
        min_y = -5.0  # Lowest cube position (crouched)
        max_y = 1.0   # Highest cube position (jumped)
        
        # Clamp distance to our working range
        clamped_distance = max(min_distance, min(max_distance, self.ultrasonic_distance))
        
        # Map distance to Y position linearly
        # Close distance (5cm) -> Low Y (-3.0)
        # Far distance (50cm) -> High Y (3.0)
        distance_ratio = (clamped_distance - min_distance) / (max_distance - min_distance)
        target_y = min_y + (distance_ratio * (max_y - min_y))
        
        # Smooth movement towards target position
        smoothing_factor = 0.1  # Adjust for smoother/faster response
        self.cube_y += (target_y - self.cube_y) * smoothing_factor
        
        print(f"DEBUG: Distance={self.ultrasonic_distance:.1f}cm -> Target_Y={target_y:.2f} -> Cube_Y={self.cube_y:.2f}")
        
        # Update state flags for compatibility
        self.is_jumping = self.cube_y > 1.0
        self.is_crouching = self.cube_y < -1.0
    
    def handle_continuous_input(self):
        """Handle continuous input - Arduino sensors provide continuous data"""
        # The Arduino sensors are read continuously in the background thread
        # This method can be used for any continuous processing if needed
        pass
    
    def update_movement(self):
        """Update movement - now using continuous distance mapping"""
        # Cube Y position is now continuously updated in _map_distance_to_position()
        # Just update the lane position
        self.cube_x = self.lanes[self.current_lane]
    
    def get_cube_position(self):
        """Return the current cube position"""
        return self.cube_x, self.cube_y, self.cube_distance
    
    def get_sensor_status(self):
        """Get current sensor readings for debugging"""
        # Get lane name
        lane_names = ["LEFT", "CENTER", "RIGHT"]
        lane_name = lane_names[self.current_lane] if 0 <= self.current_lane < 3 else "UNKNOWN"
        
        # Get movement state
        if self.is_jumping:
            movement_state = "JUMPING"
        elif self.is_crouching:
            movement_state = "CROUCHING"
        else:
            movement_state = "NEUTRAL"
            
        return {
            'joystick_x': self.joystick_x,
            'joystick_y': self.joystick_y,
            'joystick_button': self.joystick_button,
            'ultrasonic_distance': self.ultrasonic_distance,
            'distance_zone': self._get_distance_zone(),
            'current_lane': self.current_lane,
            'lane_name': lane_name,
            'movement_state': movement_state,
            'is_jumping': self.is_jumping,
            'is_crouching': self.is_crouching
        }
    
    def _get_distance_zone(self):
        """Get the current distance zone for debugging"""
        if self.ultrasonic_distance < 10:
            return f"CLOSE ({self.ultrasonic_distance:.1f}cm = LOW position)"
        elif self.ultrasonic_distance > 40:
            return f"FAR ({self.ultrasonic_distance:.1f}cm = HIGH position)"
        else:
            return f"MID ({self.ultrasonic_distance:.1f}cm = MID position)"
    
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
