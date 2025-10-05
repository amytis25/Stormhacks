import pygame as pg

class GameControls:
    def __init__(self):
        # Define lanes (x positions for the cube)
        self.lanes = [-4.0, 0.0, 4.0]  # Left, Center, Right
        self.current_lane = 1  # Start in the center lane (index 1)

        # Smooth lane switching variables
        self.target_x = self.lanes[self.current_lane]
        self.cube_x = self.lanes[self.current_lane]
        self.is_moving_side = False
        self.move_speed = 0.3  # Adjust for smoother/faster movement

        # Jump and crouch state
        self.is_jumping = False
        self.is_crouching = False
        self.jump_timer = 0
        self.crouch_timer = 0
        
        # Position variables
        self.cube_y = -2.0  # Start lower on the screen
        self.cube_distance = -15.0
        
        # Pause duration for jump/crouch hold phase
        self.pause_duration = 20  # Number of frames to pause at peak/bottom
        
    def handle_events(self, events):
        """Handle discrete key press events (single presses)"""
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT or event.key == pg.K_a:  # Move to the left lane
                    if self.current_lane > 0:
                        self.current_lane -= 1
                        self.target_x = self.lanes[self.current_lane]
                        self.is_moving_side = True
                if event.key == pg.K_RIGHT or event.key == pg.K_d:  # Move to the right lane
                    if self.current_lane < 2:
                        self.current_lane += 1
                        self.target_x = self.lanes[self.current_lane]
                        self.is_moving_side = True
                if event.key == pg.K_UP or event.key == pg.K_w:  # Jump
                    if not self.is_jumping and not self.is_crouching:
                        self.is_jumping = True
                        self.jump_timer = 50
                if event.key == pg.K_DOWN or event.key == pg.K_s:  # Crouch
                    if not self.is_crouching and not self.is_jumping:
                        self.is_crouching = True
                        self.crouch_timer = 50
    
    def handle_continuous_input(self):
        """Handle continuous key presses (holding keys down)"""
        # Uncomment and modify as needed for continuous input
        pass
    
    def update_movement(self):
        """Update movement animations (jump, crouch, lane switching)"""
        # Handle jump
        if self.is_jumping:
            up_frames = (50 - self.pause_duration) // 2
            down_frames = (50 - self.pause_duration) // 2
            # Up phase
            if self.jump_timer > (down_frames + self.pause_duration):
                self.cube_y += 0.2
            # Pause phase
            elif self.jump_timer > down_frames:
                pass
            # Down phase
            elif self.jump_timer > 0:
                self.cube_y -= 0.2
            self.jump_timer -= 1
            if self.jump_timer == 0:
                self.is_jumping = False

        # Handle crouch
        if self.is_crouching:
            down_frames = (50 - self.pause_duration) // 2
            up_frames = (50 - self.pause_duration) // 2
            # Down phase
            if self.crouch_timer > (up_frames + self.pause_duration):
                self.cube_y -= 0.2
            # Pause phase
            elif self.crouch_timer > up_frames:
                pass
            # Up phase
            elif self.crouch_timer > 0:
                self.cube_y += 0.2
            self.crouch_timer -= 1
            if self.crouch_timer == 0:
                self.is_crouching = False
                        
        # Smooth side-to-side movement
        if self.is_moving_side:
            if abs(self.cube_x - self.target_x) < self.move_speed:
                self.cube_x = self.target_x
                self.is_moving_side = False
            else:
                direction = 1 if self.target_x > self.cube_x else -1
                self.cube_x += direction * self.move_speed
        else:
            self.cube_x = self.target_x  # Ensure exact position when not moving
    
    def get_cube_position(self):
        """Return the current cube position"""
        return self.cube_x, self.cube_y, self.cube_distance
    
    def get_control_status(self):
        """Get current control status for debugging and streaming"""
        return {
            'cube_x': self.cube_x,
            'cube_y': self.cube_y,
            'cube_distance': self.cube_distance,
            'current_lane': self.current_lane,
            'lane_name': ['LEFT', 'CENTER', 'RIGHT'][self.current_lane],
            'is_jumping': self.is_jumping,
            'is_crouching': self.is_crouching,
            'jump_timer': self.jump_timer,
            'crouch_timer': self.crouch_timer,
            'movement_state': self._get_movement_state()
        }
    
    def _get_movement_state(self):
        """Get the current movement state as a string"""
        if self.is_jumping:
            if self.jump_timer > 20:
                return "JUMPING_UP"
            elif self.jump_timer > 10:
                return "JUMPING_PEAK"
            else:
                return "JUMPING_DOWN"
        elif self.is_crouching:
            if self.crouch_timer > 20:
                return "CROUCHING_DOWN"
            elif self.crouch_timer > 10:
                return "CROUCHING_HOLD"
            else:
                return "CROUCHING_UP"
        else:
            return "NEUTRAL"