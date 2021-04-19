import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cat Adventure")
x = 200
y = 200
scale = 0.3

img = pygame.image.load('img/cat/idle/mario.png')
img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
rect = img.get_rect()
rect.center = (x, y)


running = True

while running:

    screen.blit(img, rect)

    for event in pygame.event.get():
        # quits the game
        if event.type == pygame.QUIT:
            running = False

        pygame.display.update()


pygame.quit()