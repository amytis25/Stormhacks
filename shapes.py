from OpenGL.GL import *

class Shapes:
    @staticmethod
    def draw_cube(cube_x, cube_y, cube_distance, rotation_angle):
        """Draw a cube at the specified position with rotation"""
        glLoadIdentity()
        glTranslatef(cube_x, cube_y, cube_distance)  # Use variable distance from camera
        glRotatef(rotation_angle, 1, 1, 0)  # Rotate around all axes - fixed rotation
        
        # Define cube vertices
        vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], # Back face
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1] # Front face
        ]
        
        # Define faces (vertex indices) and colors
        faces = [
            ([0, 1, 2, 3], (199/255, 159/255, 212/255)),  # Back face
            ([4, 5, 6, 7], (199/255, 159/255, 212/255)),  # Front face
            ([0, 1, 5, 4], (159/255, 186/255, 212/255)),  # Bottom face
            ([2, 3, 7, 6], (159/255, 186/255, 212/255)),  # Top face
            ([0, 3, 7, 4], (159/255, 159/255, 212/255)),  # Left face
            ([1, 2, 6, 5], (159/255, 159/255, 212/255))   # Right face
        ]
        
        # Draw each face
        for face, color in faces:
            glColor3f(*color)
            glBegin(GL_QUADS)
            for vertex_index in face:
                glVertex3f(*vertices[vertex_index])
            glEnd()
    
    @staticmethod
    def draw_triangle_left(rotation_angle):
        """Draw a pyramid on the left side"""
        glLoadIdentity()
        glTranslatef(-4.0, 0.0, -15.0)  # Position pyramid to the left
        glRotatef(rotation_angle, 1, 1, 1)  # Rotate around all axes
        
        # Define pyramid vertices
        # Apex (top point)
        apex = [0.0, 2.0, 0.0]
        
        # Base vertices (square base)
        base = [
            [-1.5, -1.0, 1.5], # Front-left
            [1.5, -1.0, 1.5],  # Front-right
            [1.5, -1.0, -1.5], # Back-right
            [-1.5, -1.0, -1.5] # Back-left
        ]
        
        # Draw pyramid faces
        # Front face (apex + front edge of base) 
        glColor3f(175/255, 205/255, 237/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[0])  # Front-left
        glVertex3f(*base[1])  # Front-right
        glEnd()
        
        # Right face (apex + right edge of base) 
        glColor3f(175/255, 237/255, 209/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[1])  # Front-right
        glVertex3f(*base[2])  # Back-right
        glEnd()
        
        # Back face (apex + back edge of base) 
        glColor3f(175/255, 205/255, 237/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[2])  # Back-right
        glVertex3f(*base[3])  # Back-left
        glEnd()
        
        # Left face (apex + left edge of base) 
        glColor3f(175/255, 237/255, 209/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[3])  # Back-left
        glVertex3f(*base[0])  # Front-left
        glEnd()
        
        # Base (square bottom) 
        glColor3f(84/255, 118/255, 153/255)
        glBegin(GL_QUADS)
        glVertex3f(*base[0])  # Front-left
        glVertex3f(*base[1])  # Front-right
        glVertex3f(*base[2])  # Back-right
        glVertex3f(*base[3])  # Back-left
        glEnd()

    @staticmethod
    def draw_triangle_right(rotation_angle):
        """Draw a pyramid on the right side"""
        glLoadIdentity()
        glTranslatef(4.0, 0.0, -15.0)  # Position pyramid to the right
        glRotatef(rotation_angle, -1, 1, -1)  # Rotate around all axes
        
        # Define pyramid vertices
        # Apex (top point)
        apex = [0.0, 2.0, 0.0]
        
        # Base vertices (square base)
        base = [
            [-1.5, -1.0, 1.5],  # Front-left
            [1.5, -1.0, 1.5],   # Front-right
            [1.5, -1.0, -1.5],  # Back-right
            [-1.5, -1.0, -1.5]  # Back-left
        ]
        
        # Draw pyramid faces
        # Front face (apex + front edge of base) 
        glColor3f(175/255, 205/255, 237/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[0])  # Front-left
        glVertex3f(*base[1])  # Front-right
        glEnd()
        
        # Right face (apex + right edge of base) 
        glColor3f(175/255, 237/255, 209/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[1])  # Front-right
        glVertex3f(*base[2])  # Back-right
        glEnd()
        
        # Back face (apex + back edge of base) 
        glColor3f(175/255, 205/255, 237/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[2])  # Back-right
        glVertex3f(*base[3])  # Back-left
        glEnd()
        
        # Left face (apex + left edge of base) 
        glColor3f(175/255, 237/255, 209/255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[3])  # Back-left
        glVertex3f(*base[0])  # Front-left
        glEnd()
        
        # Base (square bottom) 
        glColor3f(84/255, 118/255, 153/255)
        glBegin(GL_QUADS)
        glVertex3f(*base[0])  # Front-left
        glVertex3f(*base[1])  # Front-right
        glVertex3f(*base[2])  # Back-right
        glVertex3f(*base[3])  # Back-left
        glEnd()
