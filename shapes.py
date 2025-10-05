from OpenGL.GL import *

class Shapes:
    @staticmethod
    def draw_wall(wall_x, wall_y, wall_distance, rotation_angle, height=3.0, width=3.0):
        """Draw a wall (tall cube) at the specified position with rotation"""
        glLoadIdentity()
        glTranslatef(wall_x, wall_y, wall_distance)
        glRotatef(rotation_angle, 1, 1, 0)

        # Define wall vertices (taller than cube)
        half_width = width / 2.0
        vertices = [
            [-half_width, -height, -1], [half_width, -height, -1], [half_width, height, -1], [-half_width, height, -1], # Back face
            [-half_width, -height, 1], [half_width, -height, 1], [half_width, height, 1], [-half_width, height, 1] # Front face
        ]

        # Use same faces/colors as cube
        faces = [
            ([0, 1, 2, 3], (199/255, 159/255, 212/255)),  # Back face
            ([4, 5, 6, 7], (199/255, 159/255, 212/255)),  # Front face
            ([0, 1, 5, 4], (159/255, 186/255, 212/255)),  # Bottom face
            ([2, 3, 7, 6], (159/255, 186/255, 212/255)),  # Top face
            ([0, 3, 7, 4], (159/255, 159/255, 212/255)),  # Left face
            ([1, 2, 6, 5], (159/255, 159/255, 212/255))   # Right face
        ]

        for face, color in faces:
            glColor3f(*color)
            glBegin(GL_QUADS)
            for vertex_index in face:
                glVertex3f(*vertices[vertex_index])
            glEnd()
            
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
    def draw_triangle(position, rotation_angle):
        """Draw a pyramid (triangle) at a specified position with rotation"""
        glLoadIdentity()
        glTranslatef(*position)  # Position the triangle
        glRotatef(rotation_angle, 1, 1, 1)  # Rotate around all axes

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
        glColor3f(175 / 255, 205 / 255, 237 / 255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[0])  # Front-left
        glVertex3f(*base[1])  # Front-right
        glEnd()

        # Right face (apex + right edge of base)
        glColor3f(175 / 255, 237 / 255, 209 / 255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[1])  # Front-right
        glVertex3f(*base[2])  # Back-right
        glEnd()

        # Back face (apex + back edge of base)
        glColor3f(175 / 255, 205 / 255, 237 / 255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[2])  # Back-right
        glVertex3f(*base[3])  # Back-left
        glEnd()

        # Left face (apex + left edge of base)
        glColor3f(175 / 255, 237 / 255, 209 / 255)
        glBegin(GL_TRIANGLES)
        glVertex3f(*apex)
        glVertex3f(*base[3])  # Back-left
        glVertex3f(*base[0])  # Front-left
        glEnd()

        # Base (square bottom)
        glColor3f(84 / 255, 118 / 255, 153 / 255)
        glBegin(GL_QUADS)
        glVertex3f(*base[0])  # Front-left
        glVertex3f(*base[1])  # Front-right
        glVertex3f(*base[2])  # Back-right
        glVertex3f(*base[3])  # Back-left
        glEnd()
    
    @staticmethod
    def draw_sphere(sphere_x, sphere_y, sphere_z, radius=1.0, color=(0.5, 0.8, 1.0), slices=20, stacks=20):
        """
        Draw a sphere at the specified position
        
        Parameters:
        - sphere_x, sphere_y, sphere_z: Position coordinates
        - radius: Sphere radius (default: 1.0)
        - color: RGB color tuple (default: light blue)
        - slices: Number of vertical divisions (default: 20)
        - stacks: Number of horizontal divisions (default: 20)
        """
        import math
        
        glLoadIdentity()
        glTranslatef(sphere_x, sphere_y, sphere_z)
        glColor3f(*color)
        
        # Generate sphere vertices using spherical coordinates
        vertices = []
        
        # Generate vertices
        for i in range(stacks + 1):
            phi = math.pi * i / stacks  # Latitude angle (0 to pi)
            for j in range(slices + 1):
                theta = 2.0 * math.pi * j / slices  # Longitude angle (0 to 2*pi)
                
                x = radius * math.sin(phi) * math.cos(theta)
                y = radius * math.cos(phi)
                z = radius * math.sin(phi) * math.sin(theta)
                
                vertices.append((x, y, z))
        
        # Draw sphere using triangle strips
        for i in range(stacks):
            glBegin(GL_TRIANGLE_STRIP)
            for j in range(slices + 1):
                # Current vertex
                current = i * (slices + 1) + j
                # Next stack vertex
                next_stack = (i + 1) * (slices + 1) + j
                
                glVertex3f(*vertices[current])
                glVertex3f(*vertices[next_stack])
            glEnd()
    
    @staticmethod
    def draw_simple_sphere(sphere_x, sphere_y, sphere_z, radius=1.0, color=(0.5, 0.8, 1.0)):
        """
        Draw a simple sphere using fewer vertices for better performance
        """
        import math
        
        glLoadIdentity()
        glTranslatef(sphere_x, sphere_y, sphere_z)
        glColor3f(*color)
        
        slices = 12  # Fewer divisions for simpler sphere
        stacks = 8
        
        # Generate and draw sphere
        for i in range(stacks):
            lat0 = math.pi * (-0.5 + float(i) / stacks)
            lat1 = math.pi * (-0.5 + float(i + 1) / stacks)
            
            z0 = radius * math.sin(lat0)
            z1 = radius * math.sin(lat1)
            zr0 = radius * math.cos(lat0)
            zr1 = radius * math.cos(lat1)
            
            glBegin(GL_QUAD_STRIP)
            for j in range(slices + 1):
                lng = 2 * math.pi * float(j) / slices
                x = math.cos(lng)
                y = math.sin(lng)
                
                glVertex3f(x * zr0, y * zr0, z0)
                glVertex3f(x * zr1, y * zr1, z1)
            glEnd()
    
    @staticmethod
    def draw_textured_sphere(sphere_x, sphere_y, sphere_z, radius=1.0, color=(1.0, 0.7, 0.3), rotation_angle=0):
        """
        Draw a sphere with rotation and gradient-like coloring
        """
        import math
        
        glLoadIdentity()
        glTranslatef(sphere_x, sphere_y, sphere_z)
        glRotatef(rotation_angle, 0, 1, 0)  # Rotate around Y-axis
        
        slices = 16
        stacks = 12
        
        for i in range(stacks):
            lat0 = math.pi * (-0.5 + float(i) / stacks)
            lat1 = math.pi * (-0.5 + float(i + 1) / stacks)
            
            z0 = radius * math.sin(lat0)
            z1 = radius * math.sin(lat1)
            zr0 = radius * math.cos(lat0)
            zr1 = radius * math.cos(lat1)
            
            # Vary color based on height for gradient effect
            color_factor = 0.5 + 0.5 * (float(i) / stacks)
            glColor3f(color[0] * color_factor, color[1] * color_factor, color[2] * color_factor)
            
            glBegin(GL_QUAD_STRIP)
            for j in range(slices + 1):
                lng = 2 * math.pi * float(j) / slices
                x = math.cos(lng)
                y = math.sin(lng)
                
                glVertex3f(x * zr0, y * zr0, z0)
                glVertex3f(x * zr1, y * zr1, z1)
            glEnd()