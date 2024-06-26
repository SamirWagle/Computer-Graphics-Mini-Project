import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Constants
GRAVITY = 9.81
BOUNCE_DAMPING = 0.7
BALL_RADIUS = 0.1
GROUND_LEVEL = -1

class Ball:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0])
        self.velocity = np.array([0.0, 2.0, 0.0])

    def update(self, dt):
        # Update position
        self.position += self.velocity * dt
        # Apply gravity
        self.velocity[1] -= GRAVITY * dt

        # Check for collision with the ground
        if self.position[1] - BALL_RADIUS < GROUND_LEVEL:
            self.position[1] = GROUND_LEVEL + BALL_RADIUS
            self.velocity[1] = -self.velocity[1] * BOUNCE_DAMPING

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        quadric = gluNewQuadric()
        gluSphere(quadric, BALL_RADIUS, 32, 32)
        glPopMatrix()

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)

def display(ball):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # Draw the ground
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)
    glVertex3f(-2.0, GROUND_LEVEL, -2.0)
    glVertex3f(2.0, GROUND_LEVEL, -2.0)
    glVertex3f(2.0, GROUND_LEVEL, 2.0)
    glVertex3f(-2.0, GROUND_LEVEL, 2.0)
    glEnd()

    # Draw the ball
    ball.draw()

    pygame.display.flip()

def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Bouncing Ball Simulation')
    clock = pygame.time.Clock()

    init()

    ball = Ball()
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        ball.update(dt)
        display(ball)

    pygame.quit()

if __name__ == "__main__":
    main()
