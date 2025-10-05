import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
import time

class GameTimer:
    """
    On-screen timer for the game that displays in format: MM:SS:mmm (minutes:seconds:milliseconds)
    """
    
    def __init__(self):
        # Initialize pygame font
        pg.font.init()
        self.font = pg.font.Font(None, 48)  # Font for timer display
        
        # Timer variables
        self.start_time = time.time()
        self.paused_time = 0
        self.is_paused = False
        
        # Display properties
        self.timer_color = (255, 255, 255)  # White text
        self.position = (20, 20)  # Top-left position
        
    def reset_timer(self):
        """Reset the timer to 00:00:000"""
        self.start_time = time.time()
        self.paused_time = 0
        self.is_paused = False
    
    def pause_timer(self):
        """Pause the timer"""
        if not self.is_paused:
            self.paused_time = time.time() - self.start_time
            self.is_paused = True
    
    def resume_timer(self):
        """Resume the timer"""
        if self.is_paused:
            self.start_time = time.time() - self.paused_time
            self.is_paused = False
    
    def get_elapsed_time(self):
        """Get elapsed time in seconds"""
        if self.is_paused:
            return self.paused_time
        else:
            return time.time() - self.start_time
    
    def format_time(self, elapsed_time):
        """Format time as MM:SS:mmm"""
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time % 1) * 1000)
        
        return f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
    
    def create_timer_texture(self, text):
        """Create an OpenGL texture from timer text"""
        try:
            # Render text to pygame surface
            text_surface = self.font.render(text, True, self.timer_color)
            text_width = text_surface.get_width()
            text_height = text_surface.get_height()
            
            # Convert pygame surface to OpenGL texture format
            text_data = pg.image.tostring(text_surface, "RGBA", False)  # Changed from True to False
            
            # Generate OpenGL texture
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            
            # Set texture parameters
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            
            # Upload texture data
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_width, text_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
            
            return texture_id, text_width, text_height
            
        except Exception as e:
            print(f"Error creating timer texture: {e}")
            return None, 0, 0
    
    def draw_timer_2d(self):
        """Draw timer using 2D overlay method (simpler approach)"""
        elapsed_time = self.get_elapsed_time()
        time_text = self.format_time(elapsed_time)
        
        # Save current OpenGL state
        glPushMatrix()
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        
        # Switch to 2D rendering
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, 800, 600, 0, -1, 1)  # 2D orthographic projection
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Disable depth testing for 2D overlay
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Create and draw timer texture
        texture_id, width, height = self.create_timer_texture(time_text)
        
        if texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glColor4f(1.0, 1.0, 1.0, 1.0)  # White color
            
            x, y = self.position
            
            # Draw textured quad with corrected texture coordinates
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex2f(x, y)                    # Top-left
            glTexCoord2f(1, 0); glVertex2f(x + width, y)            # Top-right
            glTexCoord2f(1, 1); glVertex2f(x + width, y + height)   # Bottom-right
            glTexCoord2f(0, 1); glVertex2f(x, y + height)           # Bottom-left
            glEnd()
            
            glDisable(GL_TEXTURE_2D)
            glDeleteTextures([texture_id])  # Clean up texture
        
        # Restore OpenGL state
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        glPopAttrib()
        glPopMatrix()
    
    def draw_timer_simple(self):
        """Draw timer using simple OpenGL text rendering (fallback method)"""
        elapsed_time = self.get_elapsed_time()
        time_text = self.format_time(elapsed_time)
        
        # Save current state
        glPushMatrix()
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        
        # Switch to 2D mode
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, 800, 0, 600, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Disable depth testing
        glDisable(GL_DEPTH_TEST)
        
        # Set color to white
        glColor3f(1.0, 1.0, 1.0)
        
        # Position text (top-left, accounting for inverted Y)
        glRasterPos2f(20, 580)
        
        # Draw each character (basic method)
        for char in time_text:
            # This is a simple fallback - actual text rendering would need a font library
            pass
        
        # Restore state
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopAttrib()
        glPopMatrix()
        
        # Print to console as backup
        print(f"Timer: {time_text}", end='\r')
    
    def draw_timer(self):
        """Main draw method - tries 2D overlay first, falls back to console"""
        try:
            self.draw_timer_2d()
        except Exception as e:
            # Fallback to console output
            elapsed_time = self.get_elapsed_time()
            time_text = self.format_time(elapsed_time)
            print(f"Timer: {time_text}", end='\r')
    
    def set_position(self, x, y):
        """Set timer position on screen"""
        self.position = (x, y)
    
    def set_color(self, r, g, b):
        """Set timer text color (RGB values 0-255)"""
        self.timer_color = (r, g, b)
