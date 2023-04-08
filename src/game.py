import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the display
display_width = 800
display_height = 600
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("My Game")

# Load the background image
background_image = pygame.image.load(os.path.join(os.path.dirname(__file__), "images", "background.png")).convert()

# Set up the floor
floor_color = (233, 120, 145)
floor_rect = pygame.Rect(0, display_height - 50, display_width, 50)

# Set up the platforms
platform_color = (139, 69, 19)
platforms = [
    pygame.Rect(0, display_height - 150, 200, 20),
    pygame.Rect(300, display_height - 250, 200, 20),
    pygame.Rect(500, display_height - 350, 200, 20)
]

# Set up the rectangle
rect_width = 50
rect_height = 50
rect_x = display_width // 2
rect_y = display_height // 2
rect_speed = 300
rect_color = (255, 0, 0)
my_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
my_rect_speed_y = 0

# Set up gravity
gravity = 500

# Set up the clock
clock = pygame.time.Clock()

# Main game loop
game_running = True
while game_running:

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        my_rect.x -= rect_speed * clock.get_time() / 1000
    elif keys[pygame.K_d]:
        my_rect.x += rect_speed * clock.get_time() / 1000

    # Jumping
    if keys[pygame.K_SPACE] and my_rect.bottom >= floor_rect.top:
        my_rect_speed_y = -600

    # Apply gravity
    my_rect_speed_y += gravity * clock.get_time() / 1000
    my_rect.y += my_rect_speed_y * clock.get_time() / 1000

    # Check for collision with the floor
    if my_rect.bottom > floor_rect.top:
        my_rect.bottom = floor_rect.top
        my_rect_speed_y = 0

    # Check for collision with the platforms
    for platform in platforms:
        if my_rect.colliderect(platform):
            if my_rect_speed_y > 0:
                my_rect.bottom = platform.top
                my_rect_speed_y = 0
            elif my_rect_speed_y < 0:
                my_rect.top = platform.bottom
                my_rect_speed_y = 0

    # Drawing
    game_display.blit(background_image, (0, 0))
    pygame.draw.rect(game_display, floor_color, floor_rect)
    for platform in platforms:
        pygame.draw.rect(game_display, platform_color, platform)
    pygame.draw.rect(game_display, rect_color, my_rect)
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Clean up
pygame.quit()
