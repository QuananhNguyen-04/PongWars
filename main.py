import pygame
import random
from pygame.locals import *
import time

pygame.init()
size = (1000, 600)
resolution = (800, 600)
white = (255, 255, 255)
black = (0, 0, 0)
nearwhite = (200, 200, 200)
nearblack = (50, 50, 50)
red = (255, 0, 0)

screen = pygame.display.set_mode(size)
log = (resolution[0], size[0])
screen.fill(nearwhite)
start_time = time.time()
Endgame = False
Midgame = False
block_width = 30
block_height = 30
blocks = []
white_points = 0.0
black_points = 0.0


def reset():
    # only max 8 events can be defined by user
    global \
        gameObjects, \
        timerEventP1, \
        timerEventP2, \
        boostP1, \
        boostP2, \
        points, \
        money, \
        start_time, \
        Endgame, \
        Midgame, \
        white_points, \
        black_points
    start_time = time.time()
    Endgame = False
    Midgame = False
    white_points = 0
    black_points = 0
    gameObjects = [Ball(nearwhite), Ball(nearblack)]
    timerEventP1 = pygame.USEREVENT + 0
    timerEventP2 = pygame.USEREVENT + 1
    boostP1 = pygame.USEREVENT + 2
    boostP2 = pygame.USEREVENT + 3
    points = pygame.USEREVENT + 4
    money = pygame.USEREVENT + 5
    pygame.time.set_timer(money, 0)
    pygame.time.set_timer(points, 0)
    pygame.time.set_timer(money, 1000)
    pygame.time.set_timer(points, 1000)
    if len(blocks) == 0:
        for y in range(0, resolution[1], block_height):
            for x in range(0, resolution[0], block_width):
                if x < resolution[0] / 2:
                    blocks.append(Block(x, y, block_width, block_height, white))
                else:
                    blocks.append(Block(x, y, block_width, block_height, black))
    else:
        for block in blocks:
            if block.x < resolution[0] / 2:
                block.color = white
            else:
                block.color = black
    for block in blocks:
        block.draw(screen)
    for obj in gameObjects:
        obj.draw(screen)
    pygame.display.flip()
    print(white_points, black_points)
    calcState(blocks)


class Block:
    def __init__(self, xPos, yPos, width, height, color):
        self.x = xPos
        self.y = yPos
        self.width = width
        self.height = height
        self.color = color
        self.type = "block"

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height)
        )


