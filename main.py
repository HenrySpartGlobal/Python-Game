import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cat Adventure")

# frame rate
clock = pygame.time.Clock()
fps = 60

# player action variables
moving_left = False
moving_right = False

# colours
BG = (144, 201, 120)


def draw_bg():
    screen.fill(BG)


class Cat(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(18):
            img = pygame.image.load(f'img/{self.char_type}/idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, left, right):
        # movement vars delta
        dx = 0
        dy = 0

        # movement var for left or right
        if left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # move rect pos
        self.rect.x += dx
        self.rect.y += dy

    def update_anim(self):
        # update time
        ANIMATION_COOLDOWN = 100
        # update image depending on frame
        self.image = self.animation_list[self.frame_index]
        # check when last update was
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # loop animation back to start
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player = Cat('rell', 200, 200, 2, 5)

# todo change animation loop for cat
enemy = Cat('rell', 300, 200, 2, 5)
running = True
new_time, old_time = None, None

while running:

    clock.tick(fps)
    draw_bg()

    player.update_anim()
    player.draw()
    enemy.draw()

    player.move(moving_left, moving_right)

    for event in pygame.event.get():
        # quits the game
        if event.type == pygame.QUIT:
            running = False
        # controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                running = False

        # button let go
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    # display fps and milliseconds
    if new_time:
        old_time = new_time
    new_time = pygame.time.get_ticks()
    if new_time and old_time:
        pygame.display.set_caption("FPS " + (str(int(clock.get_fps())) + " ms: " + str(new_time - old_time)))

        pygame.display.update()

pygame.quit()
