import pygame as pg
from button import Button
import time

class ArduinoStartScreen:
    def __init__(self, screen_size):
        self.width, self.height = screen_size
        
        # Control selection buttons
        self.arduino_button = Button("Arduino Controls", (self.width // 2 - 120, self.height // 2 - 30), (240, 50))
        self.keyboard_button = Button("Keyboard Controls", (self.width // 2 - 120, self.height // 2 + 30), (240, 50))
        
        # State management
        self.selected_control = None  # "arduino" or "keyboard"
        self.arduino_status = "Not Connected"
        self.connection_messages = []
        self.final_time = None
        self.arduino_button_enabled = False  # Track if Arduino button should be enabled
        
        # Colors
        self.bg_color = (25, 25, 35)           # Dark background
        self.text_color = (255, 255, 255)      # White text
        self.success_color = (0, 255, 100)     # Green for success
        self.error_color = (255, 80, 80)       # Red for errors
        self.warning_color = (255, 200, 0)     # Yellow for warnings
        self.disabled_color = (80, 80, 80)     # Gray for disabled elements
        
        # Fonts
        pg.font.init()
        self.title_font = pg.font.Font(None, 48)
        self.subtitle_font = pg.font.Font(None, 32)
        self.text_font = pg.font.Font(None, 24)
        self.small_font = pg.font.Font(None, 20)

    def set_arduino_button_enabled(self, enabled):
        """Enable or disable the Arduino button based on connection status"""
        self.arduino_button_enabled = enabled

    def set_arduino_status(self, status, using_arduino=False):
        """Update Arduino connection status"""
        self.arduino_status = status
        if using_arduino:
            self.selected_control = "arduino"
        
    def add_connection_message(self, message, msg_type="info"):
        """Add a connection status message"""
        timestamp = time.strftime("%H:%M:%S")
        self.connection_messages.append({
            'text': f"[{timestamp}] {message}",
            'type': msg_type,
            'time': time.time()
        })
        # Keep only last 10 messages
        if len(self.connection_messages) > 10:
            self.connection_messages.pop(0)

    def set_final_time(self, time_str):
        """Set final game time for game over screen"""
        self.final_time = time_str

    def draw(self, surface):
        """Draw the start screen"""
        surface.fill(self.bg_color)
        
        # Draw title
        if self.final_time:
            title_text = "Game Over!"
            title_color = self.error_color
        else:
            title_text = "Force Cube Runner"
            title_color = self.text_color
            
        title_surface = self.title_font.render(title_text, True, title_color)
        title_x = self.width // 2 - title_surface.get_width() // 2
        surface.blit(title_surface, (title_x, 30))
        
        # Draw final time if game over
        if self.final_time:
            time_surface = self.subtitle_font.render(f"Final Time: {self.final_time}", True, self.success_color)
            time_x = self.width // 2 - time_surface.get_width() // 2
            surface.blit(time_surface, (time_x, 80))
        
        # Draw control selection section
        control_title = self.subtitle_font.render("Choose Control Method:", True, self.text_color)
        control_x = self.width // 2 - control_title.get_width() // 2
        surface.blit(control_title, (control_x, 140))
        
        # Update button colors based on selection and enable status
        if not self.arduino_button_enabled:
            # Arduino button disabled - gray it out
            self.arduino_button.bg_color = self.disabled_color
        elif self.selected_control == "arduino":
            self.arduino_button.bg_color = (0, 150, 0)  # Green when selected
        else:
            self.arduino_button.bg_color = (70, 130, 180)  # Default blue
            
        # Keyboard button is always enabled
        if self.selected_control == "keyboard":
            self.keyboard_button.bg_color = (0, 150, 0)  # Green when selected
        elif self.selected_control == "arduino":
            self.keyboard_button.bg_color = (100, 100, 100)  # Gray when not selected
        else:
            self.keyboard_button.bg_color = (70, 130, 180)  # Default blue
        
        # Draw control buttons
        self.arduino_button.draw(surface)
        self.keyboard_button.draw(surface)
        
        # Draw selection prompt
        if not self.selected_control:
            prompt_text = "Select your preferred control method above"
            prompt_surface = self.text_font.render(prompt_text, True, self.text_color)
            prompt_x = self.width // 2 - prompt_surface.get_width() // 2
            surface.blit(prompt_surface, (prompt_x, 420))
        
        # Draw connection messages log
        self.draw_connection_log(surface)
        
        pg.display.flip()

    def draw_control_instructions(self, surface):
        """Draw control method instructions"""
        instructions_y = 320
        
        if self.selected_control == "arduino":
            instructions = [
                "ARDUINO CONTROLS:",
                "Ultrasonic Sensor: Close = Crouch, Far = Jump",
                "Joystick: Left/Right = Change Lanes",
                "Real-time position control"
            ]
            color = self.success_color
        elif self.selected_control == "keyboard":
            instructions = [
                "KEYBOARD CONTROLS:",
                "LEFT ARROW = Left Lane, RIGHT ARROW = Right Lane",
                "UP ARROW = Jump, DOWN ARROW = Crouch",
                "R = Reset Timer, P = Pause/Resume"
            ]
            color = self.success_color
        else:
            instructions = [
                "Select a control method above to see instructions",
                "Arduino controls offer hardware immersion",
                "Keyboard controls are reliable and responsive"
            ]
            color = self.text_color
        
        for i, instruction in enumerate(instructions):
            text_surface = self.small_font.render(instruction, True, color)
            text_x = self.width // 2 - text_surface.get_width() // 2
            surface.blit(text_surface, (text_x, instructions_y + i * 25))

    def draw_connection_log(self, surface):
        """Draw Arduino connection messages log"""
        log_title = self.text_font.render("Connection Log:", True, self.text_color)
        surface.blit(log_title, (20, 450))
        
        current_time = time.time()
        y_offset = 475
        
        for message in self.connection_messages[-6:]:  # Show last 6 messages
            # Fade old messages
            age = current_time - message['time']
            if age > 10:  # Fade messages older than 10 seconds
                alpha = max(0, 255 - int((age - 10) * 25))
            else:
                alpha = 255
            
            # Choose color based on message type
            if message['type'] == 'success':
                color = self.success_color
            elif message['type'] == 'error':
                color = self.error_color
            elif message['type'] == 'warning':
                color = self.warning_color
            else:
                color = self.text_color
            
            # Apply alpha for fading
            color = (*color[:3], alpha) if alpha < 255 else color
            
            text_surface = self.small_font.render(message['text'], True, color)
            surface.blit(text_surface, (20, y_offset))
            y_offset += 20

    def handle_events(self, events):
        """Handle user input events"""
        for event in events:
            if event.type == pg.QUIT:
                return "QUIT"
            
            # Handle control selection
            if self.arduino_button.is_clicked(event):
                if self.arduino_button_enabled:
                    self.selected_control = "arduino"
                    self.add_connection_message("Arduino controls selected", "info")
                    return "SELECT_ARDUINO"
                else:
                    self.add_connection_message("Arduino not connected - cannot select Arduino controls", "error")
            
            if self.keyboard_button.is_clicked(event):
                self.selected_control = "keyboard"
                self.add_connection_message("Keyboard controls selected", "info")
                return "SELECT_KEYBOARD"
                
        return None

    def show_control_instructions(self, surface, control_type):
        """Show control instructions for 3 seconds before starting game"""
        import time
        
        start_time = time.time()
        countdown_duration = 3.0
        
        # Create fonts for the countdown screen
        title_font = pg.font.Font(None, 48)
        subtitle_font = pg.font.Font(None, 32)
        text_font = pg.font.Font(None, 24)
        countdown_font = pg.font.Font(None, 64)
        
        while time.time() - start_time < countdown_duration:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
            
            # Calculate remaining time
            remaining_time = countdown_duration - (time.time() - start_time)
            countdown = int(remaining_time) + 1
            
            # Clear screen with dark background
            surface.fill((25, 25, 35))
            
            # Draw title
            if control_type == "arduino":
                title_text = "Arduino Controls Ready!"
                title_color = (0, 255, 100)
            else:
                title_text = "Keyboard Controls Ready!"
                title_color = (0, 180, 255)
            
            title_surface = title_font.render(title_text, True, title_color)
            title_x = surface.get_width() // 2 - title_surface.get_width() // 2
            surface.blit(title_surface, (title_x, 50))
            
            # Draw control instructions
            y_offset = 120
            if control_type == "arduino":
                instructions = [
                    "ARDUINO CONTROLS:",
                    "",
                    "Ultrasonic Sensor:",
                    "   • Move closer = Crouch/Duck",
                    "   • Move farther = Jump/Rise",
                    "   • Middle distance = Normal height",
                    "",
                    "Joystick:",
                    "   • Push LEFT = Move to left lane",
                    "   • Push RIGHT = Move to right lane",
                    "   • CENTER = Stay in current lane",
                    "",
                    "Position yourself and control the cube in real-time!"
                ]
                text_color = (255, 255, 255)
            else:
                instructions = [
                    "KEYBOARD CONTROLS:",
                    "",
                    "Movement:",
                    "   • LEFT Arrow  = Move to left lane",
                    "   • RIGHT Arrow = Move to right lane",
                    "   • UP Arrow = Jump over obstacles",
                    "   • DOWN Arrow = Crouch under obstacles",
                    "",
                    "Game Controls:",
                    "   • R = Reset timer",
                    "   • P = Pause/Resume timer",
                    "",
                    "Use precise timing to avoid obstacles!"
                ]
                text_color = (255, 255, 255)
            
            for instruction in instructions:
                if instruction == "":
                    y_offset += 15
                    continue
                    
                if instruction.endswith("CONTROLS:"):
                    # Main section headers (ARDUINO CONTROLS: or KEYBOARD CONTROLS:)
                    text_surface = subtitle_font.render(instruction, True, title_color)
                elif instruction.endswith(":") and not instruction.endswith("CONTROLS:"):
                    # Sub-section headers (Ultrasonic Sensor:, Movement:, etc.)
                    text_surface = text_font.render(instruction, True, (255, 200, 0))
                elif instruction.startswith("Position yourself") or instruction.startswith("Use precise timing"):
                    # Tips
                    text_surface = text_font.render(instruction, True, (100, 255, 100))
                else:
                    # Regular instructions
                    text_surface = text_font.render(instruction, True, text_color)
                
                text_x = surface.get_width() // 2 - text_surface.get_width() // 2
                surface.blit(text_surface, (text_x, y_offset))
                y_offset += 25
            
            # Draw countdown
            countdown_text = f"Starting in {countdown}..."
            countdown_surface = countdown_font.render(countdown_text, True, (255, 255, 0))
            countdown_x = surface.get_width() // 2 - countdown_surface.get_width() // 2
            surface.blit(countdown_surface, (countdown_x, 500))
            
            pg.display.flip()
            time.sleep(0.1)  # Small delay for smooth countdown

    def reset_for_new_game(self):
        """Reset the screen for a new game"""
        self.final_time = None
        # Keep control selection and connection status
