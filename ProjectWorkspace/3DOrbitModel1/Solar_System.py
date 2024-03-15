import matplotlib.pyplot as plt
from vectors import Vector
import math
import itertools

class SolarSystem:
    def __init__(self, size):
        self.size = size
        self.bodies = []

        self.fig, self.ax = plt.subplots(
            1, 1, 
            subplot_kw={'projection': '3d'},
            figsize=(self.size/50, self.size/50),
              )
        
        self.fig.tight_layout()
        #self.ax.view_init(30, 30)
        
    def add_body(self, body ):
        self.bodies.append(body)

    def update_all(self):
        for body in self.bodies:
            body.move()
            body.draw()
    
    def draw_all(self):
        self.ax.set_xlim((-self.size / 2, self.size / 2))
        self.ax.set_ylim((-self.size / 2, self.size / 2))
        self.ax.set_zlim((-self.size / 2, self.size / 2))
        plt.pause(0.001)
        self.ax.clear()

    def calculate_all_body_interactions(self):
        bodies_copy = self.bodies.copy()
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:
                first.accel_due_to_gravity(second)


class SolarSystemBody:
    min_display_size = 10
    display_log_base =1.3

    def __init__(
            self,
            solar_system,
            mass,
            position=(0,0,0),
            velocity=(0,0,0),
    
    ):
        self.SolarSystem = solar_system
        self.mass = mass
        self.position = position
        self.velocity = Vector(*velocity)
        self.display_size = max(
            math.log(self.mass, self.display_log_base),
            self.min_display_size,
        )
        self.colour = 'black'

        self.SolarSystem.add_body(self, self)

    def move(self):
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
            self.position[2] + self.velocity[2],
        )
    def accel_due_to_gravity(self, other):
        distance = Vector(*other.position) - Vector(*self.position)
        distance_mag = distance.mag()
        
        force_mag = (self.mass * other.mass) / distance_mag ** 2
        force = distance.norm() * force_mag

        reverse = 1

        for body in self, other:
            acceleration = force / body.mass
            body.velocity += acceleration * reverse
            reverse = -1

    def draw(self):
        self.SolarSystem.ax.plot(
            *self.position,
            marker='o',
            markersize=self.display_size + self.position[0] / 30,
            color=self.colour,
        )

class Sun(SolarSystemBody):
   def __init__(
           self,
           SolarSystem,
           mass = 100000,
           position=(0,0,0),
           velocity=(0,0,0),
   ):
         super(Sun, self).__init__(SolarSystem, mass, position, velocity)
         self.colour = 'yellow'
         
class Planet(SolarSystemBody):
    colours = itertools.cycle(['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black'])

    def __init__(
            self,
            SolarSystem,
            mass= 10,
            position=(0,0,0),
            velocity=(0,0,0),
    ):
        super(Planet, self).__init__(SolarSystem, mass, position, velocity)
        self.colour = next(self.colours)
      