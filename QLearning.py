import pygame
import time
import math
import sys
from collections import defaultdict
import pickle
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

style.use("ggplot") # fancy graphs xd

# util files
from pygame_util import scale_image, rotate_image_ByCenter, rotate_image_ByCenter_noApply, drawRadarV2, drawTable
from RobotCar import RoboCar


def draw(win, images, rewardGate, car, clock, FLAGS):
    if FLAGS["RENDER"]:
        for img, posi in images[:-1]:
            win.blit(img, posi)

    if FLAGS["REWARD"]:
        win.blit(rewardGate, (0, 0))

    if FLAGS["RENDER"]:
        win.blit(images[-1][0], images[-1][1])

    dist = drawRadarV2(WIN, car, TRACK_OL_MASK, FLAGS)
    if FLAGS["RADAR"]:
        drawTable(WIN, dist)

    if FLAGS["RENDER"]:
        car.draw(win)  # Draw the car

        pygame.display.set_caption("F1 Simulator!🔥🔥\t FPS:" + str(round(clock.get_fps())))
        pygame.display.update()  # Update display after new drawing
    return dist


# Bucketing
def bucketReading(lidarReadings, buckets):
    return tuple(np.ceil(np.round(list(lidarReadings.values())) / buckets).astype(int))


def startGame(car, TRACK_OL_MASK, REWARDS, REWARDS_mask, FLAGS=None, q_table = None):

    if FLAGS is None:
        FLAGS = {
            "RADAR": True,
            "REWARD": True,
            "RENDER": True,
            "HUMAN_TRAIN": True
        }

    lastMove = 0  # 0: fwd, 1: bkwd  ## Used to remember which the last movement was, accordingly apply friction.
    gateNo = 0  # handles which reward gate is activated


    # Q-learning variable
    epoch = 0  # updates after every death
    MOVE_PENALTY = 10
    DEATH_PENALTY = 3000
    GATE_REWARD = 500
    FINAL_REWARD = 1000
    TIME_COUNTER = 0
    MAX_TIME_PER_GATE = 500

    # Made epsilon reward Gate based
    if FLAGS["HUMAN_TRAIN"]:
        epsilon = [1] * len(REWARDS_mask)
        EPS_DECAY = 1
    else:
        # epsilon = [0.9] * len(REWARDS_mask)
        epsilon = [0.00607039955568851, 0.041208891621480594, 0.05790120948680733, 0.232565335586142,
                   0.35220829642741547, 0.5177322779220248, 0.6887501638125324, 0.7551674354364434, 0.9, 0.9, 0.9, 0.9,
                   0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9,
                   0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
        EPS_DECAY = 1 - (3 * 10**-4)

    if FLAGS["TEST"]:
        epsilon = [0] * len(REWARDS_mask)
        EPS_DECAY = 0

    SHOW_EVERY = 200

    LEARNING_RATE = 0.1
    DISCOUNT = 0.65

    BUCKETS = 1
    ###################


    FPS = 60
    clock = pygame.time.Clock()  # To sync FPS ## no jittery

    pygame.init()

    # Original Readings
    lidarReadings = draw(WIN, images, REWARDS[gateNo], car, clock, FLAGS)  # Drawing ## Also handles lidar

    # Bucketing our radar readings into a bucket of 3 to save space basically in short cause the qtabe
    # naturally would become 600 * 600 * 600...#obs times * #actions
    # this makes it 200 * 200 ...# obs times * #act
    obs = bucketReading(lidarReadings, BUCKETS)

    epoch_rewards = []
    episodeReward = 0

    run = True
    while run:  # handles all events (collisions, user movements, window status, etc)
        clock.tick(FPS)  # V-Sync
        TIME_COUNTER += 1

        if TIME_COUNTER == MAX_TIME_PER_GATE:
            TIME_COUNTER = 0
            car.reset()
            lidarReadings = draw(WIN, images, REWARDS[gateNo], car, clock, FLAGS)
            obs = bucketReading(lidarReadings, BUCKETS)
            gateNo = 0
            epsilon[gateNo] *= EPS_DECAY
            print(f"time ran out ded {epoch}")
            epoch += 1

        for event in pygame.event.get():  # Any event happened will be handelled here
            if event.type == pygame.QUIT:  # X is clicked?
                run = False
                break

        if car.TYPE == "HUMAN":
            lastMove = car.movePlayer(lastMove)

        else:
            # save model
            keys_ = pygame.key.get_pressed()
            if keys_[pygame.K_p]:  # save the model using human input
                with open(f"qTables/qtableSavedModelP-{int(time.time())}_{epoch},{BUCKETS}.pickle", "wb") as f:
                    pickle.dump(q_table, f)
                print("saved model")


            if np.random.random() > epsilon[gateNo]:    # Don't explore
                action = np.argmax(q_table[obs])
            else:                               # explore
                if FLAGS["HUMAN_TRAIN"]:
                    action = car.getHumanAction()  # humanized learning???
                    if action == -1:
                        with open(f"qTables/qtableHumanSave-{int(time.time())}_{epoch},{BUCKETS}.pickle", "wb") as f:
                            pickle.dump(q_table, f)

                        action = 6
                else:
                    action = np.random.randint(0, NoOfActions)


            lastMove = car.performAction(lastMove, action)  # perform the action

        # Track Boundary Detection
        if car.collision(TRACK_OL_MASK, 0, 0): # 0,0 because mask/ track is the bigg img
            car.reset()
            reward = -DEATH_PENALTY
            epsilon[gateNo] *= EPS_DECAY
            gateNo = 0 # handles reward gate

        # Checking Reward Gate Collision
        elif car.collision(REWARDS_mask[gateNo], 0, 0):
            # print("Reward!")
            reward = GATE_REWARD * (gateNo+1)
            gateNo += 1
            gateNo %= len(REWARDS_mask) # modulus restarts gate automatically


            # Handle if last reward gate (FINISH)
            if gateNo == len(REWARDS_mask)-1:
                print("Reach Finished at ", epoch)
                with open(f"qTables/qtableFinish-{int(time.time())}_{epoch},{BUCKETS}.pickle", "wb") as f:
                    pickle.dump(q_table, f)
                epoch += 1
                reward = FINAL_REWARD

        else:
            reward = -MOVE_PENALTY

        newLidarReadings = draw(WIN, images, REWARDS[gateNo], car, clock, FLAGS)  # Drawing ## Also handles lidar
        newObs = bucketReading(newLidarReadings, BUCKETS) # bucketing

        maxFutureQ = np.max(q_table[newObs])
        current_q = q_table[obs][action]

        if reward == GATE_REWARD:
            print("gate", epoch, "time taken:", TIME_COUNTER)
            TIME_COUNTER = 0
            new_q = GATE_REWARD
        elif reward == -DEATH_PENALTY:
            new_q = -DEATH_PENALTY
            print("ded", epoch)
        elif reward == FINAL_REWARD:
            new_q = FINAL_REWARD
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * maxFutureQ)

        q_table[obs][action] = new_q

        episodeReward += reward
        if reward % GATE_REWARD == 0 or reward == -DEATH_PENALTY:

            if (epoch) % SHOW_EVERY == 0 and reward == -DEATH_PENALTY:
                print(f"At {epoch},{BUCKETS}, exploration {epsilon[gateNo]}, Gate: {gateNo}")
                print(epsilon)
                with open(f"qTables/qtable-{int(time.time())}_{epoch},{BUCKETS}.pickle", "wb") as f:
                    pickle.dump(q_table, f)

            if reward == -DEATH_PENALTY:
                epoch += 1
                epoch_rewards.append(episodeReward)
                episodeReward = 0
                # Decay exploration:
                # print(epsilon)

        obs = newObs





    # Saving Final Qtable:
    with open(f"qTables/qtable-{int(time.time())}.pickle", "wb") as f:
        pickle.dump(q_table, f)

    pygame.quit()

