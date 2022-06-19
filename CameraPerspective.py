from pyrr import *
from math import *

class Camera:
    def __init__(self):
        self.cam_position = Vector3([-10.0, 30.0, 40.0])
        self.cam_front = None
        self.cam_right = None
        self.cam_up = None
        self.mouse_sensitivity = 0.15
        self.yaw = -90
        self.pitch = 0
        self.speed = 0.02

    def get_view(self):
        return matrix44.create_look_at(self.cam_position, self.cam_position + self.cam_front, self.cam_up)

    def process_mouse_movement(self, xDifference, yDifference):
        xDifference *= self.mouse_sensitivity
        yDifference *= self.mouse_sensitivity

        self.yaw += xDifference
        self.pitch += yDifference

        if self.pitch > 45:
            self.pitch = 45
        if self.pitch < -45:
            self.pitch = -45

        front = Vector3([
            cos(radians(self.yaw)) * cos(radians(self.pitch)), 
            sin(radians(self.pitch)),
            sin(radians(self.yaw)) * cos(radians(self.pitch))
        ])

        self.cam_front = vector.normalise(front)
        self.cam_right = vector.normalise(vector3.cross(self.cam_front, Vector3([0.0, 1.0, 0.0])))
        self.cam_up = vector.normalise(vector3.cross(self.cam_right, self.cam_front))


    def process_keyboard_button_press(self, pressed):
        if pressed == "w":
            self.cam_position += self.cam_front * self.speed
        if pressed == "s":
            self.cam_position -= self.cam_front * self.speed
        if pressed == "a":
            self.cam_position -= self.cam_right * self.speed
        if pressed == "d":
            self.cam_position += self.cam_right * self.speed
        if pressed == "shift":
            self.speed = 0.05
        if pressed == "tab":
            self.speed = 0.02