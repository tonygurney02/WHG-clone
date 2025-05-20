"""
Tony's attempt to make the world's hardest game.

if there is time I will try to learn how to use machine learning.
"""

import os
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

# Set up the game window and some constants
pygame.display.set_caption("World's hardest game")

print("Game started")

BG_COLOR = (255, 255, 255)  # Background color (white)
WIDTH, HEIGHT = 1000, 600  # Window dimensions
FPS = 60  # Frames per second for the game loop
PLAYER_VEL = 2  # Player velocity (speed)
level_scale = (605, 455)  # Scale of the level
WIN_Game = False

window = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window


# Function to load sprites from a given directory
def load_sprites(dir1, dir2, width, height):
    # Construct the file path to the sprite directory
    path = join(r"C:\Users\HP\PycharmProjects\PythonProject", dir1, dir2)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")

    # Get a list of all files in the directory
    images = [f for f in listdir(path) if isfile(join(path, f))]
    all_sprites = {}

    # Process each sprite sheet
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sheet_width, sheet_height = sprite_sheet.get_size()

        # Split the sprite sheet into individual sprites
        sprites = []
        for i in range(sheet_width // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)  # Copy part of the sheet
            sprites.append(pygame.transform.scale(surface, (15, 15)))  # Scale sprite

        all_sprites[image] = sprites  # Store sprites in a dictionary

    return all_sprites


# Function to load and scale the level image
def get_level(width, height):
    path = join(r"C:\Users\HP\PycharmProjects\PythonProject", "World's hardest game assets",
                "Browser Games - Worlds Hardest Game - Stages.png")

    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)  # Transparent surface
    rect = pygame.Rect(0, 0, width, height)
    surface.blit(image, (0, 0), rect)  # Copy the image to the surface
    return pygame.transform.scale(surface, level_scale)  # Scale the surface


# Player class (inherits from pygame.sprite.Sprite)
class Player(pygame.sprite.Sprite):
    color = (255, 0, 0)  # Player color (used if no sprite is loaded)
    SPRITES = load_sprites("World's hardest game assets", "", 18, 18)  # Load player sprites

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)  # Player's rectangle
        self.x_vel = 0  # Horizontal velocity
        self.y_vel = 0  # Vertical velocity
        self.direction = "left"  # Initial direction

        # Use the first sprite as the player's image and create a mask for collisions
        sprite = self.SPRITES[list(self.SPRITES.keys())[0]][0]
        self.image = sprite
        self.mask = pygame.mask.from_surface(self.image)

    # Move the player by (dx, dy)
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    # Movement functions for each direction
    def move_left(self, vel):
        self.x_vel = -vel
        self.direction = "left"

    def move_right(self, vel):
        self.x_vel = vel
        self.direction = "right"

    def move_up(self, vel):
        self.y_vel = -vel
        self.direction = "up"

    def move_down(self, vel):
        self.y_vel = vel
        self.direction = "down"

    # Update the player's position each frame
    def loop(self, fps):
        self.move(self.x_vel, self.y_vel)

    # Draw the player on the screen
    def draw(self, win):
        sprite = self.SPRITES[list(self.SPRITES.keys())[0]][0]
        win.blit(sprite, (self.rect.x, self.rect.y))


# Function to draw all game elements
def draw(window, player, objects):
    window.fill(BG_COLOR)  # Clear the screen
    player.draw(window)  # Draw the player

    # Draw all other objects
    for obj in objects:
        obj.draw(window)

    pygame.display.update()  # Update the display


# Base class for game objects (inherits from pygame.sprite.Sprite)
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)  # Object's rectangle
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Transparent surface
        self.width, self.height = width, height  # Store dimensions
        self.name = name  # Optional name for the object

        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for collisions

    # Draw the object on the screen
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))


# Level class (inherits from Object)
class level(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)  # Initialize the base object
        level = get_level(width, height)  # Load the level image
        self.image.blit(level, (0, 0))  # Copy the level onto the object's surface
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for collisions

class Goal(Object):
    color = (0, 255, 0)

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height,"goal")  # Initialize the base object
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a surface for the goal
        self.image.fill(self.color)  # Fill it with the goal color
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for collision detection

    def draw(self, win):
        pygame.draw.rect(win, self.color,self.rect)


# Check if the player collides with any object when moved by (dx, dy)
def collide(player, objects, dx, dy):
    player.move(dx, dy)  # Temporarily move the player
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):  # Check for collision using masks
            collided_object = obj  # Store the collided object
            break

    player.move(-dx, -dy)  # Move the player back to its original position
    return collided_object


# Handle player movement and prevent collisions
def handle_move(player, objects):

    global WIN_Game

    keys = pygame.key.get_pressed()  # Get pressed keys

    # Reset velocities
    player.x_vel = 0
    player.y_vel = 0

    # Check for potential collisions in each direction
    collide_left = collide(player, objects, -PLAYER_VEL, 0)
    collide_right = collide(player, objects, PLAYER_VEL, 0)
    collide_up = collide(player, objects, 0, -PLAYER_VEL)
    collide_down = collide(player, objects, 0, PLAYER_VEL)

    # Move the player if no collision is detected
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)
    if keys[pygame.K_UP] and not collide_up:
        player.move_up(PLAYER_VEL)
    if keys[pygame.K_DOWN] and not collide_down:
        player.move_down(PLAYER_VEL)

    to_check = [collide_left, collide_right, collide_up, collide_down]
    for obj in to_check:
        if obj and obj.name == "goal":
            WIN_Game = True


# Main game loop
def main(window):
    clock = pygame.time.Clock()  # Track time

    # Initialize the player and levels
    player = Player(100, 200, 50, 50)
    levels = level(0, 0, level_scale[0], level_scale[1])
    goal = Goal(450,290,100,100)

    objects = [goal,levels]

    run = True  # Game loop control

    while run:
        clock.tick(FPS)  # Ensure the game runs at the correct frame rate

        for event in pygame.event.get():  # Handle events
            if event.type == pygame.QUIT:  # Quit the game
                run = False
                break

        player.loop(FPS)  # Update the player
        handle_move(player, objects)  # Handle movement
        draw(window, player, objects)  # Draw the game

        if WIN_Game == True:
            print("Game Won!")
            run = False

    pygame.quit()  # Quit pygame
    quit()  # Quit the program


# Run the game
if __name__ == "__main__":
    main(window)
