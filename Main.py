#Original way to create a basic screen
# import pygame
# pygame.init()
#
# win = pygame.display.set_mode((500, 500))
#
# pygame.display.set_caption("First Game")
#
# x = 50
# y = 50
# width = 40
# height = 60
# vel = 5
#
# run = True
# while run:
#     pygame.time.delay(100)
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#
# pygame.quit()

#The link below shows and explains how to drop spheres with gravity playing a role with Pymunk and Pygames interacting.
#https://github.com/viblo/pymunk/blob/08fb141b81c0240513fc16e276d5ade5b0506512/docs/html/_sources/tutorials/SlideAndPinJoint.rst.txt

import sys, random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util

def add_ball(space):
    mass = 1
    radius = 20
    moment = pymunk.moment_for_circle(mass, 0, radius) #sets moment of inertia
    body = pymunk.Body(mass, moment) #creates body
    x = random.randint(120, 380)
    body.position = x, 550 #sets position, (x, y) coordinate with x generated randomly
    shape = pymunk.Circle(body, radius) #body needs to be defined as a shape to collide with things
    space.add(body, shape) #add shape to the space
    return shape

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Object Dropping, Affect of Gravity")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0, -980) #x-coordinate is for gravity in x-direction, y-coordinate for gravity in y-direction


    balls = []
    draw_options = pymunk.pygame_util.DrawOptions(screen)


    ticks_to_next_ball = 10
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        space.step(1/50.0) #amount of steps the object takes downwards at a time.

        screen.fill((255,255,255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(40)

if __name__ == '__main__':
    main()