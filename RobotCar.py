from commonCar import AbstractCar
import pygame


class RoboCar(AbstractCar): # inherits everything from super class.

    def __init__(self, CAR, max_vel, rot_vel):
        self.TYPE = "ROBO"
        self.IMG = CAR
        self.StartPos = (442, 620)
        self.StartAngle = 90

        super().__init__(max_vel, rot_vel)


    def getHumanAction(self):  # To get faster learning....
        keys = pygame.key.get_pressed()
        action = 6 # default do nothing

        if keys[pygame.K_a]:
            action = 2
        if keys[pygame.K_d]:
            action = 3
        if keys[pygame.K_w]:
            action = 0
        if keys[pygame.K_s]:
            action = 1
        if keys[pygame.K_w] and keys[pygame.K_a]:
            action = 4
        if keys[pygame.K_w] and keys[pygame.K_d]:
            action = 5
        if keys[pygame.K_h]:  # save the model using human input
            action = -1

        return action


    def performAction(self, lastMove, action):

        JFR = {
            0: 'w',
            1: 's',
            2: 'a',
            3: 'd',
            4: 'w+a',
            5: 'w+d',
            # 6: 'w+s',
            6: 'do nothing'
        } # Just For Reference

        moved = False

        # Turn before accelerating
        if action == 2:
            self.rotate(left=True)

        elif action == 3:
            self.rotate(right=True)


        elif action == 0:
            moved = True
            lastMove = 0
            self.move_fwd()

        elif action == 1:
            moved = True
            lastMove = 1
            self.move_bkwd()


        elif action == 4:
            self.rotate(left=True)

            moved = True
            lastMove = 0
            self.move_fwd()

        elif action == 5:
            self.rotate(right=True)

            moved = True
            lastMove = 0
            self.move_fwd()

        # elif action == 6:
        #     self.move_fwd()
        #
        #     moved = True
        #     lastMove = 1
        #     self.move_bkwd()
        else:
            pass

        if not moved:
            if lastMove == 0:
                self.fwdFriction()
            if lastMove == 1:
                self.bkwdFriction()
