import pygame
import random
from pygame import mixer

pygame.init()

SCRN_HEIGHT = 600
SCRN_WIDTH = 1100
global GAME_SPEED
GAME_SPEED = 14
SCREEN = pygame.display.set_mode((SCRN_WIDTH, SCRN_HEIGHT))

RUNNING = [pygame.image.load("Assets/Dino/DinoRun1.png"),
           pygame.image.load("Assets/Dino/DinoRun2.png")]

JUMPING = pygame.image.load("Assets/Dino/DinoJump.png")

DUCKING = [pygame.image.load("Assets/Dino/DinoDuck1.png"),
           pygame.image.load("Assets/Dino/DinoDuck2.png")]

LARGE_TREE = [pygame.image.load("Assets/Cactus/LargeCactus1.png"),
              pygame.image.load("Assets/Cactus/LargeCactus2.png"),
             ]

SMALL_TREE = [pygame.image.load("Assets/Cactus/SmallCactus1.png"),
              pygame.image.load("Assets/Cactus/SmallCactus2.png"),
              ]

BIRD = [pygame.image.load("Assets/Bird/Bird1.png"),
        pygame.image.load("Assets/Bird/Bird2.png")]

CLOUD = pygame.image.load("Assets/Other/Cloud.png")

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


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCRN_WIDTH

    def updateObstacle(self):
        self.rect.x -= GAME_SPEED
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCRN):
        SCRN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice([250, 300])
        self.step_index = 0  # For animation

    def updateObstacle(self):
        super().updateObstacle()
        self.step_index += 1
        if self.step_index >= 20:  # Reset step index for smooth animation
            self.step_index = 0

    def draw(self, SCRN):
        # Alternate between the two bird images for animation
        if self.step_index < 10:
            self.image = BIRD[0]
        else:
            self.image = BIRD[1]
        SCRN.blit(self.image, self.rect)


def displayScore(SCRN, points):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render(f"Score: {points}", True, (0, 0, 0))
    SCRN.blit(text, (950, 50))


def showGameOverScreen(SCRN, points):
    font = pygame.font.Font('freesansbold.ttf', 30)
    game_over_text = font.render("Game Over", True, (0, 0, 0))
    score_text = font.render(f"Your Score: {points}", True, (0, 0, 0))
    restart_text = font.render("Press R to Restart", True, (0, 0, 0))

    global GAME_SPEED
    GAME_SPEED = 14 # reset the game speed

    SCRN.fill((255, 255, 255))
    SCRN.blit(game_over_text, (SCRN_WIDTH // 2 - game_over_text.get_width() // 2, SCRN_HEIGHT // 2 - 50))
    SCRN.blit(score_text, (SCRN_WIDTH // 2 - score_text.get_width() // 2, SCRN_HEIGHT // 2))
    SCRN.blit(restart_text, (SCRN_WIDTH // 2 - restart_text.get_width() // 2, SCRN_HEIGHT // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False  # Exit the waiting loop to restart the game


def dino_game():
    while True:  # Add a loop to allow restarting the game
        run = True
        clock = pygame.time.Clock()

        player = Dino()
        cloud = Cloud()
        background = Background()

        global obstacles
        obstacles = []

        points = 0

        playMusic()

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            SCREEN.fill((255, 255, 255))
            userInput = pygame.key.get_pressed()

            # Update and draw player
            player.draw(SCREEN)
            player.updatePlayer(userInput)

            # Update and draw cloud
            cloud.draw(SCREEN)
            cloud.updateCloud()

            # Update and draw background
            background.drawBG(SCREEN)
            background.updateBG()

            # Spawn obstacles
            if len(obstacles) == 0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_TREE))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_TREE))
                else:
                    obstacles.append(Bird(BIRD))

            # Update and draw obstacles
            for obstacle in obstacles:
                obstacle.draw(SCREEN)
                obstacle.updateObstacle()

                # Check for collision
                if player.dino_rect.colliderect(obstacle.rect):
                    # pygame.time.delay(500)
                    showGameOverScreen(SCREEN, points)
                    run = False  # Exit the game loop to restart
                    break

            # Display score
            points += 1
            if points % 200 == 0:
                global GAME_SPEED
                GAME_SPEED += 1
            displayScore(SCREEN, points)

            clock.tick(60)
            pygame.display.flip()

dino_game()