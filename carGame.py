import pygame
import time
import math

# util files
from pygame_util import scale_image, rotate_image_ByCenter


# MAIN()
# Loading image assets
BG = pygame.image.load("assets/bg_ucsd.png")
# BG = scale_image(BG, 1.5) # resizing shiz to fit

TRACK = pygame.image.load("assets/track_Zandvoort.png")
TRACK_OL = pygame.image.load("assets/track_outline_Zandvoort.png")
FINISH = pygame.image.load("assets/finishLine.png")
FINISH = scale_image(FINISH, 0.2)

CAR_R = pygame.image.load("assets/car_red.png")
CAR_R = scale_image(CAR_R, 0.2)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("F1 Simulator!🔥🔥")

images = [(BG, (0,0)), (TRACK, (0, 0)), (FINISH, (0, 0)),] # Order of loading assets


class AbstractCar:  # Abstract parent class of a car
    def __init__(self, max_vel, rot_vel):
        self.img = self.IMG # my car
        self.max_vel = max_vel
        self.vel = 0 # starting velo
        self.rot_vel = rot_vel # how quickly you can turn
        self.angle = -70 # starting angle
        self.x, self.y = self.StartPos
        self.acc = 0.1 # px/s

    def rotate(self, left = False, right = False): # Rotate the car
        if left:
            self.angle += self.rot_vel
        elif right:
            self.angle -= self.rot_vel

    def move_fwd(self):
        self.vel = min(self.vel + self.acc, self.max_vel) # acceerate the car
        self.move()

    def move_bkwd(self):
        self.vel = max(self.vel - self.acc, -self.max_vel/(1.5)) # acceerate the car
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        yvel = math.cos(radians) * self.vel
        xvel = math.sin(radians) * self.vel
        self.x -= xvel  # - because of the perspective...
        self.y -= yvel

    def fwdFriction(self):
        self.vel = max(self.vel - (self.acc/4), 0) # Forward friction
        self.move()

    def bkwdFriction(self):
        self.vel = min(self.vel + (self.acc/4), 0) # Backward friction
        self.move()

    def draw(self, win):
        rotate_image_ByCenter(win, self.img, (self.x, self.y), self.angle)


class HumanPlayer(AbstractCar): # inherits everything from super class.
    IMG = CAR_R
    StartPos = (100, 297)

def draw(win, images, humanCar):
    for img, posi in images:
        win.blit(img, posi)

    humanCar.draw(win) # Draw the car
    pygame.display.set_caption(str(round(clock.get_fps())))
    pygame.display.update()  # Update display after new drawing


lastMove = 0 # 0: fwd, 1: bkwd  ## Used to remember which the last movement was, accordingly apply friction.
def movePlayer(player):
    global lastMove

    keys = pygame.key.get_pressed()

    moved = False

    if keys[pygame.K_a]:
        player.rotate(left=True)
    if keys[pygame.K_d]:
        player.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        lastMove = 0
        player.move_fwd()
    if keys[pygame.K_s]:
        moved = True
        lastMove = 1
        player.move_bkwd()

    if not moved:
        if lastMove == 0:
            player.fwdFriction()
        if lastMove == 1:
            player.bkwdFriction()


human1 = HumanPlayer(1.5, 2)

FPS = 60
clock = pygame.time.Clock() # To sync FPS ## no jittery


run = True
while run: # handles all events (collisions, user movements, window status, etc)
    clock.tick(FPS)  # V-Sync

    # WIN.blit(BG, (0, 0)) # drawing image on the display, 0,0 is the position// top left origin
    draw(WIN, images, human1) # Drawing


    for event in pygame.event.get(): # Any event happened will be handelled here
        if event.type == pygame.QUIT: # X is clicked?
            run = False
            break

    movePlayer(human1)


pygame.quit()
