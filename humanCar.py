import pygame
from commonCar import AbstractCar


class HumanPlayer(AbstractCar): # inherits everything from super class.

    def __init__(self, CAR, max_vel, rot_vel):
        self.TYPE = "HUMAN"
        self.IMG = CAR
        self.StartPos = (442, 620)
        self.StartAngle = 90

        super().__init__(max_vel, rot_vel)

    def movePlayer(self, lastMove):

        keys = pygame.key.get_pressed()

        moved = False

        if keys[pygame.K_a]:
            self.rotate(left=True)
        if keys[pygame.K_d]:
            self.rotate(right=True)
        if keys[pygame.K_w]:
            moved = True
            lastMove = 0
            self.move_fwd()
        if keys[pygame.K_s]:
            moved = True
            lastMove = 1
            self.move_bkwd()

        if not moved:
            if lastMove == 0:
                self.fwdFriction()
            if lastMove == 1:
                self.bkwdFriction()

        return lastMove
