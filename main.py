import pygame as pg
from OpenGL.GL import *
import numpy as np
import glm
import time
from shader import create_shader_program, create_square, load_texture, load_shader

VERTEX_SHADER = load_shader("vertex_shader.vsh")
FRAGMENT_SHADER = load_shader("fragment_shader.fsh")

class UIHandler:
    window_size = (1200, 675)
    mouse_x = 0
    mouse_y = 0
    click_x = 0
    click_y = 0
    mouse_pressed = True

    game_window_size = [300, 300]
    game_window_size_click = [0, 0]
    game_window_size_min = [300, 300]
    game_window_size_max = [600, 600]
    
    element_window_width = 200
    element_window_width_click = 0
    element_window_width_min = 200
    element_window_width_max = 400

    padding = 15

    mouse_at = ""
    fix_mouse_at = False

    def handle():
        global mouse_x
        global mouse_y
        global click_x
        global click_y
        global mouse_pressed

        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_hold = pg.mouse.get_pressed()

        if mouse_hold[0]:
            if mouse_pressed:
                click_x = mouse_x
                click_y = mouse_y
                mouse_pressed = False

                if not UIHandler.mouse_at == "":
                    UIHandler.game_window_size_click = [UIHandler.game_window_size[0], UIHandler.game_window_size[1]]
                    UIHandler.element_window_width_click = UIHandler.element_window_width
                UIHandler.fix_mouse_at = True

            if UIHandler.mouse_at == "game_window_size_side":
                UIHandler.game_window_size[0] = min(UIHandler.game_window_size_max[0], max(UIHandler.game_window_size_min[0], click_x - mouse_x + UIHandler.game_window_size_click[0]))
            elif UIHandler.mouse_at == "game_window_size_full":
                UIHandler.game_window_size[0] = min(UIHandler.game_window_size_max[0], max(UIHandler.game_window_size_min[0], click_x - mouse_x + UIHandler.game_window_size_click[0]))
                UIHandler.game_window_size[1] = min(UIHandler.game_window_size_max[1], max(UIHandler.game_window_size_min[1], mouse_y + UIHandler.game_window_size_click[1] - click_y))
            elif UIHandler.mouse_at == "game_window_size_down":
                UIHandler.game_window_size[1] = min(UIHandler.game_window_size_max[1], max(UIHandler.game_window_size_min[1], mouse_y + UIHandler.game_window_size_click[1] - click_y))
            elif UIHandler.mouse_at == "element_window_width":
                UIHandler.element_window_width = min(UIHandler.element_window_width_max, max(UIHandler.element_window_width_min, mouse_x + UIHandler.element_window_width_click - click_x))
        else:
            mouse_pressed = True
            UIHandler.fix_mouse_at = False

        if not UIHandler.fix_mouse_at:
            UIHandler.mouse_at = ""

        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        
        if mouse_box(UIHandler.window_size[0] - UIHandler.padding * 2 - UIHandler.game_window_size[0],
                     UIHandler.padding,
                     UIHandler.window_size[0] - UIHandler.padding - UIHandler.game_window_size[0],
                     UIHandler.padding + UIHandler.game_window_size[1]):
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            if not UIHandler.fix_mouse_at:
                UIHandler.mouse_at = "game_window_size_side"
            
        if mouse_box(UIHandler.window_size[0] - UIHandler.padding * 2 - UIHandler.game_window_size[0],
                     UIHandler.padding * 2 + UIHandler.game_window_size[1],
                     UIHandler.window_size[0] - UIHandler.padding - UIHandler.game_window_size[0],
                     UIHandler.window_size[1] - UIHandler.padding):
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            if not UIHandler.fix_mouse_at:
                UIHandler.mouse_at = "game_window_size_side"

        if mouse_box(UIHandler.window_size[0] - UIHandler.padding * 2 - UIHandler.game_window_size[0],
                     UIHandler.padding + UIHandler.game_window_size[1],
                     UIHandler.window_size[0] - UIHandler.padding - UIHandler.game_window_size[0],
                     UIHandler.padding * 2 + UIHandler.game_window_size[1]):
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            if not UIHandler.fix_mouse_at:
                UIHandler.mouse_at = "game_window_size_full"

        if mouse_box(UIHandler.window_size[0] - UIHandler.padding - UIHandler.game_window_size[0],
                     UIHandler.padding + UIHandler.game_window_size[1],
                     UIHandler.window_size[0] - UIHandler.padding,
                     UIHandler.padding * 2 + UIHandler.game_window_size[1]):
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            if not UIHandler.fix_mouse_at:
                UIHandler.mouse_at = "game_window_size_down"

        if mouse_box(UIHandler.padding + UIHandler.element_window_width,
                     UIHandler.padding,
                     UIHandler.padding * 2 + UIHandler.element_window_width,
                     UIHandler.window_size[1] - UIHandler.padding):
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            if not UIHandler.fix_mouse_at:
                UIHandler.mouse_at = "element_window_width"

