
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
import numpy as np
from shader import create_shader_program, load_texture

vertices = np.array([
    -1.0, -1.0, 0.0,
    1.0, -1.0, 0.0,
    1.0, 1.0, 0.0,
    -1.0, 1.0, 0.0,
], dtype=np.float32)

indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

vertex_shader = ""
fragment_shader = ""

with open("vertex_shader.vsh", "r") as file:
    vertex_shader = file.read()

with open("fragment_shader.fsh", "r") as file:
    fragment_shader = file.read()

def start_shader():
    shader_program = create_shader_program(vertex_shader, fragment_shader)
    glUseProgram(shader_program)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

def main():
    pg.init()
    display = (800, 600)
    screen = pg.display.set_mode(display, DOUBLEBUF | OPENGL)

    start_shader()

    FPS = 60
    clock = pg.time.Clock()

    view_buffer = pg.surface.Surface(display)
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        view_buffer.fill((255, 255, 255))

        glClear(GL_COLOR_BUFFER_BIT)

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        screen.blit(view_buffer, (0, 0))
        pg.display.flip()
        clock.tick(FPS)

    pg.quit()

if __name__ == "__main__":
    main()
