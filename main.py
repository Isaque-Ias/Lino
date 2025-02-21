import pygame as pg
from pygame.locals import K_RETURN
from OpenGL.GL import *
import glm
from shader import *
import json
import copy

#add other bar
#fix bar hitbox move
#add visualizer for blocks
#make the block act algorithm
#make better areas structure
#build 2d world at least
#display only displays
#most versatile display -> topleft, color, structure_type, vec2 codeBlockSizes, isElse;
#is text:0 -> None, 1 -> whole, 2 = game, 3 = elements, 4 = codespace 5 = scenarios

pg.init()

VERTEX_SHADER = load_shader("vertex_shader.vsh")
FRAGMENT_SHADER = load_shader("fragment_shader.fsh")

with open("default_block_structure.json", "r") as file:
    DEFAULT_BLOCK_STRUCTURE = json.load(file)

with open("menu_interface.json", "r") as file:
    MENU_INTERFACE = json.load(file)

scene = "menu"

class UIHandler:
    fonts = {
        "roboto_72": pg.font.Font("Roboto.ttf", 72)
    }

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
    elements_bar_percent = 0.1
    elements_bar_percent_click = 0

    menu_outer_offset = 10
    menu_outer_width = 10
    menu_outer_radius = 50
    menu_background_alpha = 1

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
    category_height = 30
    current_category = category_color["movimento"]

    elements_bar_height = window_size[1] - padding * 2 - bar_padding * 2 - category_height
    elements_view_spam = window_size[1] - padding * 2 - category_height

    elements_bar_hold_height = elements_bar_height * elements_view_spam / elements_list_height

    def recalc_hold_height():
        UIHandler.elements_bar_hold_height = UIHandler.elements_bar_height * UIHandler.elements_view_spam / UIHandler.elements_list_height

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

class Menu:
    menu_outer_offset = 10
    menu_outer_width = 5
    menu_outer_radius = 50
    menu_background_alpha = 1

    def handle():
        Menu.menu_background_alpha = max(0, Menu.menu_background_alpha - 0.01)

class Area:
    def __init__(self, area_type, information):
        self.parent = information["parent"]
        self.area_type = area_type
        
        if area_type == "text":
            self.text = information["text"]
            self.font = UIHandler.fonts[information["font"]]
            self.color = information["color"]
            self.raw_pos = information["pos"]
            self.raw_scale = information["scale"]

            self.texture = load_text(self.text, self.font, self.color)

            self.scale = [self.raw_scale[0] * self.texture.width / UIHandler.window_size[0], self.raw_scale[1] * self.texture.height / UIHandler.window_size[1]]
            
            self.position_offset = information["position_offset"] if information.get("position_offset") else (0, 0)
            
            self.size = [self.raw_scale[0] * self.texture.width, self.raw_scale[1] * self.texture.height]

            screen_pos = [self.parent.x + self.raw_pos[0] + self.size[0] * self.position_offset[0], (UIHandler.window_size[1] - self.parent.y) - self.raw_pos[1] + self.size[1] * self.position_offset[1]]
            self.pos = [map(0, UIHandler.window_size[0], -1, 1, screen_pos[0]), map(UIHandler.window_size[1], 0, -1, 1, screen_pos[1])]

        elif area_type == "sensing":
            self.space = information["space"]
            self.bound_scale = information["bound_scale"] if not information.get("bound_scale") == None else False

            self.text = information["text"]
            self.font = UIHandler.fonts[information["font"]]
            self.color = information["color"]
            self.raw_pos = information["pos"]
            self.raw_scale = information["scale"]

            texture_bound = [self.bound_scale[0] / self.raw_scale[0], self.bound_scale[1] / self.raw_scale[1]] if self.bound_scale else False

            self.texture = load_sensing(self.text, self.font, self.color, texture_bound)

            if not self.bound_scale:
                self.bound_scale = [self.texture.width * self.raw_scale[0], self.texture.height * self.raw_scale[1]]

            self.scale = [self.raw_scale[0] * self.texture.width / UIHandler.window_size[0], self.raw_scale[1] * self.texture.height / UIHandler.window_size[1]]
            
            self.position_offset = information["position_offset"] if information.get("position_offset") else [0, 0]
            
            self.size = [self.bound_scale[0], self.bound_scale[1]]
            screen_pos = [self.parent.x + self.raw_pos[0] + self.size[0] / 2, (UIHandler.window_size[1] - self.parent.y) - self.raw_pos[1]]
            self.pos = [map(0, UIHandler.window_size[0], -1, 1, screen_pos[0]), map(UIHandler.window_size[1], 0, -1, 1, screen_pos[1])]

    def change_text(self, text):
        self.text = text

        self.texture = load_text(self.text, self.font, self.color)

        self.scale = [self.raw_scale[0] * self.texture.width / UIHandler.window_size[0], self.raw_scale[1] * self.texture.height / UIHandler.window_size[1]]

        self.size = [self.raw_scale[0] * self.texture.width, self.raw_scale[1] * self.texture.height]

        screen_pos = [self.parent.x + self.raw_pos[0] + self.size[0] * self.position_offset[0], (UIHandler.window_size[1] - self.parent.y) - self.raw_pos[1] + self.size[1] * self.position_offset[1]]
        self.pos = [map(0, UIHandler.window_size[0], -1, 1, screen_pos[0]), map(UIHandler.window_size[1], 0, -1, 1, screen_pos[1])]

