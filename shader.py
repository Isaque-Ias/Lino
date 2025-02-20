from OpenGL.GL import *
import pygame as pg
import numpy as np

class Texture():
    def __init__(self, texture, width, height):
        self.texture = texture
        self.width = width
        self.height = height

def load_shader(path):
    with open(path, "r") as file:
        return file.read()

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader).decode())
    return shader

def create_shader_program(vertex, fragment):
    """Creates the shader program."""
    program = glCreateProgram()
    vertex_shader = compile_shader(vertex, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment, GL_FRAGMENT_SHADER)
    
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    
    if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(program).decode())
    
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    
    return program

def create_square():
    """Creates a textured square using two triangles."""
    vertices = np.array([
        #pos       #coords
        -1.0, -1.0, 0.0,   0.0, 0.0,  #bottom left
         1.0, -1.0, 0.0,   1.0, 0.0,  #bottom right
         1.0,  1.0, 0.0,   1.0, 1.0,  #top right

        -1.0, -1.0, 0.0,   0.0, 0.0,  #bottom left
         1.0,  1.0, 0.0,   1.0, 1.0,  #top right
        -1.0,  1.0, 0.0,   0.0, 1.0   #top left
    ], dtype=np.float32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, None)
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return VAO

def load_texture(path):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = pg.image.load(path)
    img_data = pg.image.tostring(image, "RGBA", True)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    return Texture(texture, image.get_width(), image.get_height())

def load_text(text, font, color):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    text = font.render(text, False, color)
    image = pg.surface.Surface((text.get_width(), text.get_height()))
    image.fill((0, 0, 0))
    image.blit(text, (0, 0))
    img_data = pg.image.tostring(image, "RGBA", True)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    return Texture(texture, image.get_width(), image.get_height())