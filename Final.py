import pygame
from OpenGL.GL import *
from pygame.locals import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
import numpy as np
import os
import pyrr
from ObjectLoader import ObjectLoader
from CameraPerspective import Camera


camera = Camera()
WIDTH, HEIGHT = 1280, 720
first_mouse_movement = True

vao, program, textures = None, None, None

def getFileContents(filename):
    p = os.path.join(os.getcwd(), "shaders", filename)
    return open(p, 'r').read()

def load_texture(path, texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = pygame.image.load(path)
    image = pygame.transform.flip(image, False, True)
    image_width, image_height = image.get_rect().size
    img_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture

def mouse_look(x, y):
    global first_mouse_movement, prevX, prevY

    if first_mouse_movement:
        prevX = x
        prevY = y
        first_mouse_movement = False

    if x <= 0:
        pygame.mouse.set_pos((WIDTH-2, y))
        prevX = WIDTH -2

    elif x >= WIDTH-1 :
        pygame.mouse.set_pos((1, y))
        prevX = 1

    camera.process_mouse_movement(x - prevX, prevY - y)

    prevX = x
    prevY = y


def init():
    global vao, program, textures, axum_indices, lalibela_indices, ground_indices, view_location, model_location, projection_location, axum_position, lalibela_position, ground_position
    pygame.init()
    display = (1280, 720)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    glClearColor(.0, 0.90, 1.0, 1.0)
    glViewport(0, 0, 1280, 720)

    vertexShader = compileShader(getFileContents(
        "triangle.vertex.shader"), GL_VERTEX_SHADER)
    fragmentShader = compileShader(getFileContents(
        "triangle.fragment.shader"), GL_FRAGMENT_SHADER)

    program = glCreateProgram()
    glAttachShader(program, vertexShader)
    glAttachShader(program, fragmentShader)
    glLinkProgram(program)

    axum_indices, axum_buffer = ObjectLoader().getVertexArray("models/axum2.obj")
    lalibela_indices, lalibela_buffer = ObjectLoader().getVertexArray("models/lalibelaa(2).obj")
    ground_indices, ground_buffer = ObjectLoader().getVertexArray("models/floor.obj")

    vao = glGenVertexArrays(3)
    vbo = glGenBuffers(3)

    glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
    glBufferData(GL_ARRAY_BUFFER, axum_buffer.nbytes, axum_buffer, GL_STATIC_DRAW)
    glBindVertexArray(vao[0])

    positionLocation = glGetAttribLocation(program, "position")
    glVertexAttribPointer(positionLocation, 3, GL_FLOAT, GL_FALSE,
                          8 * axum_buffer.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    texLocation = glGetAttribLocation(program, "texCoord")
    glVertexAttribPointer(texLocation, 2, GL_FLOAT, GL_FALSE,
                          8 * axum_buffer.itemsize, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    


    glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
    glBufferData(GL_ARRAY_BUFFER, lalibela_buffer.nbytes, lalibela_buffer, GL_STATIC_DRAW)
    glBindVertexArray(vao[1])

    positionLocation = glGetAttribLocation(program, "position")
    glVertexAttribPointer(positionLocation, 3, GL_FLOAT, GL_FALSE,
                          8 * lalibela_buffer.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    texLocation = glGetAttribLocation(program, "texCoord")
    glVertexAttribPointer(texLocation, 2, GL_FLOAT, GL_FALSE,
                          8 * lalibela_buffer.itemsize, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)



    glBindBuffer(GL_ARRAY_BUFFER, vbo[2])
    glBufferData(GL_ARRAY_BUFFER, ground_buffer.nbytes, ground_buffer, GL_STATIC_DRAW)
    glBindVertexArray(vao[2])

    positionLocation = glGetAttribLocation(program, "position")
    glVertexAttribPointer(positionLocation, 3, GL_FLOAT, GL_FALSE,
                          8 * ground_buffer.itemsize, ctypes.c_void_p(0))

    glEnableVertexAttribArray(0)

    texLocation = glGetAttribLocation(program, "texCoord")
    glVertexAttribPointer(texLocation, 2, GL_FLOAT, GL_FALSE,
                          8 * ground_buffer.itemsize, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)



    textures = glGenTextures(3)
    load_texture("models/axum.jpg", textures[0])
    load_texture("models/lalibelaa.jpg", textures[1])
    load_texture("models/ground.jpg", textures[2])

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glUseProgram(program)

    projection = pyrr.matrix44.create_perspective_projection_matrix(60, 1280 / 720, 0.1, 100)
    axum_position = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 15]))
    lalibela_position = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -15]))
    ground_position = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))

    model_location = glGetUniformLocation(program, "model")
    projection_location = glGetUniformLocation(program, "projection")
    view_location = glGetUniformLocation(program, "view")

    glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection)

    
    # unbind VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    # unbind VAO
    glBindVertexArray(0)

def draw():
    glBindVertexArray(vao[0])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glUniformMatrix4fv(model_location, 1, GL_FALSE, axum_position)
    glDrawArrays(GL_TRIANGLES, 0, len(axum_indices))

    glBindVertexArray(vao[1])
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glUniformMatrix4fv(model_location, 1, GL_FALSE, lalibela_position)
    glDrawArrays(GL_TRIANGLES, 0, len(lalibela_indices))

    glBindVertexArray(vao[2])
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glUniformMatrix4fv(model_location, 1, GL_FALSE, ground_position)
    glDrawArrays(GL_TRIANGLES, 0, len(ground_indices))


    glBindTexture(GL_TEXTURE_2D, 0)
    glBindVertexArray(0)


def main():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_w]:
            camera.process_keyboard_button_press("w")
        if pressed_key[pygame.K_s]:
            camera.process_keyboard_button_press("s")
        if pressed_key[pygame.K_a]:
            camera.process_keyboard_button_press("a")
        if pressed_key[pygame.K_d]:
            camera.process_keyboard_button_press("d")
        if pressed_key[pygame.K_LSHIFT]:
            camera.process_keyboard_button_press("shift")
        if pressed_key[pygame.K_TAB]:
            camera.process_keyboard_button_press("tab")


        mouse_pos = pygame.mouse.get_pos()
        mouse_look(mouse_pos[0], mouse_pos[1])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        view = camera.get_view()
        glUniformMatrix4fv(view_location, 1, GL_FALSE, view)            
            
        draw()
        pygame.display.flip()

main()