class Block:
    def __init__(self, block_type, pos, content=False):
        padding = 5
        self.x = pos[0]
        self.y = pos[1]
        self.sequence = []
        category_color_key = DEFAULT_BLOCK_STRUCTURE[block_type]["color"]

        self.color = UIHandler.category_color[category_color_key]
        self.width = DEFAULT_BLOCK_STRUCTURE[block_type]["width"]
        self.height = DEFAULT_BLOCK_STRUCTURE[block_type]["height"]
        self.block_format = DEFAULT_BLOCK_STRUCTURE[block_type]["block_format"]
        if content:
            self.sequence = content
        else:
            carry_over = 0
            for sequence_area in enumerate(DEFAULT_BLOCK_STRUCTURE[block_type]["sequence"]):
                information = copy.deepcopy(sequence_area[1]["information"])
                information["parent"] = self
                
                information["pos"] = [information["pos"][0] + carry_over + padding, information["pos"][1] + padding]

                sequence_value = Area(sequence_area[1]["type"], information)
                self.sequence.append(sequence_value)
                
                carry_over += self.sequence[sequence_area[0]].size[0] + padding
            self.width = carry_over + self.x + padding * 2
        
        
class Element:
    #only for selection
    blocks = []

class Workspace:
    #only for selection
    blocks = [
        # Block("move_forward", (20, 20)),
    ]

def draw(square, uniforms, textures, texture, texture_transform=False):
    if not texture_transform:
        texture_transform = glm.mat4(1.0)

    glUniformMatrix4fv(uniforms["transform_loc"], 1, GL_FALSE, glm.value_ptr(texture_transform))
    
    glUniform1i(uniforms["texture_loc"], 0)

    glActiveTexture(GL_TEXTURE0)
    if isinstance(texture, str):
        glBindTexture(GL_TEXTURE_2D, textures[texture].texture)
    else:
        glBindTexture(GL_TEXTURE_2D, texture)

    glBindVertexArray(square)
    glDrawArrays(GL_TRIANGLES, 0, 6)

def game(square, uniforms, textures):
    for element in Element.blocks:
        glUniform1i(uniforms["display_area_loc"], 3)
        glUniform1i(uniforms["is_text_loc"], 0)

        glUniform2f(uniforms["block_pos_loc"], element.x, element.y)
        glUniform2f(uniforms["block_size_loc"], element.width, element.height)
        glUniform4f(uniforms["block_color_loc"], element.color[0], element.color[1], element.color[2], element.color[3])
        glUniform1i(uniforms["block_format_loc"], element.block_format)
        
        draw(square, uniforms, textures, "background_texture")

        for part in element.sequence:
            glUniform1i(uniforms["display_area_loc"], 3)

            if part.area_type == "text":
                glUniform1i(uniforms["is_text_loc"], 1)

                texture_transform = glm.mat4(1.0)
                texture_transform = glm.translate(texture_transform, glm.vec3(part.pos[0], part.pos[1], 0.0))
                texture_transform = glm.scale(texture_transform, glm.vec3(part.scale[0], part.scale[1], 1.0))
                
            elif part.area_type == "sensing":
                glUniform1i(uniforms["is_text_loc"], 2)
                glUniform2f(uniforms["block_pos_loc"], part.raw_pos[0] + element.x, part.raw_pos[1] + element.y)
                glUniform2f(uniforms["block_size_loc"], part.bound_scale[0], part.bound_scale[1])

                texture_transform = glm.mat4(1.0)
                texture_transform = glm.translate(texture_transform, glm.vec3(part.pos[0], part.pos[1], 0.0))
                texture_transform = glm.scale(texture_transform, glm.vec3(part.scale[0], part.scale[1], 1.0))

            draw(square, uniforms, textures, part.texture.texture, texture_transform)

