from LoadImage import load_image
import pygame as pg
import random


class Ball():
    def __init__(self, tp):
        width, height = 800, 600
        if tp == 0:
            tp = random.randint(1, 3)

        if tp == 1:
            self.picture = load_image("red_ball.png", -1)
        elif tp == 2:
            self.picture = load_image("green_ball.png", -1)
        elif tp == 3:
            self.picture = load_image("blue_ball.png", -1)

        a = [random.randint(0, width // 2 - self.picture.get_rect().width),
             random.randint(width // 2 + self.picture.get_rect().width, width - self.picture.get_rect().width)]
        b = [random.randint(0, height // 2 - self.picture.get_rect().height),
             random.randint(height // 2 + self.picture.get_rect().height, height - self.picture.get_rect().height)]

        self.rect = pg.Rect((a[random.randint(0, 1)], b[random.randint(0, 1)],
                             self.picture.get_rect().width,
                             self.picture.get_rect().height))

        self.angle = random.randint(0, 360)
        self.speed = 4
