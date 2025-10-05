import random

class SphereManager:
    def __init__(self):
        # Initial z positions for the spheres
        self.left_sphere_z = -50.0
        self.middle_sphere_z = -50.0
        self.right_sphere_z = -50.0
        # Track if each object is a wall
        self.left_is_wall = random.choice([True, False])
        self.middle_is_wall = random.choice([True, False])
        self.right_is_wall = random.choice([True, False])
        # Initial y positions for the spheres
        self.left_sphere_y = 0.0 if self.left_is_wall else random.choice([0.0, -3.0])
        self.middle_sphere_y = 0.0 if self.middle_is_wall else random.choice([0.0, -3.0])
        self.right_sphere_y = 0.0 if self.right_is_wall else random.choice([0.0, -3.0])

    def update_positions(self):
        # Move spheres closer
        self.left_sphere_z += 0.5
        self.middle_sphere_z += 0.5
        self.right_sphere_z += 0.5
        self.reset_if_needed()

    def reset_if_needed(self):
        # Reset spheres when they get too close
        if self.left_sphere_z > -5.0:
            self.left_sphere_z = -50.0
            self.left_is_wall = random.choice([True, False])
            self.left_sphere_y = 0.0 if self.left_is_wall else random.choice([0.0, -3.0])
        if self.middle_sphere_z > -5.0:
            self.middle_sphere_z = -50.0
            self.middle_is_wall = random.choice([True, False])
            self.middle_sphere_y = 0.0 if self.middle_is_wall else random.choice([0.0, -3.0])
        if self.right_sphere_z > -5.0:
            self.right_sphere_z = -50.0
            self.right_is_wall = random.choice([True, False])
            self.right_sphere_y = 0.0 if self.right_is_wall else random.choice([0.0, -3.0])

    def draw_objects(self, shapes, rotation_angle):
        # Draw left object
        if self.left_is_wall:
            shapes.draw_wall(-4.0, self.left_sphere_y, self.left_sphere_z, rotation_angle, height=3.0)
        else:
            shapes.draw_textured_sphere(-4.0, self.left_sphere_y, self.left_sphere_z, radius=1.5, color=(1.0, 0.3, 0.3), rotation_angle=rotation_angle)
        # Draw middle object
        if self.middle_is_wall:
            shapes.draw_wall(0.0, self.middle_sphere_y, self.middle_sphere_z, rotation_angle, height=3.0)
        else:
            shapes.draw_textured_sphere(0.0, self.middle_sphere_y, self.middle_sphere_z, radius=1.2, color=(0.3, 1.0, 0.3), rotation_angle=rotation_angle)
        # Draw right object
        if self.right_is_wall:
            shapes.draw_wall(4.0, self.right_sphere_y, self.right_sphere_z, rotation_angle, height=3.0)
        else:
            shapes.draw_textured_sphere(4.0, self.right_sphere_y, self.right_sphere_z, radius=1.5, color=(0.3, 0.3, 1.0), rotation_angle=rotation_angle)
