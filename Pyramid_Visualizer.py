import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *  # more advanced openGl stuff


def draw_axes():
    # Draw Red X Axis
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)

    glVertex3f(-4.0, 0.0, 0.0)
    glVertex3f(4.0, 0.0, 0.0)

    # arrow
    glVertex3f(4.0, 0.0, 0.0)
    glVertex3f(3.0, 1.0, 0.0)
    glVertex3f(4.0, 0.0, 0.0)
    glVertex3f(3.0, -1.0,0.0)

    glEnd()
    glFlush()

    # Draw green Y Aiis
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, -4.0, 0)
    glVertex3f(0.0, 4.0, 0)

    # arrow
    glVertex3f(0.0, 4.0, 0.0)
    glVertex3f(1.0, 3.0, 0.0)
    glVertex3f(0.0, 4.0, 0)
    glVertex3f(-1.0, 3.0, 0 )
    glEnd()
    glFlush()

    # Draw Blue Z axis
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, -4.0)
    glVertex3f(0.0, 0.0, 4.0)

    # arrow
    glVertex3f(0.0, 0.0, 4.0)
    glVertex3f(0.0, 1.0, 3.0)
    glVertex3f(0.0, 0.0, 4.0)
    glVertex3f(0.0, -1.0, 3.0)
    glEnd()

class Pyramid_arm:  # define a class of object to use repeatably

    def __init__(self, origin, direction_name, cube_l, tip_l, color):  # this method gets called once (and only once) when object is created

        # Set up Pyramid object attributes using constructor parameters
        self.origin = origin  # initial position of pyramid
        self.direction_name = direction_name  # 3 element vector defining [x,y,z] scaling
        self.cube_l = cube_l
        self.tip_l = tip_l
        self.color = color  # 3 element vector defining [r,g,b] pyramid wall color

        # Make empty lists to hold vertices and surfaces of the pyramid
        self.vertices = []
        self.tri_surfaces = []
        self.flat_surface = []
        self.position = np.array(self.origin)  # converting the position to a numpy array using type casting

        self.set_vertices()  # call the set_vertices method to initialize the shape, might not need to call this here

    def set_vertices(self):
        """
        Establishes new vertices after any scaling and translation
        """

        if self.direction_name == "Right":

            base_poly = [
                    [.5, -.5, .5],
                    [.5, -.5, -.5],
                    [.5, .5, -.5],
                    [.5, .5, .5],
                    [1 + self.tip_l/self.cube_l, 0, 0]
                    ]
        if self.direction_name == "Left":
            base_poly = [
                [-.5, -.5, .5],
                [-.5, -.5, -.5],
                [-.5, .5, -.5],
                [-.5, .5, .5],
                [-1 - self.tip_l/self.cube_l, 0, 0]
            ]

        if self.direction_name == "Top":
            base_poly = [
                [.5, -.5, .5],
                [-.5, -.5, .5],
                [-.5, .5, .5],
                [.5, .5, .5],
                [0, 0, 1 + self.tip_l/self.cube_l]
            ]

        if self.direction_name == "Bottom":
            base_poly = [
                [.5, -.5, -.5],
                [-.5, -.5, -.5],
                [-.5, .5, -.5],
                [.5, .5, -.5],
                [0, 0, -1 - self.tip_l/self.cube_l]
            ]

        if self.direction_name == "Front":
            base_poly = [
                [.5, -.5, -.5],
                [-.5, -.5, -.5],
                [-.5, -.5, .5],
                [.5, -.5, .5],
                [0, -1 - self.tip_l/self.cube_l, 0]
            ]

        if self.direction_name == "Back":
            base_poly = [
                [.5, .5, -.5],
                [-.5, .5, -.5],
                [-.5, .5, .5],
                [.5, .5, .5],
                [0, 1 + self.tip_l/self.cube_l, 0]
            ]

        self.vertices = np.array(base_poly) * self.cube_l
        self.vertices = self.vertices + self.origin

        self.flat_surface = [0, 1, 2, 3]
        self.tri_surfaces = [
            [0, 1, 4],
            [1, 4, 2],
            [3, 2, 4],
            [0, 3, 4]
        ]

    def draw(self):
        """Actually draws the object, kinda janky?"""

        self.set_vertices()  # update to newest vertices

        glBegin(GL_QUADS)  # set drawing mode to filled triangles
        glColor3fv(self.color)  # set shader(idk if right term?) color to the object color

        for corners in self.flat_surface: # loop through each surface definition (the 3 vertex indices that make up that surface)
            glVertex3fv(self.vertices[corners])  # feed the (shader?) the next point
            # print(f"Corner value: %d : Coordinate %s" % (corners,self.vertices[corners]))
        glEnd()  # close up drawing session

        glBegin(GL_TRIANGLES)  # set drawing mode to filled triangles
        glColor3fv(self.color)  # set shader(idk if right term?) color to the object color

        for triangles in self.tri_surfaces:  # loop through each surface definition (the 3 vertex indices that make up that surface)
            for point in triangles:
                glVertex3fv(self.vertices[point])  # feed the (shader?) the next point
            # print(f"Corner value: %d : Coordinate %s" % (corners, self.vertices[corners]))
        glEnd()  # close up drawing session


