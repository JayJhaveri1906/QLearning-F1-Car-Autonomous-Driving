import pygame
import math
import time


def scale_image(img, factor):  # resize the image
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def rotate_image_ByCenter(win, img, top_left, angle):  # For Dynamic Car Rotate
    rotImg = pygame.transform.rotate(img, angle)  # pygame default rotate at topleft ig...
    newRect = rotImg.get_rect(center=img.get_rect(topleft=top_left).center)  # To avoid morphing/destortion after
    # rotation, translate the new image back to the new center
    win.blit(rotImg, newRect)  # rotated image with new coordinates.


def rotate_image_ByCenter_noApply(img, top_left, angle):  # For Once rotate like FINISH
    rotImg = pygame.transform.rotate(img, angle)  # pygame default rotate at topleft ig...
    newRect = rotImg.get_rect(center=img.get_rect(topleft=top_left).center)  # To avoid morphing/destortion after
    # rotation, translate the new image back to the new center
    return rotImg, newRect


def drawTable(win, dist):
    # Set the font for the table
    font = pygame.font.SysFont(None, 15)
    COLOR = (255, 0, 0)
    XOffset = 600
    YOffset = 20

    # Define the row and column size for the table
    row_size = 10
    column_size = 100

    # Draw the table headers
    headers = ["Angle", "Distance"]
    for i, header in enumerate(headers):
        text = font.render(header, True, COLOR)
        x = XOffset + (i * column_size + (column_size - text.get_width()) / 2)
        y = YOffset
        win.blit(text, (x, y))

    # Draw the table data
    c = 0
    for k in dist:
        text = font.render(str(round(k,5)), True, COLOR)
        x = XOffset
        y = YOffset + ((c + 1) * row_size)
        win.blit(text, (x, y))

        text = font.render(str(round(dist[k],5)), True, COLOR)
        x = XOffset + column_size
        win.blit(text, (x, y))

        c+=1


def drawRadarV2(win, car, trackMask, FLAGS):
    # Angle of orientation from the y axis
    angle_radians = math.radians(car.angle)

    # Center coordinates of the car current
    x, y = car.img.get_rect(topleft=(car.x, car.y)).center
    # win_line = pygame.Surface((win.get_width(), win.get_height()), pygame.SRCALPHA)
    MAX_DISTANCE = 600

    dick = {
        "FRONT RAY": 0,
        # "FRONT RAY Quad": math.pi / 16,
        # "FRONT RAY -Quad": -math.pi / 16,
        "FRONT RAY Oct": math.pi / 8,
        "FRONT RAY -Oct": -math.pi / 8,
        "FRONT RAY 5OCT": 3 * math.pi / 8,
        "FRONT RAY -5OCT": -3 * math.pi / 8,

        # "BACK RAY": math.pi,
        # "BACK RAY Quad": math.pi - math.pi / 4,
        # "BACK RAY -Quad": math.pi + math.pi / 4,

        # "LEFT": -math.pi / 2,
        # "RIGHT": math.pi / 2
    }

    dist = {
        0: -1,
        # math.pi / 16: MAX_DISTANCE,
        # -math.pi / 16: MAX_DISTANCE,
        math.pi / 8: MAX_DISTANCE,
        -math.pi / 8: MAX_DISTANCE,
        3 * math.pi / 8: MAX_DISTANCE,
        -3 * math.pi / 8: MAX_DISTANCE,

        # math.pi: MAX_DISTANCE,
        # math.pi - math.pi / 4: MAX_DISTANCE,
        # math.pi + math.pi / 4: MAX_DISTANCE,
        #
        # -math.pi / 2: MAX_DISTANCE,
        # math.pi / 2: MAX_DISTANCE,
    }

    # Displaying multiple lines (radar)
    for offset in dick.values():
        endX, endY = (x - 1000 * math.sin(angle_radians + offset),
                      y - 1000 * math.cos(angle_radians + offset))

        # if RADAR:
        #     pygame.draw.line(win, (0, 0, 0), (x, y), (endX, endY), 1)

        # for i in range(win.get_width()):
        for i in range(MAX_DISTANCE): # max distance you think it could be at
            # Calculate the coordinates of the current pixel along the ray
            px = x - i * math.sin(angle_radians + offset)
            py = y - i * math.cos(angle_radians + offset)
            pixel_pos = (int(px), int(py))

            # if RADAR:
            #     pygame.draw.circle(win, (0, 0, 0), pixel_pos, 1)

            # Check if the pixel position intersects with the mask
            mask_value = trackMask.get_at(pixel_pos) # Returns if mask is not transparent at that posi

            # Check if the pixel is not transparent
            if mask_value != 0:
                # Intersection found, draw a red point
                if FLAGS["RADAR"]:
                    pygame.draw.line(win, (0, 0, 0), (x, y), pixel_pos, 1)
                    pygame.draw.circle(win, (255, 0, 0), pixel_pos, 3)

                # distance = math.dist((x, y), pixel_pos)  # Works in python 3.8 not in 3.6 sed
                # sqrt((x2 - x1) ^ 2 + (y2 - y1) ^ 2)
                distance = math.sqrt((pixel_pos[0]-x)**2 + (pixel_pos[1]-y)**2)
                dist[offset] = distance
                break
    return dist


