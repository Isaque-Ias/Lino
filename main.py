import pygame as pg
from OpenGL.GL import *
import glm
from shader import *

pg.init()

VERTEX_SHADER = load_shader("vertex_shader.vsh")
FRAGMENT_SHADER = load_shader("fragment_shader.fsh")

def map(x, y, z, w, t):
    return (t - x) * (w - z) / (y - x) + z

class UIHandler:
    window_size = (1200, 675)
    mouse_x = 0
    mouse_y = 0
    click_x = 0
    click_y = 0
    mouse_pressed = True

    game_window_size = [400, 400]
    game_window_size_click = [0, 0]
    game_window_size_min = [300, 300]
    game_window_size_max = [600, 600]
    
    element_window_width = 200
    element_window_width_click = 0
    element_window_width_min = 200
    element_window_width_max = 400

    elements_list_height = 2000
    elements_bar_percent = 0.9
    elements_bar_percent_click = 0

    padding = 15

    bar_width = 20
    bar_padding = 5

    mouse_at = ""
    fix_mouse_at = False

    category_color = {
        "movimento": [0.496, 0.351, 1.0, 1.0],
        "controle": [0.921, 0.356, 0.337, 1.0],
        "sensacao": [1.0, 0.69, 0.117, 1.0],
        "booleanos": [0.556, 0.984, 0.235, 1.0],
        "variaveis": [1.0, 0.352, 0.937, 1.0],
    }
    category_height = 50
    current_category = category_color["movimento"]

    elements_bar_height = window_size[1] - padding * 2 - bar_padding * 2 - category_height
    elements_view_spam = window_size[1] - padding * 2 - category_height
    elements_bar_hold_height = elements_bar_height * elements_view_spam / elements_list_height

    roboto_72 = pg.font.Font("Roboto.ttf", 72)

    def handle():
        global mouse_x
        global mouse_y
        global click_x
        global click_y
        global mouse_pressed

        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_hold = pg.mouse.get_pressed()

        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        if mouse_hold[0]:
            if mouse_pressed:
                click_x = mouse_x
                click_y = mouse_y
                mouse_pressed = False

                if not UIHandler.mouse_at == "":
                    UIHandler.game_window_size_click = [UIHandler.game_window_size[0], UIHandler.game_window_size[1]]
                    UIHandler.element_window_width_click = UIHandler.element_window_width
                    UIHandler.elements_bar_percent_click = UIHandler.elements_bar_percent * (UIHandler.elements_bar_height - UIHandler.elements_bar_hold_height) + UIHandler.padding + UIHandler.bar_padding + UIHandler.elements_bar_hold_height / 2
                UIHandler.fix_mouse_at = True

            if not UIHandler.mouse_at == "":
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            if UIHandler.mouse_at == "game_window_size_side":
                UIHandler.game_window_size[0] = min(UIHandler.game_window_size_max[0], max(UIHandler.game_window_size_min[0], click_x - mouse_x + UIHandler.game_window_size_click[0]))
            elif UIHandler.mouse_at == "game_window_size_full":
                UIHandler.game_window_size[0] = min(UIHandler.game_window_size_max[0], max(UIHandler.game_window_size_min[0], click_x - mouse_x + UIHandler.game_window_size_click[0]))
                UIHandler.game_window_size[1] = min(UIHandler.game_window_size_max[1], max(UIHandler.game_window_size_min[1], mouse_y + UIHandler.game_window_size_click[1] - click_y))
            elif UIHandler.mouse_at == "game_window_size_down":
                UIHandler.game_window_size[1] = min(UIHandler.game_window_size_max[1], max(UIHandler.game_window_size_min[1], mouse_y + UIHandler.game_window_size_click[1] - click_y))
            elif UIHandler.mouse_at == "element_window_width":
                UIHandler.element_window_width = min(UIHandler.element_window_width_max, max(UIHandler.element_window_width_min, mouse_x + UIHandler.element_window_width_click - click_x))
            elif UIHandler.mouse_at == "element_bar":
                UIHandler.elements_bar_percent = max(0, min(1, (mouse_y + (UIHandler.elements_bar_percent_click - click_y) - UIHandler.padding - UIHandler.bar_padding - UIHandler.elements_bar_hold_height / 2) / (UIHandler.elements_bar_height - UIHandler.elements_bar_hold_height)))
        else:
            mouse_pressed = True
            UIHandler.fix_mouse_at = False

        if not UIHandler.fix_mouse_at:
            UIHandler.mouse_at = ""

        
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

        if mouse_box(UIHandler.padding + UIHandler.element_window_width - UIHandler.bar_width + UIHandler.bar_padding,
                     UIHandler.padding + UIHandler.bar_padding,
                     UIHandler.padding + UIHandler.element_window_width - UIHandler.bar_padding,
                     UIHandler.window_size[1] - UIHandler.padding - UIHandler.category_height - UIHandler.bar_padding):
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            if not UIHandler.fix_mouse_at:
                UIHandler.mouse_at = "element_bar"

