import pygame
import os
from PIL import Image

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Rells Adventure')

# set frame rate
clock = pygame.time.Clock()
FPS = 144

# define game variables
GRAVITY = 0.4

# define Rell action variables
moving_left = False
moving_right = False
shoot = False

# load assets
arrow_img = pygame.transform.scale(pygame.image.load('img/assets/arrow_1.png'), (40, 40)).convert_alpha()

# define colours
BG = (144, 201, 120)
RED = (255, 0, 0)


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


class Rell(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.attack = False
        self.melee = False
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the players (folders)
        animation_types = ['Idle', 'Run', 'Jump', 'Attack', 'Melee']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        # reset movement vars
        dx = 0
        dy = 0

        # assign movement vars if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # stop the player moving whilst attacking
        if player.attack:
            dx = self.speed % 4.5
        if player.melee:
            dx = self.speed % 4.5

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100

        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]

        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # if the animation has finished then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is unique
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = arrow_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction


# sprite groups
arrow_group = pygame.sprite.Group()

player = Rell('Rell', 200, 245, 3, 5)
enemy = Rell('enemy', 400, 245, 3, 5)
cat = Rell('cat', 220, 250, 3, 5)

running = True
while running:

    clock.tick(FPS)

    draw_bg()

    player.update_animation()
    player.draw()
    cat.draw()
    enemy.draw()

    # update and draw groups
    arrow_group.update()
    arrow_group.draw(screen)

    # update Rell actions
    if player.alive:
        if player.melee:
            player.update_action(4)  # 4: melee
        elif player.attack:
            player.update_action(3)  # 3: attack
            arrow = Arrow(player.rect.centerx, player.rect.centery, player.direction)
            arrow_group.add(arrow)
        elif player.in_air:
            player.update_action(2)  # 2: jump
        elif moving_left or moving_right:
            player.update_action(1)  # 1: run
        else:
            player.update_action(0)  # 0: idle
        player.move(moving_left, moving_right)

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            running = False

        # mouse presses
        if event.type == pygame.MOUSEBUTTONDOWN and player.alive:
            if event.button == 1:
                player.attack = True
                shoot = True

        if event.type == pygame.MOUSEBUTTONDOWN and player.alive:
            if event.button == 3:
                player.melee = True

        # mouse released
        if event.type == pygame.MOUSEBUTTONUP and player.alive:
            if event.button == 1:
                player.attack = False
                shoot = False

        if event.type == pygame.MOUSEBUTTONUP and player.alive:
            if event.button == 3:
                player.melee = False

        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                running = False

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()