class Ball:
    def __init__(
        self,
        color,
        xPos=resolution[0] / 2,
        yPos=resolution[1] / 2,
        xVel=2.1,
        yVel=2.1,
        rad=20,
        money=20,
    ):
        self.id = 1 if color == nearblack else 2
        self.x = xPos - xPos / 2 if self.id == 1 else xPos + xPos / 2
        self.y = yPos
        self.dx = (random.randint(0, 1) - 0.5) * 2 * xVel
        self.dy = (random.randint(0, 1) - 0.5) * 2 * yVel
        print(self.dx, self.dy)
        self.radius = rad
        self.type = "ball"
        self.color = color
        self.money = 20

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius, 5)

    def collide(self, gameObjects):
        for obj in gameObjects:
            if obj.type == "block" and (
                (obj.color == black and self.color == nearblack)
                or (obj.color == white and self.color == nearwhite)
            ):
                distX = abs(self.x - obj.x - obj.width / 2)
                distY = abs(self.y - obj.y - obj.height / 2)

                if (distX > (obj.width / 2 + self.radius)) or (
                    distY > (obj.height / 2 + self.radius)
                ):
                    continue
                
                if (distX <= (obj.width / 2)) and (distY <= (obj.height / 2)):
                    self.dx *= -1
                    self.dy *= -1
                    angle_change_rate = 0.05
                    if random.random() < angle_change_rate:
                        self.dx, self.dy = self.dy, self.dx
                    obj.color = white if self.color == nearblack else black
                    return
                if (distX <= (obj.width / 2)):
                    self.dx *= -1
                    obj.color = white if self.color == nearblack else black
                    return
                if (distY <= (obj.height / 2)):
                    self.dy *= -1
                    obj.color = white if self.color == nearblack else black
                    return

                cornerDistance_sq = (distX - obj.width / 2) ** 2 + (
                    distY - obj.height / 2
                ) ** 2

                if cornerDistance_sq <= (self.radius**2):
                    self.dx *= -1
                    self.dy *= -1
                    obj.color = white if self.color == nearblack else black

            if obj.type == "ball" and obj.id != self.id:
                distX = abs(self.x - obj.x - obj.radius / 2)
                distY = abs(self.y - obj.y - obj.radius / 2)

                cornerDistance_sq = (
                    (distX - obj.radius / 2) ** 2 + (distY - obj.radius / 2) ** 2
                ) ** (0.50)
                if cornerDistance_sq in range(self.radius * 1 + 1, self.radius * 2 + 5):
                    if (obj.x - self.x) > 0:
                        if obj.x + obj.radius <= resolution[0] - 5:
                            obj.x += obj.radius
                        if self.x - self.radius >= 5:
                            self.x -= self.radius
                    else:
                        if self.x + self.radius <= resolution[0] - 5:
                            self.x += self.radius
                        if obj.x - obj.radius >= 5:
                            obj.x -= obj.radius

                    if (obj.y - self.y) > 0:
                        if obj.y + obj.radius <= resolution[1] - 5:
                            obj.y += obj.radius
                        if self.y - self.radius >= 5:
                            self.y -= self.radius
                    else:
                        if self.y + self.radius <= resolution[1] - 5:
                            self.y += self.radius
                        if obj.y - obj.radius >= 5:
                            obj.y -= obj.radius

                    self.dx *= -1
                    self.dy *= -1
                    obj.dx *= -1
                    obj.dy *= -1
                    print(cornerDistance_sq)
                    return
                if cornerDistance_sq < (self.radius * 1):
                    if (obj.x - self.x) > 0:  # self is on lhs, obj on rhs
                        if obj.x + 2 * obj.radius <= resolution[0] - 5:
                            obj.x += 2 * obj.radius
                        else:
                            obj.x += int(obj.radius * 0.5)
                        if self.x - 2 * self.radius >= 5:
                            self.x -= 2 * self.radius
                        else:
                            self.x -= int(self.radius * 0.5)
                    else:
                        if self.x + self.radius <= resolution[0] - 5:
                            self.x += self.radius
                        else:
                            self.x += int(self.radius * 0.5)
                        if obj.x - obj.radius >= 5:
                            obj.x -= obj.radius
                        else:
                            obj.x -= int(obj.radius * 0.5)
                    if (obj.y - self.y) > 0:
                        if obj.y + obj.radius <= resolution[1] - 5:
                            obj.y += obj.radius
                        if self.y - self.radius >= 5:
                            self.y -= self.radius
                    else:
                        if self.y + self.radius <= resolution[1] - 5:
                            self.y += self.radius
                        if obj.y - obj.radius >= 5:
                            obj.y -= obj.radius

                    self.dx *= -1
                    self.dy *= -1
                    obj.dx *= -1
                    obj.dy *= -1

                    print("+++++++++++++++++++")
                return

    def update(self, gameObjects):
        self.collide(gameObjects)
        rate = 0.01
        choose = random.randint(0, 1)
        bonus_velocity = 1.0005 if random.random() > rate else 0.99

        if Endgame:
            rate = 0.1
            bonus_velocity = 1.01 if random.random() > rate else 0.9999
        self.x += self.dx
        self.y += self.dy
        if random.random() < rate:
            if choose == 0:
                self.dx *= bonus_velocity
                self.dx = min(self.dx, 20) if self.dx > 0 else max(self.dx, -20)
            else:
                self.dy *= bonus_velocity
                self.dy = min(self.dy, 20) if self.dy > 0 else max(self.dy, -20)
        self.velocity = round((self.dx**2 + self.dy**2) ** (0.5), 1)
        # prevent get stuck on edges when having high speed
        if (
            self.x <= self.radius - self.dx
            or self.x + self.dx >= resolution[0] - self.radius - 1
        ):
            self.dx *= -1
        if (
            self.y <= self.radius - self.dy
            or self.y + self.dy >= resolution[1] - self.radius - 1
        ):
            self.dy *= -1
        self.collide(blocks)

    def speedUp(self):
        if Endgame:
            self.dx *= 3
            self.dy *= 3 
        else:
            self.dx *= 1.5
            self.dy *= 1.5

    def resetSpeed(self):
        if Endgame:
            self.dx = self.dx / 2.7 if self.dx > 7 else self.dx
            self.dy = self.dy / 2.7 if self.dy > 7 else self.dy
        else:
            self.dx = self.dx / 1.3 if self.dx > 3 else self.dx
            self.dy = self.dy / 1.3 if self.dy > 3 else self.dy
        print(f"Player {self.id} velocity: {(self.dx**2 + self.dy**2)**(1.0/2.0)}")

    def addMoney(self):
        if not Midgame:
            self.money += 1
        else:
            self.money += 2

    def penalty(self):
        if not Endgame:
            self.money -= 10
        else:
            self.money -= 50
        if self.money < 0:
            self.money = 0

    def spendMoney(self):
        if not Midgame:
            if self.money >= 10:
                self.money -= 10
                return True
            return False
        if self.money >= 20:
            self.money -= 20
            return True
        return False
    
    def attack(self):
        if not Endgame:
            return False
        if (self.money < 100):
            return False
        self.money -= 100
        return True
    def nerfSpeed(self):
        self.dx /= 2
        self.dy /= 2