class Text:
    def __init__(self, text, font, color, pos, scale, proportions = (0.5, 0.5)):
        text_texture = load_text(text, font, color)
        self.text = text_texture[0]
        
        self.text_size = [scale[0] * text_texture[1][0], scale[1] * text_texture[1][1]]

        self.pos = [map(0, UIHandler.window_size[0], -1, 1, pos[0] + self.text_size[0] * proportions[0]), map(UIHandler.window_size[1], 0, -1, 1, pos[1] + self.text_size[1] * proportions[1])]
        self.scale = [scale[0] * text_texture[1][0] / UIHandler.window_size[0], scale[1] * text_texture[1][1] / UIHandler.window_size[1]]

def mouse_box(x1, y1, x2, y2):
    if mouse_x >= x1 and mouse_x <= x2 and mouse_y >= y1 and mouse_y <= y2:
        return True
    return False

def main():
    pg.display.set_mode(UIHandler.window_size, pg.OPENGL | pg.DOUBLEBUF)
    pg.display.set_caption("Lino")

    shader_program = create_shader_program(VERTEX_SHADER, FRAGMENT_SHADER)
    square_VAO = create_square()
    
    texture1 = load_texture("pixel.png")
    texture2 = load_texture("car.png")
    texture3 = load_texture("car.jpg")

    UIHandler.texts = [
        Text("208", UIHandler.roboto_72, (255, 255, 255), [0, 0], [0.25, 0.25]),
    ]

    glUseProgram(shader_program)

    transform_loc = glGetUniformLocation(shader_program, "transform")
    texture_loc = glGetUniformLocation(shader_program, "ourTexture")
    window_size_loc = glGetUniformLocation(shader_program, "windowSize")
    game_window_size_loc = glGetUniformLocation(shader_program, "gameWindowSize")
    padding_loc = glGetUniformLocation(shader_program, "padding")
    bar_width_loc = glGetUniformLocation(shader_program, "barWidth")
    bar_padding_loc = glGetUniformLocation(shader_program, "barPadding")
    element_window_width_loc = glGetUniformLocation(shader_program, "elementWindowWidth")
    current_category_loc = glGetUniformLocation(shader_program, "currentCategory")
    elements_list_height_loc = glGetUniformLocation(shader_program, "elementsListHeight")
    elements_bar_percent_loc = glGetUniformLocation(shader_program, "elementsBarPercent")
    category_height_loc = glGetUniformLocation(shader_program, "categoryHeight")
    is_text_loc = glGetUniformLocation(shader_program, "isText")

    running = True

    background_transform = glm.mat4(1.0)
    background_transform = glm.scale(background_transform, glm.vec3(1.0, 1.0, 1.0))

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        UIHandler.handle()
        # game_screen_center = [2 * (UIHandler.window_size[0] - UIHandler.padding - UIHandler.game_window_size[0] / 2) / UIHandler.window_size[0] - 1, 2 * (UIHandler.padding + UIHandler.game_window_size[1] / 2) / UIHandler.window_size[1] - 1]

        glClear(GL_COLOR_BUFFER_BIT)

        #global uniforms
        glUniform2f(window_size_loc, UIHandler.window_size[0], UIHandler.window_size[1])
        glUniform2f(game_window_size_loc, UIHandler.game_window_size[0], UIHandler.game_window_size[1])
        glUniform1f(padding_loc, UIHandler.padding)
        glUniform1f(bar_padding_loc, UIHandler.bar_padding)
        glUniform1f(bar_width_loc, UIHandler.bar_width)
        glUniform1f(element_window_width_loc, UIHandler.element_window_width)
        glUniform4f(current_category_loc, UIHandler.current_category[0], UIHandler.current_category[1], UIHandler.current_category[2], UIHandler.current_category[3])
        glUniform1f(elements_list_height_loc, UIHandler.elements_list_height)
        glUniform1f(elements_bar_percent_loc, UIHandler.elements_bar_percent)
        glUniform1f(category_height_loc, UIHandler.category_height)

        #layout image
        glUniform1i(is_text_loc, 0)
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, glm.value_ptr(background_transform))
        glUniform1i(texture_loc, 0)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture1[0])

        glBindVertexArray(square_VAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        #ui text
        for text in UIHandler.texts:
            glUniform1i(is_text_loc, 1)

            text_transform = glm.mat4(1.0)
            text_transform = glm.translate(text_transform, glm.vec3(text.pos[0], text.pos[1], 0.0))
            text_transform = glm.scale(text_transform, glm.vec3(text.scale[0], text.scale[1], 1.0))
            glUniformMatrix4fv(transform_loc, 1, GL_FALSE, glm.value_ptr(text_transform))
            glUniform1i(texture_loc, 0)

            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, text.text)

            glBindVertexArray(square_VAO)
            glDrawArrays(GL_TRIANGLES, 0, 6)


        pg.display.flip()
        pg.time.wait(10)

    pg.quit()

if __name__ == "__main__":
    main()