def drawRadarV1(win, car, trackMask, RADAR):
    # Angle of orientation from the y axis
    angle_radians = math.radians(car.angle)

    # Center coordinates of the car current
    x, y = car.img.get_rect(topleft=(car.x, car.y)).center
    # win_line = pygame.Surface((win.get_width(), win.get_height()), pygame.SRCALPHA)

    dick = {
        "FRONT RAY": 0,
        "FRONT RAY Quad": math.pi / 16,
        "FRONT RAY -Quad": -math.pi / 16,
        "FRONT RAY Oct": math.pi / 8,
        "FRONT RAY -Oct": -math.pi / 8,
        "FRONT RAY 5OCT": 3 * math.pi / 8,
        "FRONT RAY -5OCT": -3 * math.pi / 8,

        "BACK RAY": math.pi,
        "BACK RAY Quad": math.pi - math.pi / 4,
        "BACK RAY -Quad": math.pi + math.pi / 4,

        "LEFT": -math.pi / 2,
        "RIGHT": math.pi / 2
    }

    # Displaying multiple lines (radar)
    for offset in dick.values():
        endX, endY = (x - 1000 * math.sin(angle_radians + offset),
                      y - 1000 * math.cos(angle_radians + offset))

        if RADAR:
            pygame.draw.line(win, (0, 0, 0), (x, y), (endX, endY), 1)

        for i in range(win.get_width()):
            # Calculate the coordinates of the current pixel along the ray
            px = x - i * math.sin(angle_radians + offset)
            py = y - i * math.cos(angle_radians + offset)
            pixel_pos = (int(px), int(py))

            # Check if the pixel position intersects with the mask

            mask_value = trackMask.get_at(pixel_pos)

            # Check if the pixel is not transparent
            if mask_value != 0:
                # Intersection found, draw a red point
                if RADAR:
                    pygame.draw.circle(win, (255, 0, 0), pixel_pos, 3)
                break

        # Checking Collision
        ## Converting the line into a mask, such that we check collision
        # win_line = pygame.display.set_mode((win.get_width(), win.get_height()))

        # win_line.
        # pygame.draw.line(win_line, (0, 0, 0), (x, y), (endX, endY), 1) # Draw the line on the new surface

        # line_mask = pygame.mask.from_surface(win_line) # creates a line mask

        ## Collision:
        # no offset because both's top-left at 0,0
        # offset_ = (0,0)
        # track and the car to compare intersection between them.
        # poi = trackMask.overlap(line_mask, offset_)  # Calculate the point of intersection. Returns None if no intersection.

        # print(poi)
        # time.sleep(2)
        # sys.exit("bruh")

        # pygame.draw.circle(win, (255, 255, 0), pixel_pos, 5)