def draw_percent_bar(
    screen,
    position,
    size=(80, 30),
    percent=100,
    bar_color=(0, 255, 0),
    bg_color=(255, 255, 255),
):
    """
    Draw a percentage bar on a Pygame screen.

    Parameters:
    - screen: Pygame surface where the bar will be drawn.
    - position: A tuple (x, y) representing the top left corner of the bar.
    - size: A tuple (width, height) representing the size of the bar.
    - percent: The percentage to be represented by the bar. Should be between 0 and 100.
    - bar_color: A tuple (r, g, b) representing the color of the bar. Default is green.
    - bg_color: A tuple (r, g, b) representing the color of the background. Default is white.
    """
    percent = min(percent, 100)
    pygame.draw.rect(
        screen, bg_color, (*position, *size)
    )  # Draw the background of the bar
    pygame.draw.rect(
        screen, bar_color, (*position, size[0] * percent / 100, size[1])
    )  # Draw the bar


def drawBoard(screen, dtime, tme):
    font30 = pygame.font.SysFont("timesnewroman", 30)
    font20 = pygame.font.SysFont("timesnewroman", 20)

    pygame.draw.rect(
        screen, nearwhite, pygame.Rect(resolution[0], 0, 200, resolution[1])
    )
    # screen.fill(nearwhite)
    txt = "" + str(int(white_points)) + " VS " + str(int(black_points))
    state_text = font30.render(txt, True, black, nearwhite)
    state_rect = state_text.get_rect()
    state_rect.center = (resolution[0], 100)
    state_rect.x = resolution[0] + 5
    # print(dtime[0], dtime[1])
    # print(tme)
    draw_percent_bar(screen, (resolution[0] + 5, 300), (80, 30), dtime[0] / tme * 100)
    draw_percent_bar(screen, (resolution[0] + 5, 400), (80, 30), dtime[1] / tme * 100)
    screen.blit(state_text, state_rect)
    p1 = None
    p2 = None
    for obj in gameObjects:
        if obj.id == 1:
            p1 = (obj.money, obj.velocity)
        if obj.id == 2:
            p2 = (obj.money, obj.velocity)
    p1_vel = font20.render(f"P1. Velocity: {p1[1]}", True, (200, 0, 0), white)
    p1_money = font20.render(f"Money: {p1[0]}", True, white, nearwhite)
    p2_vel = font20.render(f"P2. Velocity: {p2[1]}", True, (200, 0, 0), white)
    p2_money = font20.render(f"Money: {p2[0]}", True, white, nearwhite)

    p1_vel_rect = p1_vel.get_rect()
    p1_vel_rect.y = 250
    p1_vel_rect.x = resolution[0] + 5
    p1_money_rect = p1_money.get_rect()
    p1_money_rect.y = 300
    p1_money_rect.x = resolution[0] + 95
    screen.blit(p1_vel, p1_vel_rect)
    screen.blit(p1_money, p1_money_rect)

    p2_vel_rect = p1_vel.get_rect()
    p2_vel_rect.y = 350
    p2_vel_rect.x = resolution[0] + 5
    p2_money_rect = p1_money.get_rect()
    p2_money_rect.y = 400
    p2_money_rect.x = resolution[0] + 95
    screen.blit(p2_vel, p2_vel_rect)
    screen.blit(p2_money, p2_money_rect)


