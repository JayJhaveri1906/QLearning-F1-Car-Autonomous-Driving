import pygame


def scale_image(img, factor):  # resize the image
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def rotate_image_ByCenter(win, img, top_left, angle):
    rotImg = pygame.transform.rotate(img, angle) # pygame default rotate at topleft ig...
    newRect = rotImg.get_rect(center=img.get_rect(topleft=top_left).center) # To avoid morphing/destortion after
    # rotation, translate the new image back to the new center
    win.blit(rotImg, newRect) # rotated image with new coordinates.


def rotate_image_ByCenter_noApply(img, top_left, angle):
    rotImg = pygame.transform.rotate(img, angle) # pygame default rotate at topleft ig...
    newRect = rotImg.get_rect(center=img.get_rect(topleft=top_left).center) # To avoid morphing/destortion after
    # rotation, translate the new image back to the new center
    return rotImg, newRect