class Pyramid:

    def __init__(self, origin, color, cube_length, tip_length):
        self.origin = origin
        self.color = color
        self.cube_length = cube_length
        self.tip_length = tip_length
        self.max_length = tip_length
        self.decay_time = 0

        p1 = Pyramid_arm(self.origin, "Right", self.cube_length, self.tip_length, self.color)
        p2 = Pyramid_arm(self.origin, "Left", self.cube_length, self.tip_length, self.color)
        p3 = Pyramid_arm(self.origin, "Top", self.cube_length, self.tip_length, self.color)
        p4 = Pyramid_arm(self.origin, "Bottom", self.cube_length, self.tip_length, self.color)
        p5 = Pyramid_arm(self.origin, "Front", self.cube_length, self.tip_length, self.color)
        p6 = Pyramid_arm(self.origin, "Back", self.cube_length, self.tip_length, self.color)

        self.arms = [p1, p2, p3, p4, p5, p6]

    def spike(self, max_val):
        self.max_length = max_val
        self.decay_time = 0

    def decay(self, rate):
        self.decay_time += 1
        self.tip_length = self.max_length*(1-rate)**self.decay_time

    def draw(self):
        for p in self.arms:
            p.tip_l = self.tip_length  # update to newest vals
            p.draw()

def main():
    pygame.init()  # initializes the window and stuff
    display = (1400, 800)  # display resolution
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # this makes your graphics swole and also use OpenGL

    # set up view parameters
    gluPerspective(60, (display[0]/display[1]), 0.01, 100.0)  # (fov in deg, aspect ratio, near clipping plane, far clipping plane)
    glTranslatef(0.0, 0, -5)  # move camera to 40 units above the Z plane (relative to prev position at origin)
    # glRotatef(180, 1, 0, 0)  # optional rotate initial camera view

    t1 = Pyramid([0, 0, 0], [204/255, 1, 203/255], .5, 2)
    t2 = Pyramid([4, 0, 2], [118/255, 213/255, 237/255], 2, 1)
    t3 = Pyramid([-1, 0, -2], [56/255, 2/255, 59/255], 1, 3)
    a = 1

    t1.spike(3)
    t2.spike(3)
    t3.spike(3)


    while True:  # infinite loop
        for event in pygame.event.get():
            # this prevents it from running forever, otherwise close button doesn't work
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # keypress handling done by pyGame
            if event.type == pygame.KEYDOWN:

                # handy keyboard quit option, press q
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

                # camera rotation with arrow keys, mostly works
                if event.key == pygame.K_DOWN:
                    glRotatef(15, .5, 0.0, 0)
                if event.key == pygame.K_UP:
                    glRotatef(15, -.5, 0.0, 0)
                if event.key == pygame.K_LEFT:
                    glRotatef(15, 0, 0.0, .5)
                if event.key == pygame.K_RIGHT:
                    glRotatef(15, 0, 0.0, -.5)

            # zoom functionality using mousewheel, only sort of works. todo: make this better
            if event.type == pygame.MOUSEBUTTONDOWN:  # mousewheel event handling
                if event.button == 4:  # zoom in
                    glTranslatef(0, 0, 1)
                if event.button == 5:  # zoom out
                    glTranslatef(0, 0, -1)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  # clears the frame and some specific params

        draw_axes()
        t1.decay(.05)
        t2.decay(.05)
        t3.decay(.05)
        t1.draw()
        t2.draw()
        t3.draw()

        if a%15 == 0:
            t1.spike(2)
            t2.spike(1)
            t3.spike(3)

        a += 1
        pygame.display.flip()  # actually update the screen to show stuff
        pygame.time.wait(20)  #wait 10 ms to loop



main()  # run the main function