NoOfActions = 7
def initQtableRow():
    return [np.random.uniform(-5, 0) for i in range(NoOfActions)]

if __name__ == "__main__":
    # FLAGS
    FLAGS = {
        "RADAR": False,
        "REWARD": False,
        "RENDER": False,
        "HUMAN_TRAIN": False,
        "TEST": False,
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
    # sys.exit("bruh")
    pygame.display.set_caption("F1 Simulator!🔥🔥")
    if not FLAGS["RENDER"]:
        pygame.quit()

    CAR_R = pygame.image.load("assets/car_red.png")
    CAR_R = scale_image(CAR_R, 0.2)

    # Reward Gates loading into an array
    map = "Zandvoort"
    folder_path = "assets/rewardGates/" + str(map)
    png_files = glob.glob(folder_path + "/*.png")
    num_files = len(png_files)
    REWARDS = []
    REWARDS_mask = []
    for i in range(num_files):
        rewardGate = pygame.image.load(folder_path + "/RG" + str(i) + ".png")
        REWARDS.append(rewardGate)
        reward_mask = pygame.mask.from_surface(rewardGate)
        REWARDS_mask.append(reward_mask)

    images = [(BG, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_COORDS), (TRACK_OL, (0, 0)), ]  # Order of loading assets



    # Creating a Robo Object
    robo1 = RoboCar(CAR_R, 2, 2)

    # Q-Learning
    # 1600 + 2200 + 4400 + 11200 + 8400 + 8200(higher exploration) + 10200 + 12400 + 52_human_wted rewards +
    # +
    start_q_table = "qTables/qtableHumanSave-1677722381_52,1.pickle"  # or the path of the prev wts/pickle
    # start_q_table = None

    q_table = ""

    # Loading existing qTable/ initializing
    if start_q_table is None:
        q_table = defaultdict(initQtableRow)  # whenever a new combination of state will be called it will be randomly initialized
        # states (radar readings) * #actions
    else:
        print("Loading PreTrained qtable")
        with open(start_q_table, "rb") as f:
            q_table = pickle.load(f)
            print(type(q_table))
            # q_table = defaultdict(initQtableRow, q_table)


    startGame(robo1, TRACK_OL_MASK, REWARDS, REWARDS_mask, FLAGS, q_table)