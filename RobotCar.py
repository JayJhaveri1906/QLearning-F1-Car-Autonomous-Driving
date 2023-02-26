from commonCar import AbstractCar


class RoboCar(AbstractCar): # inherits everything from super class.

    def __init__(self, CAR, max_vel, rot_vel):
        self.TYPE = "ROBO"
        self.IMG = CAR
        self.StartPos = (442, 620)
        self.StartAngle = 90

        super().__init__(max_vel, rot_vel)

    def performAction(self, lastMove, action):

        JFR = {
            0: 'w',
            1: 's',
            2: 'a',
            3: 'd',
            4: 'w+a',
            5: 'w+d',
            # 6: 'w+s',
            7: 'do nothing'
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