def calcState(blocks):
    total = resolution[0] * resolution[1] / block_width / block_height
    white_blocks = 0
    for block in blocks:
        if block.type == "block" and block.color == white:
            white_blocks += 1
    global white_points, black_points
    
    white_points = round(white_blocks / total, 2) * 100
    black_points = 100.0 - white_points

    death_line = 20 if not Endgame else 35
    # print(white_points, black_points)
    if white_points <= death_line or black_points <= death_line:
        return True
    # for obj in gameObjects:
    #     print(obj.money)
    return False


def run():
    clk = pygame.time.Clock()
    running = True
    canBoostP1 = True
    canBoostP2 = True
    start_p1 = 0
    start_p2 = 0
    p1 = time.time()
    p2 = time.time()
    while running:
        global Endgame
        global Midgame
        tme = 10000 if not Midgame else 5000
        now = time.time()

        if now - start_time > 40:
            Midgame = True
        if now - start_time > 100:
            Endgame = True
        for block in blocks:
            block.draw(screen)
        for gameObj in gameObjects:
            gameObj.update(gameObjects)

        for event in (
            pygame.event.get()
        ):  # call pygame.event.get() once cause it will clear all other events
            if event.type == pygame.QUIT:
                return
            key = pygame.key.get_pressed()

            if event.type == points:
                if calcState(blocks):
                    running = False
                print("current time", now - start_time)

            if key[pygame.K_ESCAPE]:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if not canBoostP1:
                        for obj in gameObjects:
                            if obj.id == 1:
                                obj.penalty()
                                break
                        continue
                    for obj in gameObjects:
                        if obj.id == 1:
                            if obj.velocity > 30:
                                break
                            if not obj.spendMoney():
                                break
                            obj.speedUp()
                            print("p1 speedup")
                            pygame.time.set_timer(
                                timerEventP1, 2000 if not Endgame else 4000
                            )
                            canBoostP1 = False
                            pygame.time.set_timer(boostP1, tme)
                            start_p1 = time.time()
                            end_p1 = start_p1 + tme

                elif event.key == pygame.K_UP:
                    if not canBoostP2:
                        for obj in gameObjects:
                            if obj.id == 2:
                                obj.penalty()
                                break
                        continue
                    for obj in gameObjects:
                        if obj.id == 2:
                            if obj.velocity > 30:
                                break
                            if not obj.spendMoney():
                                break
                            obj.speedUp()
                            print("p2 speedup")
                            pygame.time.set_timer(
                                timerEventP2, 2000 if not Endgame else 4000
                            )
                            canBoostP2 = False
                            pygame.time.set_timer(boostP2, tme)
                            start_p2 = time.time()
                            end_p2 = start_p2 + tme
                elif event.key == pygame.K_s:
                    pass
            elif event.type == timerEventP1:
                for obj in gameObjects:
                    if obj.id == 1:
                        obj.resetSpeed()
                        print("p1 slowdown")
                        pygame.time.set_timer(timerEventP1, 0)  # disable timer
                        break

            elif event.type == timerEventP2:
                for obj in gameObjects:
                    if obj.id == 2:
                        obj.resetSpeed()
                        print("p2 slowdown")
                        pygame.time.set_timer(timerEventP2, 0)  # disable timer
                        break

            if event.type == boostP1:
                canBoostP1 = True
                pygame.time.set_timer(boostP1, 0)

            if event.type == boostP2:
                canBoostP2 = True
                pygame.time.set_timer(boostP2, 0)

            if event.type == money:
                for obj in gameObjects:
                    obj.addMoney()

        p1 = min(time.time(), end_p1) if start_p1 != 0 else 100
        p2 = min(time.time(), end_p2) if start_p2 != 0 else 100
        drawBoard(screen, (p1 - start_p1, p2 - start_p2), tme / 1000)
        for gameObj in gameObjects:
            gameObj.draw(screen)
        clk.tick(100)
        pygame.display.flip()

    while not running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                return

            if key[pygame.K_r]:
                reset()
                run()
                return


# only max 8 events can be defined by user
gameObjects = [Ball(nearwhite), Ball(nearblack)]
timerEventP1 = pygame.USEREVENT + 0
timerEventP2 = pygame.USEREVENT + 1
boostP1 = pygame.USEREVENT + 2
boostP2 = pygame.USEREVENT + 3
attackP1 = pygame.USEREVENT + 4
attackP2 = pygame.USEREVENT + 5
points = pygame.USEREVENT + 6
money = pygame.USEREVENT + 7

reset()
run()
pygame.quit()
