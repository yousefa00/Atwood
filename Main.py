# Original way to create a basic screen
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

# The link below shows and explains how to drop spheres with gravity playing a role with Pymunk and Pygames interacting.
# https://github.com/viblo/pymunk/blob/08fb141b81c0240513fc16e276d5ade5b0506512/docs/html/_sources/tutorials/SlideAndPinJoint.rst.txt

import sys, random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util

import math, sys, random

import pygame
import re
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk import Vec2d
import pymunk.pygame_util

object_draging = False #object refers to any of the circles being dropped. This boolean indicates whether object is being dragged (mouse down) or not (mouse up).


#testing
def draw_collision(arbiter, space, data):
    for c in arbiter.contact_point_set.points:
        r = max(3, abs(c.distance * 5))
        r = int(r)

        p = pymunk.pygame_util.to_pygame(c.point_a, data["surface"])
        pygame.draw.circle(data["surface"], THECOLORS["black"], p, r, 1)


def main():
    global contact
    global shape_to_remove
    global object_draging
    global screen
    global balls
    global space

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True

    ### Physics stuff
    space = pymunk.Space()  # creates a space for the physics
    space.gravity = (0.0, -980.0)  # sets the gravity of the space
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    # disable the build in debug draw of collision point since we use our own code.
    draw_options.flags = draw_options.flags ^ pymunk.pygame_util.DrawOptions.DRAW_COLLISION_POINTS
    ## Balls
    balls = []

    ### walls
    static_lines = [pymunk.Segment(space.static_body, (11.0, 280.0), (407.0, 246.0), 0.0)
        , pymunk.Segment(space.static_body, (407.0, 246.0), (407.0, 343.0), 0.0)
                    ]
    for l in static_lines:
        l.friction = 0.5
    space.add(static_lines)

    # ticks_to_next_ball = 10

    ch = space.add_collision_handler(0, 0)
    ch.data["surface"] = screen
    ch.post_solve = draw_collision

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            # Added interactive stuff starting here:
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # When event.button == 1, that's referring to a left click

                    # 1 - left click
                    #
                    # 2 - middle click
                    #
                    # 3 - right click
                    #
                    # 4 - scroll up
                    #
                    # 5 - scroll down
                    for ball in balls:
                        surface = pygame.Surface(screen.get_size())
                        print("pos")
                        print(ball.body.position)
                        print(pymunk.pygame_util.get_mouse_pos(surface))
                        # mouse_x, mouse_y = event.pos

                        if ball.body.position == pymunk.pygame_util.get_mouse_pos(surface):
                            # if (ball.body.position.x )
                            space.gravity = (0, 0)
                            object_draging = True
                            # mouse_x, mouse_y = event.pos
                            offset_x = ball.x - mouse_x
                            offset_y = ball.y - mouse_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    space.gravity = (0, -980)
                    object_draging = False

            elif event.type == pygame.MOUSEMOTION:
                if object_draging:
                    for ball in balls:
                        mouse_x, mouse_y = event.pos
                        ball.x = mouse_x + offset_x
                        ball.y = mouse_y + offset_y
            # Interactive stuff ends here

            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "contact_with_friction.png")
            elif event.type == KEYDOWN and event.key == K_s:
                pos = pygame.mouse.get_pos()
                final = str(pos)
                x = final[final.find('(') + len('('):final.rfind(',')]
                y = final[final.find(',') + len(','):final.rfind(')')]
                add_ramp(100, 45, x, y, 0.1)

            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                final = str(pos)
                x = final[final.find('(') + len('('):final.rfind(',')]
                y = final[final.find(',') + len(','):final.rfind(')')]
                add_circle(0.1, 25, x, y, 0.5)

            # adds a square when the 'A' key is pressed; change around later for better UI
            if event.type == KEYDOWN and event.key == K_a:
                pos = pygame.mouse.get_pos()
                final = str(pos)
                x = final[final.find('(') + len('('):final.rfind(',')]
                y = final[final.find(',') + len(','):final.rfind(')')]
                add_square(0.1, 50.0, 50.0, x, y, 0.5)

        # ticks_to_next_ball -= 1
        # if ticks_to_next_ball <= 0:
        #     ticks_to_next_ball = 100
        #     mass = 0.1
        #     radius = 25
        #     inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        #     body = pymunk.Body(mass, inertia)
        #     pos = pygame.mouse.get_pos()
        #     final = str(pos)
        #     x = final[final.find('(')+len('('):final.rfind(',')]
        #     print(x)
        #     y = final[final.find(',') + len(','):final.rfind(')')]
        #     print(int(x), int(y))
        #     body.position = int(x), (600 - int(y))
        #     shape = pymunk.Circle(body, radius, (0, 0))
        #     shape.friction = 0.5
        #     space.add(body, shape)
        #     balls.append(shape)

        ### Clear screen
        screen.fill(THECOLORS["white"])

        ### Draw stuff
        space.debug_draw(draw_options)

        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 200: balls_to_remove.append(ball)
        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        ### Update physics
        dt = 1.0 / 60.0
        for x in range(1):
            space.step(dt)

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


#adds a circle to the screen with changeabe mass, radius, x and y position, and friction coef
def add_circle(mass, radius, xpos, ypos, friction):
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = int(xpos), (600 - int(ypos))
    shape = pymunk.Circle(body, radius, (0, 0))
    shape.friction = friction
    space.add(body, shape)
    balls.append(shape)


# adds a square to the screen with changeable mass, width, height, x and y positions, and friction coef
def add_square(mass, width, height, xpos, ypos, friction):
    inertia = pymunk.moment_for_box(mass, (width, height))
    body = pymunk.Body(mass, inertia)
    body.position = int(xpos), (600 - int(ypos))
    shape = pymunk.Poly.create_box(body, (width, height), 0)  # adding a radius (third param) bevels corners of poly
    shape.friction = friction
    space.add(body, shape)


def add_ramp(mass, degree, xpos, ypos, friction):
    tan = math.tan((degree * (math.pi / 180)))
    height = 100 / tan  #height adjusts to make degree applicable
    inertia = pymunk.moment_for_poly(mass, [(0, 0), (100, 0), (0, height)], (0, 0), 0)  # the length is always 100
    body = pymunk.Body(mass, inertia)
    body.position = int(xpos), (600 - int(ypos))
    shape = pymunk.Poly(body, [(0, 0), (100, 0), (0, height)])  # adding a radius (a third param) bevels corners of poly
    shape.friction = friction
    space.add(body, shape)


if __name__ == '__main__':
    sys.exit(main())