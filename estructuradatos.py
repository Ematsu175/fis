from tokenize import String

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import time


class Circle:
    def __init__(self, x, y, radius=0.05, color=(1.0, 0.0, 0.0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self):
        glColor3f(*self.color)
        glPushMatrix()
        glTranslatef(self.x, self.y, 0.0)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0)
        for i in range(50 + 1):
            angle = 2 * math.pi * i / 50
            x = self.radius * math.cos(angle)
            y = self.radius * math.sin(angle)
            glVertex2f(x, y)
        glEnd()
        glPopMatrix()


def init():
    pygame.init()
    display = (1087, 361)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_TEXTURE_2D)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)


def draw_text(text, x_pos, y_pos):
    font = pygame.font.SysFont('monospace', 18)
    text_surface = font.render(text, True, (255, 255, 255), (0, 0, 0))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)

    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x_pos, y_pos)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glPopMatrix()


def load_texture(image_path):
    texture_surface = pygame.image.load(image_path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", True)
    width, height = texture_surface.get_size()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    return texture


def draw_background(texture):
    glColor3f(1.0, 1.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(-1, -1)
    glTexCoord2f(1, 0)
    glVertex2f(1, -1)
    glTexCoord2f(1, 1)
    glVertex2f(1, 1)
    glTexCoord2f(0, 1)
    glVertex2f(-1, 1)
    glEnd()


def main():
    global display  # Necesario para la función draw_text
    init()
    display = (1087, 361)
    textura = load_texture("C:\\Users\\emyva\\OneDrive\\Escritorio\\10mo semestre\\FIS\\mapa1.png")

    coordinates = [
        (-0.9, 0.0),
        (-0.8, 0.5),
        (-0.07, 0.4),
        (0.7, 0.1),
        (0.9, -0.2),
    ]

    circles = [Circle(x, y) for x, y in coordinates]

    current_index = 0
    last_change_time = time.time()
    state = 'waiting'

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        draw_background(textura)

        current_time = time.time()

        lugares_disponibles=40
        lugares_ocupados=0

        if state == 'waiting' and current_time - last_change_time >= 10:
            circles[current_index].color = (0.0, 1.0, 0.0)
            last_change_time = current_time
            state = 'green'
        elif state == 'green' and current_time - last_change_time >= 5:
            circles[current_index].color = (1.0, 0.0, 0.0)
            last_change_time = current_time
            current_index =(current_index + 1) % len(circles)
            state = 'waiting'

        for circle in circles:
            circle.draw()

        draw_text("Lugares Disponibles: "+str(lugares_disponibles),-0.9,-0.7)  # Dibuja el texto en el centro
        draw_text("Lugares Ocupados: " + str(lugares_ocupados), -0.9, -0.9)

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()


if __name__ == "__main__":
    main()