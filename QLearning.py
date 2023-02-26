import pygame
import time
import math
import sys
from collections import defaultdict
import pickle

# util files
from pygame_util import scale_image, rotate_image_ByCenter, rotate_image_ByCenter_noApply, drawRadarV2, drawTable
from RobotCar import RoboCar


def draw(win, images, car, clock, RADAR):
    for img, posi in images:
        win.blit(img, posi)



    dist = drawRadarV2(WIN, car, TRACK_OL_MASK, RADAR)
    if RADAR:
        drawTable(WIN, dist)



    car.draw(win) # Draw the car

    pygame.display.set_caption("F1 Simulator!🔥🔥\t FPS:" + str(round(clock.get_fps())))
    pygame.display.update()  # Update display after new drawing
    return dist



def startGame(car, TRACK_OL_MASK, FLAGS=None, q_table = None):

    epoch = 0 # udates after every death

    if FLAGS is None:
        FLAGS = {
            "RADAR": True
        }
    RADAR = FLAGS["RADAR"]


    lastMove = 0  # 0: fwd, 1: bkwd  ## Used to remember which the last movement was, accordingly apply friction.

    FPS = 60
    clock = pygame.time.Clock()  # To sync FPS ## no jittery

    pygame.init()
    run = True
    while run:  # handles all events (collisions, user movements, window status, etc)
        clock.tick(FPS)  # V-Sync

        lidarReadings = draw(WIN, images, car, clock, RADAR)  # Drawing ## Also handles lidar

        for event in pygame.event.get():  # Any event happened will be handelled here
            if event.type == pygame.QUIT:  # X is clicked?
                run = False
                break

        if car.TYPE == "HUMAN":
            lastMove = car.movePlayer(lastMove)

        else:
            pass
            # get some action based on lidarReadings not decided yet car.getAction(lidarReadings)
            # execute the action car.moveAi()

        # Track Boundary Detection
        if car.collision(TRACK_OL_MASK, 0, 0):  # 0,0 because mask/ track is the bigg img
            car.reset()

        # Lidar

    pygame.quit()

NoOfActions = 7
def initQtableRow():
    return [np.random.uniform(-5, 0) for i in range(NoOfActions)]

if __name__ == "__main__":
    # FLAGS
    FLAGS = {
        "RADAR" : True,
    }

    # MAIN()
    # Loading image assets
    BG = pygame.image.load("assets/bg_ucsd.png")
    # BG = scale_image(BG, 1.5) # resizing shiz to fit

    TRACK = pygame.image.load("assets/track_Zandvoort.png")

    TRACK_OL = pygame.image.load("assets/track_outline_Zandvoort.png")
    TRACK_OL_MASK = pygame.mask.from_surface(TRACK_OL)

    FINISH = pygame.image.load("assets/finishLine.png")
    FINISH = scale_image(FINISH, 0.40)
    FINISH_ROTATE = 90
    FINISH_COORDS = (460, 622)
    FINISH, FINISH_COORDS = rotate_image_ByCenter_noApply(FINISH, FINISH_COORDS, FINISH_ROTATE)
    FINISH_MASK = pygame.mask.from_surface(FINISH)

    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("F1 Simulator!🔥🔥")

    images = [(BG, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_COORDS), (TRACK_OL, (0, 0)), ]  # Order of loading assets

    CAR_R = pygame.image.load("assets/car_red.png")
    CAR_R = scale_image(CAR_R, 0.2)

    # Creating a human Object
    robo1 = RoboCar(CAR_R, 4, 2)


    # Q-Learning
    start_q_table = None # or the path of the prev wts/pickle
    q_table = ""

    # Loading existing qTable/ initializing
    if start_q_table is None:
        q_table = defaultdict(initQtableRow)  # whenever a new combination of state will be called it will be randomly initialized
        # states (radar readings) * #actions
    else:
        with open(start_q_table, "rb") as f:
            q_table = pickle.load(f)
            q_table = defaultdict(initQtableRow, q_table)


    startGame(robo1, TRACK_OL_MASK, FLAGS, q_table)