def mouse_box(x1, y1, x2, y2):
    if mouse_x >= x1 and mouse_x <= x2 and mouse_y >= y1 and mouse_y <= y2:
        return True
    return False

def main():
    pg.init()
    pg.display.set_mode(UIHandler.window_size, pg.OPENGL | pg.DOUBLEBUF)

    shader_program = create_shader_program(VERTEX_SHADER, FRAGMENT_SHADER)
    square_VAO = create_square()
    
    texture1 = load_texture("pixel.png")
    texture2 = load_texture("car.png")
    texture3 = load_texture("car.jpg")

    glUseProgram(shader_program)

    transform_loc = glGetUniformLocation(shader_program, "transform")
    texture_loc = glGetUniformLocation(shader_program, "ourTexture")
    window_size_loc = glGetUniformLocation(shader_program, "windowSize")
    game_window_size_loc = glGetUniformLocation(shader_program, "gameWindowSize")
    padding_loc = glGetUniformLocation(shader_program, "padding")
    element_window_width_loc = glGetUniformLocation(shader_program, "elementWindowWidth")

    running = True
    start_time = time.time()

    window_ratio = UIHandler.window_size[0] / UIHandler.window_size[1]

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        UIHandler.handle()
        game_screen_center = [2 * (UIHandler.window_size[0] - UIHandler.padding - UIHandler.game_window_size[0] / 2) / UIHandler.window_size[0] - 1, 2 * (UIHandler.padding + UIHandler.game_window_size[1] / 2) / UIHandler.window_size[1] - 1]

        glClear(GL_COLOR_BUFFER_BIT)

        #transforms
        elapsed_time = time.time() - start_time
        
        transform1 = glm.mat4(1.0)
        # transform1 = glm.translate(transform1, glm.vec3(game_screen_center[0], game_screen_center[1], 0.0))
        transform1 = glm.scale(transform1, glm.vec3(1.0, 1.0, 1.0))
        # transform1 = glm.rotate(transform1, elapsed_time, glm.vec3(0.0, 0.0, 1.0))

        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, glm.value_ptr(transform1))
        glUniform1i(texture_loc, 0)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture1)

        glBindVertexArray(square_VAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        transform2 = glm.mat4(1.0)
        transform2 = glm.translate(transform2, glm.vec3(game_screen_center[0], -game_screen_center[1], 0.0))
        transform2 = glm.scale(transform2, glm.vec3(UIHandler.game_window_size[0] / 2000, window_ratio * UIHandler.game_window_size[1] / 2000, 1.0))
        # transform2 = glm.rotate(transform2, 0.2, glm.vec3(0.0, 0.0, 1.0))

        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, glm.value_ptr(transform2))
        glUniform1i(texture_loc, 0)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture3 if pg.mouse.get_pressed()[0] else texture2)

        #uniforms
        glUniform2f(window_size_loc, UIHandler.window_size[0], UIHandler.window_size[1])
        glUniform2f(game_window_size_loc, UIHandler.game_window_size[0], UIHandler.game_window_size[1])
        glUniform1f(padding_loc, UIHandler.padding)
        glUniform1f(element_window_width_loc, UIHandler.element_window_width)

        glBindVertexArray(square_VAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        pg.display.flip()
        pg.time.wait(10)

    pg.quit()

if __name__ == "__main__":
    main()
