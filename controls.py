import pygame as pg

class GameControls:
    def __init__(self):
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
        self.cube_y = -2.0  # Start lower on the screen
        self.cube_distance = -15.0
        
    def handle_events(self, events):
        """Handle discrete key press events (single presses)"""
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT or event.key == pg.K_a:  # Move to the left lane
                    if self.current_lane > 0:  # Ensure we don't go out of bounds
                        self.current_lane -= 1
                if event.key == pg.K_RIGHT or event.key == pg.K_d:  # Move to the right lane
                    if self.current_lane < 2:  # Ensure we don't go out of bounds
                        self.current_lane += 1
                if event.key == pg.K_UP or event.key == pg.K_w:  # Jump
                    if not self.is_jumping and not self.is_crouching:  # Prevent jumping while crouching
                        self.is_jumping = True
                        self.jump_timer = 30  # Updated to 30 frames
                if event.key == pg.K_DOWN or event.key == pg.K_s:  # Crouch
                    if not self.is_crouching and not self.is_jumping:  # Prevent crouching while jumping
                        self.is_crouching = True
                        self.crouch_timer = 30  # Updated to 30 frames
    
    def handle_continuous_input(self):
        """Handle continuous key presses (holding keys down)"""
        # Note: This section is commented out in the original code
        # Uncomment and modify as needed for continuous input
        """
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:  # W key - move cube closer
            self.cube_distance += 0.2  # Smaller increment for smoother movement
        if keys[pg.K_s]:  # S key - move cube further
            self.cube_distance -= 0.2  # Smaller increment for smoother movement
        if keys[pg.K_LEFT]:  # Left arrow key - move cube left
            self.cube_x -= 0.2  # Move left
        if keys[pg.K_RIGHT]:  # Right arrow key - move cube right
            self.cube_x += 0.2  # Move right
        if keys[pg.K_UP]:  # Up arrow key - move cube up
            self.cube_y += 0.2  # Move up
        if keys[pg.K_DOWN]:  # Down arrow key - move cube down
            self.cube_y -= 0.2  # Move down
        """
        pass
    
    def update_movement(self):
        """Update movement animations (jump, crouch, lane switching)"""
        # Handle jump
        if self.is_jumping:
            if self.jump_timer > 20:  # First phase of the jump (going up)
                self.cube_y += 0.4
            elif self.jump_timer > 10:  # Pause at the top
                pass  # Do nothing, stay at the top
            elif self.jump_timer > 0:  # Second phase of the jump (going down)
                self.cube_y -= 0.4
            self.jump_timer -= 1
            if self.jump_timer == 0:  # End of jump
                self.is_jumping = False

        # Handle crouch
        if self.is_crouching:
            if self.crouch_timer > 20:  # First phase of the crouch (going down)
                self.cube_y -= 0.4
            elif self.crouch_timer > 10:  # Pause at the bottom
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
