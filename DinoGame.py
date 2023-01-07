import pygame
import random
from pygame import mixer

pygame.init()

SCRN_HEIGHT = 600
SCRN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCRN_WIDTH, SCRN_HEIGHT))

RUNNING = [pygame.image.load("Assets/Dino/DinoRun1.png"),
           pygame.image.load("Assets/Dino/DinoRun2.png")]

JUMPING = pygame.image.load("Assets/Dino/DinoJump.png")

DUCKING = [pygame.image.load("Assets/Dino/DinoDuck1.png"),
           pygame.image.load("Assets/Dino/DinoDuck2.png")]

LARGE_TREE = [pygame.image.load("Assets/Cactus/LargeCactus1.png"),
              pygame.image.load("Assets/Cactus/LargeCactus2.png"),
              pygame.image.load("Assets/Cactus/LargeCactus3.png")]

SMALL_TREE = [pygame.image.load("Assets/Cactus/SmallCactus1.png"),
              pygame.image.load("Assets/Cactus/SmallCactus2.png"),
              pygame.image.load("Assets/Cactus/SmallCactus3.png")]

BIRD = [pygame.image.load("Assets/Bird/Bird1.png"),
        pygame.image.load("Assets/Bird/Bird2.png")]

CLOUD = pygame.image.load("Assets/Other/Cloud.png")
FIRE = pygame.image.load("Assets/Other/Fire.png")

BG = pygame.image.load("Assets/Other/Track.png")


class Dino:
    xPos = 80
    yPos = 310

    yPosDuck = 340

    JUMP_VELOCITY = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0  # for animation (to switch images)
        self.image = self.run_img[0]

        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.xPos
        self.dino_rect.y = self.yPos

        self.jump_velocity = self.JUMP_VELOCITY

    def updatePlayer(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 20:  # help animation
            self.step_index = 0

        if userInput[pygame.K_SPACE] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (userInput[pygame.K_DOWN] or self.dino_jump):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def run(self):
        if self.step_index >= 10:
            self.image = self.run_img[0]
        else:
            self.image = self.run_img[1]

        self.dino_rect = self.image.get_rect()

        self.dino_rect.x = self.xPos
        self.dino_rect.y = self.yPos

        self.step_index += 1

    def jump(self):
        self.image = self.jump_img

        if self.dino_jump:
            self.dino_rect.y -= self.jump_velocity * 4
            self.jump_velocity -= 0.8
        if self.jump_velocity < - self.JUMP_VELOCITY:
            self.dino_jump = False
            self.jump_velocity = self.JUMP_VELOCITY

    def duck(self):
        if self.step_index >= 10:
            self.image = self.duck_img[0]
        else:
            self.image = self.duck_img[1]

        self.dino_rect = self.image.get_rect()

        self.dino_rect.x = self.xPos
        self.dino_rect.y = self.yPosDuck

        self.step_index += 1

    def draw(self, SCRN):
        SCRN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCRN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def updateCloud(self):
        self.x -= GAME_SPEED

        if self.x < - self.width:
            # reset the cloud outside the screen
            self.x = SCRN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCRN):
        SCRN.blit(self.image, (self.x, self.y))


class Background:
    def __init__(self):
        self.x = 0
        self.y = 380
        self.image = BG
        self.bg_width = BG.get_width()

    def updateBG(self):
        self.x -= GAME_SPEED

        if self.x <= - self.bg_width:
            self.x = 0

    def drawBG(self, SCRN):
        SCRN.blit(self.image, (self.x, self.y))
        SCRN.blit(self.image, (self.bg_width + self.x, self.y))


def playMusic():
    mixer.init()

    mixer.music.load("Assets/Other/8bit_music.mp3")
    mixer.music.set_volume(1)
    mixer.music.play()


global GAME_SPEED
GAME_SPEED = 14


def dino_game():
    run = True
    clock = pygame.time.Clock()

    player = Dino()
    cloud = Cloud()
    background = Background()

    playMusic()

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.updatePlayer(userInput)

        cloud.draw(SCREEN)
        cloud.updateCloud()

        background.drawBG(SCREEN)
        background.updateBG()

        clock.tick(60)
        # print(clock.get_fps())
        pygame.display.flip()


dino_game()