def menu(square, uniforms, textures):
    global scene
    if pg.key.get_pressed()[K_RETURN]:
        scene = "game"

    glUniform1f(uniforms["menu_outer_offset_loc"], Menu.menu_outer_offset)
    glUniform1f(uniforms["menu_outer_width_loc"], Menu.menu_outer_width)
    glUniform1f(uniforms["menu_outer_radius_loc"], Menu.menu_outer_radius)
    glUniform1f(uniforms["menu_background_alpha_loc"], Menu.menu_background_alpha)
    glUniform1i(uniforms["is_text_loc"], 0)
    
    Menu.handle()

    glUniform1i(uniforms["scene_loc"], 0)

    draw(square, uniforms, textures, "menu_background")

    glUniform1i(uniforms["is_text_loc"], 1)

    texture_transform = glm.mat4(1.0)
    texture_transform = glm.translate(texture_transform, glm.vec3(0.0, 0.0, 0.0))
    texture_transform = glm.scale(texture_transform, glm.vec3(textures["enter"].width / UIHandler.window_size[0], textures["enter"].height / UIHandler.window_size[1], 1.0))

    draw(square, uniforms, textures, "enter", texture_transform)


def mouse_box(x1, y1, x2, y2):
    if mouse_x >= x1 and mouse_x <= x2 and mouse_y >= y1 and mouse_y <= y2:
        return True
    return False

def map(x, y, z, w, t):
    return (t - x) * (w - z) / (y - x) + z


