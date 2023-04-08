import os
import pygame

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
player_jump_height = 200
player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

# set up platform properties
platform_width = 100
platform_height = 20
platform_speed = 1
platform_rects = [
    pygame.Rect(0, WINDOW_HEIGHT - platform_height, WINDOW_WIDTH, platform_height),
    pygame.Rect(300, 450, platform_width, platform_height),
    pygame.Rect(450, 350, platform_width, platform_height),
    pygame.Rect(200, 250, platform_width, platform_height),
]

# set up gravity properties
gravity = 0.5
jumping = False
jump_counter = 0

# load background image
background_image = pygame.image.load(os.path.join("src", "images", "background.png")).convert()

# game loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping:
                jumping = True
                jump_counter = 0


    # Player movement
    player_y_change = 0

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            # Set player_y_change to a positive value to simulate gravity pulling the player down
            player_y_change = 8
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
            # Gradually decrease player_y_change to slow down player's upward motion and reverse direction
            for i in range(player_y_change):
                player_y_change -= 1

    player_y += player_y_change

    # handle jumping
    if jumping:
        player_rect.move_ip(0, -player_jump_speed)
        jump_counter += player_jump_speed
        if jump_counter >= player_jump_height:
            jumping = False

    # handle gravity
    if not jumping:
        player_rect.move_ip(0, gravity)
        for platform_rect in platform_rects:
            if player_rect.colliderect(platform_rect):
                if gravity > 0:
                    player_rect.bottom = platform_rect.top
                    jumping = False
                else:
                    player_rect.top = platform_rect.bottom
                break

    # handle platform movement
    for platform_rect in platform_rects[1:]:
        platform_rect.move_ip(-platform_speed, 0)
        if platform_rect.right < 0:
            platform_rect.left = WINDOW_WIDTH

    # draw game objects
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, DARK_PINK, platform_rects[0])
    for platform_rect in platform_rects[1:]:
        pygame.draw.rect(screen, BROWN, platform_rect)
    pygame.draw.rect(screen, WHITE, player_rect)

    # handle jumping
    if jumping:
        player_rect.move_ip(0, -player_jump_speed)
        jump_counter += player_jump_speed
        if jump_counter >= player_jump_height:
            jumping = False

    # handle gravity
    if not jumping:
        player_rect.move_ip(0, gravity)
        on_platform = False
        for platform_rect in platform_rects:
            if player_rect.colliderect(platform_rect):
                on_platform = True
                if gravity > 0:
                    player_rect.bottom = platform_rect.top
                else:
                    player_rect.top = platform_rect.bottom
                break

        if not on_platform:
            gravity += 0.5
        else:
            gravity = 0.5

    # handle platform movement
    for platform_rect in platform_rects[1:]:
        platform_rect.move_ip(-platform_speed, 0)
        if platform_rect.right < 0:
            platform_rect.left = WINDOW_WIDTH

    # draw game objects
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, DARK_PINK, platform_rects[0])
    for platform_rect in platform_rects[1:]:
        pygame.draw.rect(screen, BROWN, platform_rect)
    pygame.draw.rect(screen, WHITE, player_rect)

    # update display and tick clock
    pygame.display.update()
    clock.tick(60)

# quit pygame and exit program
pygame.quit()
exit()
