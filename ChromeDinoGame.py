import pygame

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def dinoGame():
    color = (94, 186, 125)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Welcome To GameJam Workshop!', True, color, None)

    textRect = text.get_rect()

    # set the center of the rectangular object.
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    run = True
    clock = pygame.time.Clock()

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.blit(text, textRect)

        clock.tick(60)
        pygame.display.set_caption('Chrome Dino')
        pygame.display.flip()


dinoGame()
