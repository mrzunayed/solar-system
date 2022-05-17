import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulator")

WHITE = (255, 255, 255)
SPACE_BLACK = (22, 24, 25)
LIGHT_GREY = (200, 200, 200)
DEEP_GREY = (50, 50, 50)
GOLD = (255, 215, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
ORANGE = (149, 58, 5)
BROWN = (160, 141, 130)

FONT = pygame.font.SysFont("comicsans", 12)


class Object:
    AU = 149.6e9
    G = 6.67428e-11
    SCALE = 250 / AU  # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name
        self.orbit = []
        self.sun = False
        self.distance_from_sun = 0
        self.x_velocity = 0
        self.y_velocity = 0

    def draw(self, window):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) >= 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(window, DEEP_GREY, False, updated_points, 2)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_from_sun / 1000)} km", 1, WHITE)
            window.blit(distance_text, (x + 10, y + 10))

        pygame.draw.circle(window, self.color, (x, y), self.radius)

    def attract(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_from_sun = distance

        force = self.G * self.mass * other.mass / (distance ** 2)
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update(self, objects):
        total_force_x, total_force_y = 0, 0
        for ob in objects:
            if self == ob:
                continue
            force_x, force_y = self.attract(ob)
            total_force_x += force_x
            total_force_y += force_y

        self.x_velocity += total_force_x / self.mass * self.TIMESTEP
        self.y_velocity += total_force_y / self.mass * self.TIMESTEP

        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    # Create planets
    sun = Object(0, 0, 30, GOLD, 1.988e30, "Sun")
    sun.sun = True

    earth = Object(-1 * Object.AU, 0, 16, BLUE, 5.9722e24, "Earth")
    earth.y_velocity = 29.783 * 1000

    mars = Object(-1.524 * Object.AU, 0, 12, RED, 6.4185e23, "Mars")
    mars.y_velocity = 24.077 * 1000

    mercury = Object(-0.387 * Object.AU, 0, 8, LIGHT_GREY, 3.3011e23, "Mercury")
    mercury.y_velocity = 47.362 * 1000

    venus = Object(0.723 * Object.AU, 0, 14, ORANGE, 4.8685e24, "Venus")
    venus.y_velocity = -35.02 * 1000

    # jupiter = Object(1.898 * Object.AU, 0, 20, BROWN, 1.8986e27, "Jupiter")
    # jupiter.y_velocity = -13.07 * 1000

    objects = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WIN.fill(SPACE_BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for obj in objects:
            obj.update(objects)
            obj.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
