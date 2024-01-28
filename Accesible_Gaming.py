import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Create the game screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Advanced Space Shooter")

# Set up clock for controlling the frame rate
clock = pygame.time.Clock()

# Load images
player_img = pygame.image.load("spaceship.png.png")
enemy_img = pygame.image.load("enemy.png")
powerup_img = pygame.image.load("powerup.png")

# Scale images
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
powerup_img = pygame.transform.scale(powerup_img, (30, 30))

# Define a Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)
        self.speed = 8

    def update(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width

# Define an Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 50)
        self.rect.y = random.randint(-50, 0)
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - 50)
            self.rect.y = random.randint(-50, 0)
            self.speed = random.randint(2, 5)

# Define a Powerup class
class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = powerup_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 30)
        self.rect.y = random.randint(-50, 0)
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - 30)
            self.rect.y = random.randint(-50, 0)
            self.speed = random.randint(2, 5)

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Create a player instance
player = Player()

# Add player to the sprite group
all_sprites.add(player)

# Main game loop
score = 0
game_over = False

while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Get input from the user
    keys = pygame.key.get_pressed()

    # Update player position based on input
    dx = 0
    if keys[pygame.K_LEFT]:
        dx = -player.speed
    if keys[pygame.K_RIGHT]:
        dx = player.speed

    # Update the player sprite
    player.update(dx)

    # Spawn enemies and power-ups
    if random.randint(1, 100) < 3:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    if random.randint(1, 100) < 1:
        powerup = Powerup()
        all_sprites.add(powerup)
        powerups.add(powerup)

    # Update enemies and power-ups
    enemies.update()
    powerups.update()

    # Check for collisions with enemies
    collisions = pygame.sprite.spritecollide(player, enemies, False)
    if collisions:
        print("Game Over! Your score:", score)
        game_over = True

    # Check for collisions with power-ups
    powerup_collisions = pygame.sprite.spritecollide(player, powerups, True)
    if powerup_collisions:
        score += 10

    # Clear the screen
    screen.fill(black)

    # Draw all sprites
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
