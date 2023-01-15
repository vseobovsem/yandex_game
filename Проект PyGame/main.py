import math
import pygame as pg
import time
import os
from Ball import Ball
from Wall import Wall
from LoadImage import load_image
from pygame.locals import *

state = ["start", "menu", "game", "end", "exit"]
currentState = state[0]

pg.init()
back = "white"
diff_bg = (255, 255, 0)
size = width, height = 800, 600
screen = pg.display.set_mode(size, FULLSCREEN)
table = load_image("table2.png", 2)

# playerцц
play = load_image("player.png", -1)
plx = width / 2
ply = height / 2
gamer = pg.Rect(plx, ply, play.get_rect().width, play.get_rect().height)

# explosion
babax = load_image("babax.png", -1)
song1 = pg.mixer.Sound(os.path.join('data', "babax_noise.mp3"))  # добавим музыку
song2 = pg.mixer.Sound(os.path.join('data', "music.mp3"))  # добавим музыку

while True:
    song2.play()
    if currentState == "start":
        pg.mouse.set_visible(0)
        balls = [Ball(1), Ball(2), Ball(3)]
        angle_player = 0
        fl_gamer = False
        fl_gamer_left = False
        fl_gamer_right = False
        cursor_speed = 3.5
        counter_spawn = 150
        time_counter = 0
        clock = pg.time.Clock()
        fps = 60
        time_count = 0
        win = 2
        complication = "Normal"
        best = [0, 0, 0]  # счет
        walls_count = 2
        walls = []
        lives = 1

        lines = open(os.path.join('data', 'результат игры.txt')).read().splitlines()
        record = lines[0].split()[1]

        currentState = "menu"
    #  меню
    if currentState == "menu":
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    currentState = "exit"
                if event.key == K_SPACE:
                    currentState = "game"
                if event.key == K_DOWN and complication != "Easy":
                    if complication == "Hard":
                        complication = "Normal"
                    else:
                        complication = "Easy"
                if event.key == K_UP and complication != "Hard":
                    if complication == "Easy":
                        complication = "Normal"
                    else:
                        complication = "Hard"
        if complication == "Easy":
            counter_spawn = 250
            diff_bg = (0, 255, 0)
            lives = 7
            win = 1
            walls_count = 4
        if complication == "Normal":
            counter_spawn = 150
            diff_bg = (255, 255, 0)
            lives = 5
            win = 2
            walls_count = 6
        if complication == "Hard":
            diff_bg = (240, 7, 62)
            counter_spawn = 50
            lives = 3
            win = 4
            walls_count = 8
        screen.fill((100, 100, 100))
        text_title = pg.font.SysFont(None, 125)
        text_phrase = pg.font.SysFont(None, 75)
        text_phrase2 = pg.font.SysFont(None, 25)
        title = text_title.render("Побег", True, "black")
        screen.blit(title, (40, 40))
        s1 = text_phrase.render("Нажмите пробел, чтобы начать", True, "black", (255, 255, 255))
        s2 = text_phrase.render("Нажмите esc, чтобы выйти", True, "black", (255, 255, 255))
        s3 = text_phrase.render(complication, True, "black", diff_bg)
        s4 = text_phrase2.render("Воспользуйтесь стрелками, чтобы изменить уровень", True, "black")
        s5 = text_phrase.render("Уровень:", True, "black")
        screen.blit(s1, (10, 315))
        screen.blit(s2, (65, 390))
        screen.blit(s3, (500, 100))
        screen.blit(s4, (350, 215))
        screen.blit(s5, (470, 10))
        pg.draw.polygon(screen, "black", ((500, 90), (525, 65), (550, 90)))
        pg.draw.polygon(screen, "black", ((500, 167), (525, 192), (550, 167)))
        pg.display.update()
        if currentState != "menu":
            walls = []
            for i in range(walls_count):
                walls.append(Wall())
    #  game
    if currentState == "game":
        time_count += 1  # время

        # print background and score
        screen.blit(table, (0, 0))
        score = int((round(time_count / fps, 2))) * win
        text = pg.font.SysFont(None, 25)
        s = text.render("счет: " + str(score), True, "black", (255, 255, 255))
        screen.blit(s, (10, 10))
        s = text.render("жизни: " + str(lives), True, "black", (255, 255, 255))
        screen.blit(s, (10, 30))
        s = text.render("рекорд: " + str(record), True, "black", (255, 255, 255))
        screen.blit(s, (10, 50))
        if fl_gamer_left:
            angle_player += 5
        if fl_gamer_right:
            angle_player -= 5
        if fl_gamer:
            b = math.cos(math.radians(angle_player)) * cursor_speed
            a = math.sin(math.radians(angle_player)) * cursor_speed
            gamer.top += round(b)
            gamer.left += round(a)

        for event in pg.event.get():
            if event.type == QUIT:
                currentState = "exit"
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    currentState = "exit"
                if event.key == K_UP or event.key == K_w:
                    fl_gamer = True
                if event.key == K_LEFT or event.key == K_a:
                    fl_gamer_left = True
                if event.key == K_RIGHT or event.key == K_d:
                    fl_gamer_right = True
            if event.type == KEYUP:
                if event.key == K_UP or event.key == K_w:
                    fl_gamer = False
                if event.key == K_LEFT or event.key == K_a:
                    fl_gamer_left = False
                if event.key == K_RIGHT or event.key == K_d:
                    fl_gamer_right = False

        #  Обработка balls
        for i in range(len(balls)):
            if balls[i].rect.top <= 0 or balls[i].rect.bottom >= height:
                balls[i].angle = 360 - balls[i].angle
            if balls[i].rect.left <= 0 or balls[i].rect.right >= width:
                balls[i].angle = 180 - balls[i].angle
            b = math.cos(math.radians(balls[i].angle)) * balls[i].speed
            a = math.sin(math.radians(balls[i].angle)) * balls[i].speed
            balls[i].rect.left += b
            balls[i].rect.top += a

        rectan_player = play.get_rect().center
        neu_player = pg.transform.rotate(play, angle_player - 180)
        neu_player.get_rect().center = rectan_player
        rectan_player = play.get_rect()
        center_neu = neu_player.get_rect().center
        center_diff = (gamer.center[0] - center_neu[0], gamer.center[1] - center_neu[1])
        # Команды для игрока

        time_counter += 1
        if time_counter >= counter_spawn:
            balls.append(Ball(0))
            time_counter = 0

        # Проверка касания ball
        for i in balls:
            if gamer.colliderect(i):
                balls.remove(i)
                lives -= 1
                gamer.left = width / 2 - gamer.width / 2
                gamer.top = height / 2 - gamer.height / 2

        # Проверка касания wall
        for i in walls:
            if gamer.colliderect(i):
                lives -= 1
                gamer.left = width / 2 - gamer.width / 2
                gamer.top = height / 2 - gamer.height / 2

        # Проверка касания границ
        if not gamer.colliderect(0, 0, width, height):
            lives -= 1
            gamer.left = width / 2 - gamer.width / 2
            gamer.top = height / 2 - gamer.height / 2

        for i in range(len(balls)):
            screen.blit(balls[i].picture, balls[i].rect)
        for i in range(len(walls)):
            screen.blit(walls[i].picture, walls[i].rect)
        screen.blit(neu_player, center_diff)
        pg.display.update()

        if lives < 1:
            screen.blit(babax, (
                center_diff[0] - babax.get_rect().width / 2 + 12,
                center_diff[1] - babax.get_rect().height / 2 + 12))
            song2.stop()
            song1.play()
            pg.display.update()
            time.sleep(1)
            currentState = "end"

        clock.tick(fps)
    # end
    if currentState == "end":
        for event in pg.event.get():
            if event.type == KEYDOWN:
                currentState = "start"
        screen.blit(table, (0, 0))
        bas_font = pg.font.SysFont(None, 100)  # 150)
        text = bas_font.render("Вы проиграли!", True, "black")
        c = time_count
        time_text = text_phrase.render("Ваш счет: " + str(int((round(c / fps, 2))) * win), True, "black")
        esc_text = text_phrase.render("Нажмите, чтобы продолжить.", True, "black")
        best.append(round((c / fps) * win))
        best = list(set(best))
        best.append(0)
        best.sort(reverse=True)
        best = best[:3]
        lines = open(os.path.join('data', 'результат игры.txt')).read().splitlines()
        ch = text_phrase.render(f"Рекорд: {lines[0].split()[1]}", True, "black")
        screen.blit(text, (50, 100))
        screen.blit(ch, (75, 400))
        screen.blit(time_text, (75, 300))
        screen.blit(esc_text, (40, 500))
        pg.display.update()
        if int((round(c / fps, 2))) * win > int(lines[0].split()[1]):
            f = open(os.path.join('data', 'результат игры.txt'), 'w')
            f.write(f"Рекорд: {int((round(c / fps, 2))) * win}")
            f.close()
    # exit
    if currentState == "exit":
        break
pg.quit()
