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
from pygame import mouse
import pymunk
from pymunk import Vec2d
import pymunk.pygame_util

object_draging = False  # object refers to any of the circles being dropped. This boolean indicates whether object is being dragged (mouse down) or not (mouse up)
square_draging = False  # refers to square object being dragged
ramp_dragging = False  # refers to ramp object being dragged
flipped_ramp_dragging = False
runonce = False

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
    global square_draging
    global ramp_dragging
    global flipped_ramp_dragging
    global screen
    global numGrav
    numGrav = 1
    global balls
    global squares
    global ramps
    global flipped_ramps
    global space

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True

    ### Physics stuff
    global space
    space = pymunk.Space()  # creates a space for the physics

    draw_options = pymunk.pygame_util.DrawOptions(screen)
    # disable the build in debug draw of collision point since we use our own code.
    draw_options.flags = draw_options.flags ^ pymunk.pygame_util.DrawOptions.DRAW_COLLISION_POINTS
    ## Balls
    balls = []
    squares = []
    ramps = []
    flipped_ramps = []

    ### walls
    static_lines = [pymunk.Segment(space.static_body, (0, 5), (600, 5), 5)
        , pymunk.Segment(space.static_body, (595, 600), (595, 0), 5), pymunk.Segment(space.static_body, (0, 596), (600, 596), 5),
                    pymunk.Segment(space.static_body, (4, 0), (4, 600), 5)
                    ]
    for l in static_lines:
        l.friction = 0.5
    space.add(static_lines)

    # ticks_to_next_ball = 10

    ch = space.add_collision_handler(0, 0)
    ch.data["surface"] = screen
    ch.post_solve = draw_collision
    w, h = pygame.display.get_surface().get_size()

    while running:
        global ball
        global square
        global index_dragging
        global square_index_dragging
        global ramp_index_dragging
        global flipped_ramp_index_dragging
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
                    index = -1
                    squareIndex = -1
                    ramp_index = -1
                    flipped_ramp_index = -1
                    for ball in balls:
                        surface = pygame.Surface(screen.get_size())
                        mouse_x, mouse_y = event.pos
                        index += 1
                        if (math.sqrt(math.pow(ball.body.position.x - mouse_x, 2) + math.pow((600-ball.body.position.y) - mouse_y, 2))) <= 25:
                            index_dragging = index  # saves the index of the ball that is clicked
                            space.gravity = (0, 0)
                            object_draging = True

                    for square in squares:
                        mouse_x, mouse_y = event.pos
                        squareIndex += 1
                        if mouse_x + 50 >= square.body.position.x and mouse_x <= square.body.position.x + 50 and mouse_y + 50 >= (600-square.body.position.y) and mouse_y <= (600-square.body.position.y) + 50:
                            square_index_dragging = squareIndex  # saves the index of the ball that is clicked
                            space.gravity = (0, 0)
                            square_draging = True
                            #mouse_x, mouse_y = event.pos

                    for ramp in ramps:
                        mouse_x, mouse_y = event.pos
                        ramp_index += 1
                        if mouse_x >= ramp.body.position.x and mouse_x <= ramp.body.position.x + 50 and mouse_y <= (600 - ramp.body.position.y) and mouse_y + 50 >= (600-ramp.body.position.y):
                            ramp_index_dragging = ramp_index
                            space.gravity = (0, 0)
                            ramp_dragging = True

                    for ramp in flipped_ramps:
                        mouse_x, mouse_y = event.pos
                        flipped_ramp_index += 1
                        print(ramp.body.position.x)
                        print((600-ramp.body.position.y))
                        if mouse_x <= ramp.body.position.x and mouse_x + 50 >= ramp.body.position.x and mouse_y <= (600 - ramp.body.position.y) and mouse_y + 50 >= (600-ramp.body.position.y):
                            flipped_ramp_index_dragging = flipped_ramp_index
                            space.gravity = (0, 0)
                            flipped_ramp_dragging = True

                    mouse_pos = mouse.get_pos()
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    if rect.collidepoint(mouse_pos):
                        if space.gravity == (0.0, 0):
                            space.gravity = (0.0, -980.0)  # sets the gravity of the space
                        else:
                            space.gravity = (0.0, 0)  # sets the gravity of the space
                    else:
                        if runonce is False and (object_draging is False) and (square_draging is False) and (ramp_dragging is False) and (flipped_ramp_dragging is False):
                            pos = pygame.mouse.get_pos()
                            final = str(pos)
                            x = final[final.find('(') + len('('):final.rfind(',')]
                            y = final[final.find(',') + len(','):final.rfind(')')]
                            add_circle(0.1, 25, x, y, 0.5, len(balls))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    object_draging = False
                    square_draging = False
                    ramp_dragging = False
                    flipped_ramp_dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if object_draging:
                    mouse_x, mouse_y = event.pos
                    offset_x = balls[index_dragging].body.position.x - mouse_x
                    offset_y = balls[index_dragging].body.position.y - mouse_y
                    balls[index_dragging].body.position.x = mouse_x + offset_x
                    balls[index_dragging].body.position.y = mouse_y + offset_y
                    space.remove(balls[index_dragging])
                    balls.remove(balls[index_dragging])
                    add_circle(0.1, 25, mouse_x, mouse_y, 0.5, index_dragging)

                if square_draging:
                    mouse_x, mouse_y = event.pos
                    offset_x = squares[square_index_dragging].body.position.x - mouse_x
                    offset_y = squares[square_index_dragging].body.position.y - mouse_y
                    squares[square_index_dragging].body.position.x = mouse_x + offset_x
                    squares[square_index_dragging].body.position.y = mouse_y + offset_y
                    space.remove(squares[square_index_dragging])
                    squares.remove(squares[square_index_dragging])
                    add_square(0.1, 50.0, 50.0, mouse_x, mouse_y, 0.5, square_index_dragging)

                if ramp_dragging:
                    mouse_x, mouse_y = event.pos
                    offset_x = ramps[ramp_index_dragging].body.position.x - mouse_x
                    offset_y = ramps[ramp_index_dragging].body.position.y - mouse_y
                    ramps[ramp_index_dragging].body.position.x = mouse_x + offset_x
                    ramps[ramp_index_dragging].body.position.y = mouse_y + offset_y
                    space.remove(ramps[ramp_index_dragging])
                    ramps.remove(ramps[ramp_index_dragging])
                    add_ramp(100, 45, mouse_x, mouse_y, 0.1, ramp_index_dragging)

                if flipped_ramp_dragging:
                    mouse_x, mouse_y = event.pos
                    offset_x = flipped_ramps[flipped_ramp_index_dragging].body.position.x - mouse_x
                    offset_y = flipped_ramps[flipped_ramp_index_dragging].body.position.y - mouse_y
                    flipped_ramps[flipped_ramp_index_dragging].body.position.x = mouse_x + offset_x
                    flipped_ramps[flipped_ramp_index_dragging].body.position.y = mouse_y + offset_y
                    space.remove(flipped_ramps[flipped_ramp_index_dragging])
                    flipped_ramps.remove(flipped_ramps[flipped_ramp_index_dragging])
                    add_ramp_flipped(100, 45, mouse_x, mouse_y, 0.1, flipped_ramp_index_dragging)


            # Interactive stuff ends here

            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "contact_with_friction.png")
            elif event.type == KEYDOWN and event.key == K_s:
                pos = pygame.mouse.get_pos()
                final = str(pos)
                x = final[final.find('(') + len('('):final.rfind(',')]
                y = final[final.find(',') + len(','):final.rfind(')')]
                add_ramp(100, 45, x, y, 0.1, len(ramps))
            elif event.type == KEYDOWN and event.key == K_d:
                pos = pygame.mouse.get_pos()
                final = str(pos)
                x = final[final.find('(') + len('('):final.rfind(',')]
                y = final[final.find(',') + len(','):final.rfind(')')]
                add_ramp_flipped(100, 45, x, y, 0.1, len(ramps))

            # global runonce


            # adds a square when the 'A' key is pressed; change around later for better UI
            if event.type == KEYDOWN and event.key == K_a:
                pos = pygame.mouse.get_pos()
                final = str(pos)
                x = final[final.find('(') + len('('):final.rfind(',')]
                y = final[final.find(',') + len(','):final.rfind(')')]
                add_square(0.1, 50.0, 50.0, x, y, 0.5, len(squares))

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
        background = (160, 194, 205,)
        screen.fill(background) #Dull blueish color

        ### Draw stuff
        space.debug_draw(draw_options)
        rect = Rect(450, 50, 100, 50)
        pygame.draw.rect(screen, THECOLORS["navy"], (450, 50, 100, 50))

        #Draws text onto the rectangle GO button
        def text_objects(text, font):
            textSurface = font.render(text, True, THECOLORS["white"])
            return textSurface, textSurface.get_rect()

        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = text_objects("GO!", smallText)
        textRect.center = ((450 + (100 / 2)), (50 + (50 / 2)))
        screen.blit(textSurf, textRect)

        ### Update physics
        dt = 1.0 / 60.0
        for x in range(1):
            space.step(dt)

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        #pygame.display.set_caption("fps: " + str(clock.get_fps()))
        pygame.display.set_caption("ATWOOD SIMULATION")


