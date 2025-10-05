from OpenGL.GL import *

class LaneMarkers:
    """
    Creates visual lane markers to distinguish the three lanes in the game
    Lane positions: Left (-5.0), Center (0.0), Right (+5.0)
    """
    
    def __init__(self):
        # Lane positions (matching the controls.py lanes)
        self.lane_positions = [-5.0, 0.0, 5.0]  # Left, Center, Right
        
        # Lane marker properties
        self.marker_width = 0.5
        self.marker_height = 1.0
        self.marker_depth = 0.2
        self.marker_distance = -20.0  # Behind the cube
        
        # Colors for different lane markers
        self.lane_colors = [
            (1.0, 0.3, 0.3),  # Left lane - Red
            (0.3, 1.0, 0.3),  # Center lane - Green  
            (0.3, 0.3, 1.0)   # Right lane - Blue
        ]
    
    @staticmethod
    def draw_lane_divider_boxes():
        """
        Draw two boxes positioned between the lanes to create visual separation
        These will be placed at x = -2.5 (between left and center) and x = +2.5 (between center and right)
        """
        divider_positions = [-2.5, 2.5]  # Between lanes
        divider_color = (0.8, 0.8, 0.8)  # Light gray
        
        for x_pos in divider_positions:
            LaneMarkers._draw_single_box(
                x=x_pos,
                y=-1.0,
                z=-18.0,
                width=0.3,
                height=2.0,
                depth=0.3,
                color=divider_color
            )
    
    @staticmethod
    def draw_lane_marker_boxes():
        """
        Draw boxes at each lane position to mark the lanes
        """
        lane_positions = [-5.0, 0.0, 5.0]
        lane_colors = [
            (1.0, 0.4, 0.4),  # Left lane - Light Red
            (0.4, 1.0, 0.4),  # Center lane - Light Green  
            (0.4, 0.4, 1.0)   # Right lane - Light Blue
        ]
        
        for i, (x_pos, color) in enumerate(zip(lane_positions, lane_colors)):
            LaneMarkers._draw_single_box(
                x=x_pos,
                y=-3.0,  # Below the cube
                z=-16.0,
                width=1.5,
                height=0.5,
                depth=1.0,
                color=color
            )
    
    @staticmethod
    def draw_lane_boundary_walls():
        """
        Draw tall walls on the sides to clearly define the play area
        """
        wall_positions = [-7.5, 7.5]  # Outside the leftmost and rightmost lanes
        wall_color = (0.6, 0.6, 0.6)  # Gray
        
        for x_pos in wall_positions:
            LaneMarkers._draw_single_box(
                x=x_pos,
                y=0.0,
                z=-17.0,
                width=0.5,
                height=6.0,
                depth=2.0,
                color=wall_color
            )
    
    @staticmethod
    def draw_ground_lanes():
        """
        Draw ground markers for each lane (flat rectangular strips)
        """
        lane_positions = [-5.0, 0.0, 5.0]
        lane_colors = [
            (0.9, 0.7, 0.7),  # Left lane - Light Red
            (0.7, 0.9, 0.7),  # Center lane - Light Green  
            (0.7, 0.7, 0.9)   # Right lane - Light Blue
        ]
        
        for x_pos, color in zip(lane_positions, lane_colors):
            LaneMarkers._draw_ground_strip(
                x=x_pos,
                y=-3.5,  # Ground level
                z=-15.0,
                width=2.0,
                depth=10.0,
                color=color
            )
    
    @staticmethod
    def _draw_single_box(x, y, z, width, height, depth, color):
        """
        Draw a single box at the specified position with given dimensions and color
        """
        glLoadIdentity()
        glTranslatef(x, y, z)
        
        # Half dimensions for vertex calculation
        w, h, d = width/2, height/2, depth/2
        
        # Define box vertices
        vertices = [
            [-w, -h, -d], [w, -h, -d], [w, h, -d], [-w, h, -d],  # Back face
            [-w, -h, d], [w, -h, d], [w, h, d], [-w, h, d]       # Front face
        ]
        
        # Define faces
        faces = [
            ([0, 1, 2, 3]),  # Back face
            ([4, 5, 6, 7]),  # Front face
            ([0, 1, 5, 4]),  # Bottom face
            ([2, 3, 7, 6]),  # Top face
            ([0, 3, 7, 4]),  # Left face
            ([1, 2, 6, 5])   # Right face
        ]
        
        # Set color and draw
        glColor3f(*color)
        
        for face in faces:
            glBegin(GL_QUADS)
            for vertex_index in face:
                glVertex3f(*vertices[vertex_index])
            glEnd()
    
    @staticmethod
    def _draw_ground_strip(x, y, z, width, depth, color):
        """
        Draw a flat rectangular strip on the ground
        """
        glLoadIdentity()
        glTranslatef(x, y, z)
        
        # Half dimensions
        w, d = width/2, depth/2
        
        # Ground strip vertices (flat rectangle)
        vertices = [
            [-w, 0, -d],  # Back-left
            [w, 0, -d],   # Back-right
            [w, 0, d],    # Front-right
            [-w, 0, d]    # Front-left
        ]
        
        # Set color and draw
        glColor3f(*color)
        glBegin(GL_QUADS)
        for vertex in vertices:
            glVertex3f(*vertex)
        glEnd()
    
    @staticmethod
    def draw_all_lane_markers():
        """
        Draw all lane marking elements
        """
        # Draw ground lane strips
        LaneMarkers.draw_ground_lanes()
        
        # Draw lane divider boxes
        LaneMarkers.draw_lane_divider_boxes()
        
        # Draw lane marker boxes
        LaneMarkers.draw_lane_marker_boxes()
        
        # Draw boundary walls
        LaneMarkers.draw_lane_boundary_walls()
    
    @staticmethod
    def draw_minimal_lane_markers():
        """
        Draw just the essential lane markers (divider boxes only)
        """
        LaneMarkers.draw_lane_divider_boxes()
    
    @staticmethod
    def draw_simple_lane_ground():
        """
        Draw just the ground lane strips
        """
        LaneMarkers.draw_ground_lanes()
