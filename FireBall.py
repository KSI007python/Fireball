import pygame
import math
import random

pygame.init()

screen = pygame.display.set_mode((800, 800))

running = True

gravity = False

class rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        pygame.draw.ellipse(screen, (255, 255, 255), (self.x-15, self.y-15, 30, 30))

    def move(self, velocity, angle):
        self.x += velocity*math.cos(math.radians(angle))
        self.y -= velocity*math.sin(math.radians(angle))

class particle:
    def __init__(self, x, y, radius, velocity, angle, color):
        self.x = x
        self.y = y
        self.radius = radius
        angle = math.radians(angle)
        self.vX = math.cos(angle)*velocity
        self.vY = math.sin(angle)*velocity
        self.color = color

    def update_pos(self):
        self.x -= self.vX
        self.y -= self.vY

    def show_particle(self):
        pygame.draw.ellipse(screen, self.color, (self.x-self.radius/2, self.y-self.radius/2, self.radius, self.radius))

particle_array = []

Rocket = rocket(380, 380)

angle = 90

def desperse_particle():
    particle_array.append(particle(
        Rocket.x,
        Rocket.y,
        random.randint(5, 30),
        1,
        random.randint(int(-angle%360-20), int(-angle%360+20)),
        random.choice([(255, 0, 0), (255, 255, 0), (255, 165, 0)])
    ))

def update_particle_array():
    i = 0
    while i < len(particle_array):
        particle_ = particle_array[i]
        particle_.update_pos()
        particle_.show_particle()
        particle_.radius -= 0.05
        if gravity:
            particle_.vY -= 0.01
        if particle_.x < 0 or particle_.x > 800:
            particle_.vX *= -0.9

        if particle_.y < 0 or particle_.y > 800:
            particle_.vY *= -0.9
        
        if particle_.radius < 1:
            particle_array.pop(i)
            i -= 1
        i += 1

velocity = 0

while running:
    screen.fill((0, 0, 0))

    update_particle_array()

    Rocket.show()
    
    if Rocket.x < 10:
        Rocket.x = 10
    if Rocket.x > 790:
        Rocket.x = 790
    if Rocket.y < 10:
        Rocket.y = 10
    if Rocket.y > 790:
        Rocket.y = 790

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        velocity = 1.5
        pygame.draw.ellipse(screen, (255, 255, 255), (Rocket.x-math.cos(math.radians(angle))*10-10, Rocket.y+math.sin(math.radians(angle))*10-10, 20, 20))
        pygame.draw.ellipse(screen, (255, 255, 0), (Rocket.x-math.cos(math.radians(angle))*10-12, Rocket.y+math.sin(math.radians(angle))*10-12, 25, 25))
        desperse_particle()
        Rocket.show()
    else:
        if velocity > 0:
            velocity -= 0.004
        else:
            velocity = 0
            pygame.draw.ellipse(screen, (255, 165, 0), (Rocket.x + math.cos(math.radians(angle))*30-5, Rocket.y - math.sin(math.radians(angle))*30-5, 10, 10))       

    Rocket.move(velocity, angle)
        
    if keys[pygame.K_RIGHT] and (velocity >= 1 or velocity == 0):
        angle -= 0.5

    if keys[pygame.K_LEFT] and (velocity >= 1 or velocity == 0):
        angle += 0.5
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()