#adds a circle to the screen with changeabe mass, radius, x and y position, and friction coef
def add_circle(mass, radius, xpos, ypos, friction, index):
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass*5, inertia)
    body.position = int(xpos), (600 - int(ypos))
    shape = pymunk.Circle(body, radius, (0, 0))
    shape.color = pygame.color.THECOLORS["black"]
    shape.friction = friction
    space.add(body, shape)
    balls.insert(index, shape)


# adds a square to the screen with changeable mass, width, height, x and y positions, and friction coef
def add_square(mass, width, height, xpos, ypos, friction, index):
    inertia = pymunk.moment_for_box(mass, (width, height))
    body = pymunk.Body(mass*5, inertia)
    body.position = int(xpos), (600 - int(ypos))
    shape = pymunk.Poly.create_box(body, (width, height), 0)  # adding a radius (third param) bevels corners of poly
    shape.color = pygame.color.THECOLORS["black"]
    shape.friction = friction
    space.add(body, shape)

    squares.insert(index, shape)


# adds a right triangle to the screen with changeable mass, degree, x and y position, and friction coef
def add_ramp(mass, degree, xpos, ypos, friction, index):
    tan = math.tan((degree * (math.pi / 180)))
    height = 100 / tan  #height adjusts to make degree applicable
    inertia = pymunk.moment_for_poly(pymunk.inf, [(0, height), (100, 0), (0, 0)], (0, 0), 0)  # the length is always 100
    body = pymunk.Body(mass, inertia)
    body.position = int(xpos), (600 - int(ypos))
    shape = pymunk.Poly(body, [(0, height), (100, 0), (0, 0)])  # adding a radius (a third param) bevels corners of poly
    shape.color = pygame.color.THECOLORS["black"]
    shape.friction = friction
    space.add(body, shape)

    ramps.insert(index, shape)


# adds a right triangle to the screen with changeable mass, degree, x and y position, and friction coef
def add_ramp_flipped(mass, degree, xpos, ypos, friction, index):
    tan = math.tan((degree * (math.pi / 180)))
    height = 100 / tan  #height adjusts to make degree applicable
    inertia = pymunk.moment_for_poly(pymunk.inf, [(0, height), (-100, 0), (0, 0)], (0, 0), 0)  # the length is always 100
    body = pymunk.Body(mass, inertia)
    body.position = int(xpos), (600 - int(ypos))
    shape = pymunk.Poly(body, [(0, height), (-100, 0), (0, 0)])  # adding a radius (a third param) bevels corners of poly
    shape.color = pygame.color.THECOLORS["black"]
    shape.friction = friction
    space.add(body, shape)

    flipped_ramps.insert(index, shape)


if __name__ == '__main__':
    sys.exit(main())