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
        # Wait counters for each object (only used for initial movement)
        wait_options = [0, 60, random.randint(0, 60)]
        random.shuffle(wait_options)
        self.left_wait = wait_options[0]
        self.middle_wait = wait_options[1]
        self.right_wait = wait_options[2]
        # Wait before reset counters (used only when object reaches reset point)
        self.left_wait_before_reset = 0
        self.middle_wait_before_reset = 0
        self.right_wait_before_reset = 0
        # Initial y positions for the spheres
        self.left_sphere_y = 0.0 if self.left_is_wall else random.choice([0.0, -3.0])
        self.middle_sphere_y = 0.0 if self.middle_is_wall else random.choice([0.0, -3.0])
        self.right_sphere_y = 0.0 if self.right_is_wall else random.choice([0.0, -3.0])
        # Initial random colors for spheres and walls
        self.left_color = self.random_color()
        self.middle_color = self.random_color()
        self.right_color = self.random_color()
        self.left_wall_color = self.random_color()
        self.middle_wall_color = self.random_color()
        self.right_wall_color = self.random_color()

    def random_color(self):
        return (random.random(), random.random(), random.random())

    def update_positions(self):
        # Only wait before moving right after the game starts
        if self.left_wait > 0:
            self.left_wait -= 1
        else:
            self.left_sphere_z += 0.5
        if self.middle_wait > 0:
            self.middle_wait -= 1
        else:
            self.middle_sphere_z += 0.5
        if self.right_wait > 0:
            self.right_wait -= 1
        else:
            self.right_sphere_z += 0.5
        self.reset_if_needed()

    def reset_if_needed(self):
        # Always wait before resetting an object
        if self.left_sphere_z > -5.0:
            if self.left_wait_before_reset > 0:
                self.left_wait_before_reset -= 1
            else:
                self.left_sphere_z = -50.0
                self.left_is_wall = random.choice([True, False])
                if self.left_is_wall and self.middle_is_wall and self.right_is_wall:
                    self.left_is_wall = False
                self.left_sphere_y = 0.0 if self.left_is_wall else random.choice([0.0, -3.0])
                self.left_wait_before_reset = random.randint(0, 60)
                self.left_color = self.random_color()
                self.left_wall_color = self.random_color()
        if self.middle_sphere_z > -5.0:
            if self.middle_wait_before_reset > 0:
                self.middle_wait_before_reset -= 1
            else:
                self.middle_sphere_z = -50.0
                self.middle_is_wall = random.choice([True, False])
                if self.middle_is_wall and self.left_is_wall and self.right_is_wall:
                    self.middle_is_wall = False
                self.middle_sphere_y = 0.0 if self.middle_is_wall else random.choice([0.0, -3.0])
                self.middle_wait_before_reset = random.randint(0, 60)
                self.middle_color = self.random_color()
                self.middle_wall_color = self.random_color()
        if self.right_sphere_z > -5.0:
            if self.right_wait_before_reset > 0:
                self.right_wait_before_reset -= 1
            else:
                self.right_sphere_z = -50.0
                self.right_is_wall = random.choice([True, False])
                if self.right_is_wall and self.left_is_wall and self.middle_is_wall:
                    self.right_is_wall = False
                self.right_sphere_y = 0.0 if self.right_is_wall else random.choice([0.0, -3.0])
                self.right_wait_before_reset = random.randint(0, 60)
                self.right_color = self.random_color()
                self.right_wall_color = self.random_color()

    def draw_objects(self, shapes, rotation_angle):
        # Draw left object
        if self.left_is_wall:
            shapes.draw_wall(-4.0, self.left_sphere_y, self.left_sphere_z, rotation_angle, height=3.0, color=self.left_wall_color)
        else:
            shapes.draw_textured_sphere(-4.0, self.left_sphere_y, self.left_sphere_z, radius=1.5, color=self.left_color, rotation_angle=rotation_angle)
        # Draw middle object
        if self.middle_is_wall:
            shapes.draw_wall(0.0, self.middle_sphere_y, self.middle_sphere_z, rotation_angle, height=3.0, color=self.middle_wall_color)
        else:
            shapes.draw_textured_sphere(0.0, self.middle_sphere_y, self.middle_sphere_z, radius=1.2, color=self.middle_color, rotation_angle=rotation_angle)
        # Draw right object
        if self.right_is_wall:
            shapes.draw_wall(4.0, self.right_sphere_y, self.right_sphere_z, rotation_angle, height=3.0, color=self.right_wall_color)
        else:
            shapes.draw_textured_sphere(4.0, self.right_sphere_y, self.right_sphere_z, radius=1.5, color=self.right_color, rotation_angle=rotation_angle)
