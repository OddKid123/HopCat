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

# Generate coins randomly above the platforms
def generate_coins():
    for platform_rect in platform_rects[1:]:
        num_coins = random.randint(0, 3)
        for i in range(num_coins):
            coin_x = platform_rect.x + (platform_rect.width // (num_coins + 1)) * (i + 1)
            coin_y = platform_rect.y - 20
            coin = Coin(coin_x, coin_y)
            coins.add(coin)

generate_coins()

# Set up the score display
score = 0
score_font = pygame.font.Font(None, 36)

# game loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_velocity[1] = -player_jump_speed

    # handle gravity
    player_velocity[1] += gravity

    # handle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_velocity[0] = -player_speed
        facing_right = False
    elif keys[pygame.K_d]:
        player_velocity[0] = player_speed
        facing_right = True
    else:
        player_velocity[0] = 0

    # Move player and check for collisions with the screen edges
    player.rect.move_ip(player_velocity[0], player_velocity[1])

    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > WINDOW_WIDTH:
        player.rect.right = WINDOW_WIDTH
    if player.rect.top < 0:
        player.rect.top = 0
    if player.rect.bottom > WINDOW_HEIGHT:
        player.rect.bottom = WINDOW_HEIGHT

    # handle platform collision
    for platform_rect in platform_rects:
        if player.rect.colliderect(platform_rect) and player_velocity[1] > 0:
            player.rect.bottom = platform_rect.top
            player_velocity[1] = 0
            if platform_rect == platform_rects[0]:
                score = 0
            break

    # handle platform movement
    def regenerate_platform(platform_rect):
        platform_rect.left = WINDOW_WIDTH
        generate_coins_for_platform(platform_rect)

    def generate_coins_for_platform(platform_rect):
        num_coins = random.randint(0, 3)
        for i in range(num_coins):
            coin_x = platform_rect.x + (platform_rect.width // (num_coins + 1)) * (i + 1)
            coin_y = platform_rect.y - 20
            coin = Coin(coin_x, coin_y)
            coins.add(coin)

    for platform_rect in platform_rects[1:]:
        platform_rect.move_ip(-platform_speed, 0)
        if platform_rect.right < 0:
            regenerate_platform(platform_rect)

    # update coins
    coins.update()

    # Check for collisions between the player and coins, and increase the score if a coin is collected
    coins_collected = pygame.sprite.spritecollide(player, coins, True)
    score += len(coins_collected)

    # draw game objects
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, DARK_PINK, platform_rects[0])
    for platform_rect in platform_rects[1:]:
        pygame.draw.rect(screen, BROWN, platform_rect)

    # Draw the player image based on the facing_right variable
    if facing_right:
        screen.blit(player_image_flipped, player.rect.topleft)
    else:
        screen.blit(player_image, player.rect.topleft)

    # Draw the coins
    coins.draw(screen)

    # Draw the score in the upper left side of the screen
    score_text = score_font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # update display and tick clock
    pygame.display.update()
    clock.tick(60)

# quit pygame and exit program
pygame.quit()
exit()





