import os
import pygame
import random

# Set up the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Set up the Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= platform_speed

# set up game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "My Game"
pygame.init()
print("Pygame initialized.")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_PINK = (200, 20, 100)
BROWN = (139, 69, 19)

# set up clock
clock = pygame.time.Clock()

# set up player properties
player_size = 50
player_x = WINDOW_WIDTH // 2 - player_size // 2
player_y = WINDOW_HEIGHT - player_size - 50
player_speed = 5
player_jump_speed = 12

player_velocity = [0, 0]

# load player image
player_image = pygame.image.load(os.path.join("src", "images", "player.png"))

# scale player image
image_height = 50
image_width = int(player_image.get_width() * (image_height / player_image.get_height()))
player_image = pygame.transform.scale(player_image, (image_width, image_height))

# create flipped player image
player_image_flipped = pygame.transform.flip(player_image, True, False)

# create player instance
player = Player(player_x, player_y, player_image)

# set up direction variable
facing_right = False

# set up platform properties
platform_width = 100
platform_height = 20
platform_speed = 2
platform_rects = [
    pygame.Rect(0, WINDOW_HEIGHT - platform_height, WINDOW_WIDTH, platform_height),
    pygame.Rect(300, 450, platform_width, platform_height),
    pygame.Rect(450, 350, platform_width, platform_height),
    pygame.Rect(200, 250, platform_width, platform_height),
    pygame.Rect(600, 150, platform_width, platform_height),
]

# set up gravity properties
gravity = 0.5
jumping = False
jump_counter = 0

# load background image
background_image = pygame.image.load(os.path.join("src", "images", "background.png")).convert()

# Set up the list for coins
coins = pygame.sprite.Group()

# Set up the score display
score = 0
high_score = 0
score_font = pygame.font.Font(None, 36)

def draw_score():
    score_text = score_font.render("Score: " + str(score), True, WHITE)
    high_score_text = score_font.render("High Score: " + str(high_score), True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (WINDOW_WIDTH - 250, 10))

# Generate coins randomly above the platforms
def generate_coins(platform_rects):
    for platform_rect in platform_rects:
        num_coins = random.randint(0, 3)
        for i in range(num_coins):
            coin_x = platform_rect.x + (platform_rect.width // (num_coins + 1)) * (i + 1)
            coin_y = platform_rect.y - 20
            coin = Coin(coin_x, coin_y)
            coins.add(coin)

generate_coins(platform_rects)

# main game loop
running = True
while running:
    screen.fill(BLACK)
    screen.blit(background_image, (0, 0))

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # player movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player_velocity[0] = -player_speed
        facing_right = False
    elif keys[pygame.K_d]:
        player_velocity[0] = player_speed
        facing_right = True
    else:
        player_velocity[0] = 0

    if keys[pygame.K_SPACE]:
        player_velocity[1] = -player_jump_speed

    player.rect.x += player_velocity[0]
    player.rect.y += player_velocity[1]

    # gravity
    player_velocity[1] += gravity

    # handle platform collision and reset score if player touches the ground
    for index, platform_rect in enumerate(platform_rects):
        if player.rect.colliderect(platform_rect) and player_velocity[1] > 0:
            player.rect.bottom = platform_rect.top
            player_velocity[1] = 0
            if index == 0:
                score = 0
            break


    # handle platform movement
    for platform_rect in platform_rects[1:]:
        platform_rect.x -= platform_speed
        if platform_rect.right < 0:
            platform_rect.left = WINDOW_WIDTH
            generate_coins([platform_rect])  # Generate coins for the new platform

    # update coins
    coins.update()

    # collision detection for coins
    for coin in coins:
        if player.rect.colliderect(coin.rect):
            score += 1
            if score > high_score:
                high_score = score
            coins.remove(coin)

   # check if player touches the ground and reset the score
    if player.rect.colliderect(platform_rects[0]) and player_velocity[1] >= 0:
        score = 0


    # draw platforms
    for platform_rect in platform_rects:
        pygame.draw.rect(screen, BROWN, platform_rect)

    # draw player
    if facing_right:
        screen.blit(player_image, (player.rect.x, player.rect.y))
    else:
        screen.blit(player_image_flipped, (player.rect.x, player.rect.y))

    # draw coins
    coins.draw(screen)

    # draw score
    draw_score()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