def main():
    global scene
    pg.display.set_mode(UIHandler.window_size, pg.OPENGL | pg.DOUBLEBUF)
    pg.display.set_caption("Lino")

    clock = pg.time.Clock()
    FPS = 60

    shader_program = create_shader_program(VERTEX_SHADER, FRAGMENT_SHADER)
    square_VAO = create_square()
    
    textures = {}
    textures["background_texture"] = load_texture("pixel.png")
    textures["menu_background"] = load_texture("menu_background.png")
    textures["enter"] = load_text("Pressione Enter para jogar...", UIHandler.fonts["roboto_72"], (255, 255, 255))

    glUseProgram(shader_program)

    uniforms = {}
    uniforms["scene_loc"] = glGetUniformLocation(shader_program, "scene")

    uniforms["transform_loc"] = glGetUniformLocation(shader_program, "transform")
    uniforms["texture_loc"] = glGetUniformLocation(shader_program, "ourTexture")
    uniforms["window_size_loc"] = glGetUniformLocation(shader_program, "windowSize")
    uniforms["game_window_size_loc"] = glGetUniformLocation(shader_program, "gameWindowSize")
    uniforms["padding_loc"] = glGetUniformLocation(shader_program, "padding")
    uniforms["bar_width_loc"] = glGetUniformLocation(shader_program, "barWidth")
    uniforms["bar_padding_loc"] = glGetUniformLocation(shader_program, "barPadding")
    uniforms["element_window_width_loc"] = glGetUniformLocation(shader_program, "elementWindowWidth")
    uniforms["current_category_loc"] = glGetUniformLocation(shader_program, "currentCategory")
    uniforms["elements_list_height_loc"] = glGetUniformLocation(shader_program, "elementsListHeight")
    uniforms["elements_bar_percent_loc"] = glGetUniformLocation(shader_program, "elementsBarPercent")
    uniforms["category_height_loc"] = glGetUniformLocation(shader_program, "categoryHeight")

    uniforms["menu_outer_offset_loc"] = glGetUniformLocation(shader_program, "menuOuterOffset")
    uniforms["menu_outer_width_loc"] = glGetUniformLocation(shader_program, "menuOuterWidth")
    uniforms["menu_outer_radius_loc"] = glGetUniformLocation(shader_program, "menuOuterRadius")
    uniforms["menu_background_alpha_loc"] = glGetUniformLocation(shader_program, "menuBackgroundAlpha")

    uniforms["block_pos_loc"] = glGetUniformLocation(shader_program, "blockPos")
    uniforms["block_size_loc"] = glGetUniformLocation(shader_program, "blockSize")
    uniforms["block_color_loc"] = glGetUniformLocation(shader_program, "blockColor")
    uniforms["block_format_loc"] = glGetUniformLocation(shader_program, "blockFormat")
    
    uniforms["display_area_loc"] = glGetUniformLocation(shader_program, "displayArea")
    uniforms["is_text_loc"] = glGetUniformLocation(shader_program, "isText")

    background_transform = glm.mat4(1.0)
    background_transform = glm.scale(background_transform, glm.vec3(1.0, 1.0, 1.0))

    carry_over = 0
    for i in range(10):
        Element.blocks.append(
            Block("move_forwards", (Menu.menu_outer_offset, UIHandler.window_size[1] - Menu.menu_outer_offset - 50 - carry_over))
        )
        carry_over += Element.blocks[i].height + UIHandler.padding

    UIHandler.elements_list_height = carry_over
    UIHandler.recalc_hold_height()

    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # game_screen_center = [2 * (UIHandler.window_size[0] - UIHandler.padding - UIHandler.game_window_size[0] / 2) / UIHandler.window_size[0] - 1, 2 * (UIHandler.padding + UIHandler.game_window_size[1] / 2) / UIHandler.window_size[1] - 1]

        glClear(GL_COLOR_BUFFER_BIT)

        #global uniforms
        glUniform2f(uniforms["window_size_loc"], UIHandler.window_size[0], UIHandler.window_size[1])

        glUniform1i(uniforms["display_area_loc"], 0)
        glUniform1i(uniforms["is_text_loc"], 0)

        glUniformMatrix4fv(uniforms["transform_loc"], 1, GL_FALSE, glm.value_ptr(background_transform))
        glUniform1i(uniforms["texture_loc"], 0)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, textures["background_texture"].texture)

        glBindVertexArray(square_VAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        #ui text
        if scene == "game":
            #ui
            glUniform2f(uniforms["game_window_size_loc"], UIHandler.game_window_size[0], UIHandler.game_window_size[1])
            glUniform1f(uniforms["padding_loc"], UIHandler.padding)
            glUniform1f(uniforms["bar_padding_loc"], UIHandler.bar_padding)
            glUniform1f(uniforms["bar_width_loc"], UIHandler.bar_width)
            glUniform1f(uniforms["element_window_width_loc"], UIHandler.element_window_width)
            glUniform4f(uniforms["current_category_loc"], UIHandler.current_category[0], UIHandler.current_category[1], UIHandler.current_category[2], UIHandler.current_category[3])
            glUniform1f(uniforms["elements_list_height_loc"], UIHandler.elements_list_height)
            glUniform1f(uniforms["elements_bar_percent_loc"], UIHandler.elements_bar_percent)
            glUniform1f(uniforms["category_height_loc"], UIHandler.category_height)
            #blocks
            glUniform2f(uniforms["block_pos_loc"], 0, 0)
            glUniform2f(uniforms["block_size_loc"], 0, 0)
            glUniform4f(uniforms["block_color_loc"], 0, 0, 0, 0)
            glUniform1i(uniforms["block_format_loc"], 0)
            #layout image
            glUniform1i(uniforms["display_area_loc"], 0)
            glUniform1i(uniforms["is_text_loc"], 0)

            UIHandler.handle()

            glUniform1i(uniforms["scene_loc"], 1)

            game(square_VAO, uniforms, textures)

        elif scene == "menu":
            menu(square_VAO, uniforms, textures)

        pg.display.flip()
        
        clock.tick(FPS)

    pg.quit()

if __name__ == "__main__":
    main()