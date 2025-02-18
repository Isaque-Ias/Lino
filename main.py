import pygame
from OpenGL.GL import *
import numpy as np
import glm
import time
from shader import compile_shader, create_shader_program, create_square, load_texture

VERTEX_SHADER = ""
FRAGMENT_SHADER = ""
with open("vertex_shader.vsh", "r") as file:
    VERTEX_SHADER = file.read()
with open("fragment_shader.fsh", "r") as file:
    FRAGMENT_SHADER = file.read()


def main():
    pygame.init()
    pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

    shader_program = create_shader_program(VERTEX_SHADER, FRAGMENT_SHADER)
    square_VAO = create_square()
    
    texture1 = load_texture("car.jpg")
    texture2 = load_texture("car2.webp")

    glUseProgram(shader_program)

    transform_loc = glGetUniformLocation(shader_program, "transform")
    texture_loc = glGetUniformLocation(shader_program, "ourTexture")

    running = True
    start_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT)

        elapsed_time = time.time() - start_time

        transform1 = glm.translate(glm.mat4(1.0), glm.vec3(-0.6, 0.0, 0.0))
        transform1 = glm.rotate(transform1, elapsed_time, glm.vec3(0.0, 0.0, 1.0))

        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, glm.value_ptr(transform1))
        glUniform1i(texture_loc, 0)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture1)

        glBindVertexArray(square_VAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        #transforms
        transform2 = glm.translate(glm.mat4(1.0), glm.vec3(0.6, 0.0, 0.0))
        transform2 = glm.rotate(transform2, 0.2, glm.vec3(0.0, 0.0, 1.0))

        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, glm.value_ptr(transform2))
        glUniform1i(texture_loc, 0)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture2)

        glBindVertexArray(square_VAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
