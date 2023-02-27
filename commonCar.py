import pygame
import math
from pygame_util import rotate_image_ByCenter


class AbstractCar:  # Abstract parent class of a car
    def __init__(self, max_vel, rot_vel):
        self.img = self.IMG  # my car
        self.max_vel = max_vel
        self.vel = 0  # starting velo
        self.rot_vel = rot_vel  # how quickly you can turn
        self.angle = self.StartAngle  # starting angle
        self.x, self.y = self.StartPos
        self.acc = 0.05  # px/s

    def rotate(self, left=False, right=False):  # Rotate the car
        if left:
            self.angle += self.rot_vel
        elif right:
            self.angle -= self.rot_vel

    def move_fwd(self):
        self.vel = min(self.vel + self.acc, self.max_vel)  # acceerate the car
        self.move()

    def move_bkwd(self):
        if self.vel > 0:
            self.vel = max(self.vel - 3 * self.acc, 0)  # acceerate the car
        # else:  # Removed Reversing for now
        #     self.vel = max(self.vel - self.acc, -self.max_vel / (1.5))  # acceerate the car

        self.move()

    def move(self):
        radians = math.radians(self.angle)
        yvel = math.cos(radians) * self.vel
        xvel = math.sin(radians) * self.vel
        self.x -= xvel  # - because of the perspective...
        self.y -= yvel

    def fwdFriction(self):
        self.vel = max(self.vel - (self.acc / 4), 0)  # Forward friction
        self.move()

    def bkwdFriction(self):
        self.vel = min(self.vel + (self.acc / 4), 0)  # Backward friction
        self.move()

    def collision(self, mask, x=0, y=0):
        carMask = pygame.mask.from_surface(self.img)
        offSet = (int(self.x - x), int(self.y - y))  # Calculating the difference between the topLeft coords of the
        # track and the car to compare intersection between them.
        poi = mask.overlap(carMask, offSet)  # Calculate the point of intersection. Returns None if no intersection.

        return poi

    def reset(self):
        self.vel = 0
        self.x, self.y = self.StartPos
        self.angle = self.StartAngle

    def draw(self, win):
        rotate_image_ByCenter(win, self.img, (self.x, self.y), self.angle)
