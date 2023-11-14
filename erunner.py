# Import pygame and initialize it
import pygame
import random

# Create an empty list to store the obstacles
obstacles = []


pygame.init()

# Define some colors and constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 1
JUMP_SPEED = -15
GROUND_SPEED = -15
GROUND_HEIGHT = 100
OBSTACLE_SPEED = -10
OBSTACLE_FREQUENCY = 60  # How often a new obstacle spawns (in frames)

# Create a game window and set its title
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Runner")

# Create a clock to control the frame rate
clock = pygame.time.Clock()

# Create a font to render text
font = pygame.font.SysFont("Arial", 32)

# Initialize pygame's joystick module
pygame.joystick.init()  # Initialize the joystick module
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(
        0
    )  # Create a joystick object for the first joystick
    joystick.init()  # Enable the joystick to receive events


# Create a player sprite that can jump with the spacebar
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class constructor
        super().__init__()

        # Set the image and the rect attributes
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

        # Set the initial position and speed
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 100
        self.speed_y = 0

        # Set a flag to indicate if the player is on the ground or not
        self.on_ground = True

    def update(self):
        # Update the speed and position according to gravity and user input
        self.speed_y += GRAVITY  # Apply gravity

        # Check if the spacebar is pressed and the player is on the ground
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE] and self.on_ground:
        #     # Set the speed to jump and set the flag to false
        #     self.speed_y = JUMP_SPEED
        #     self.on_ground = False

        # if a joystick button event is detected or the spacebar is pressed and the player is on the ground
        # if (
        #     pygame.JOYBUTTONDOWN in [event.type for event in pygame.event.get()]
        #     or pygame.key.get_pressed()[pygame.K_SPACE] == 1
        # ) and self.on_ground:
        #     # Set the speed to jump and set the flag to false
        #     self.speed_y = JUMP_SPEED
        #     self.on_ground = False
        # for event in pygame.event.get():
        #     print(event)
        #     if event.type == pygame.JOYBUTTONDOWN and self.on_ground:
        #         # Set the speed to jump and set the flag to false
        #         self.speed_y = JUMP_SPEED
        #         self.on_ground = False
        # check if joystick is connected

        if (
            (joystick.get_init and joystick.get_button(0) == 1)
            or pygame.key.get_pressed()[pygame.K_SPACE] == 1
        ) and self.on_ground:
            # Set the speed to jump and set the flag to false
            self.speed_y = JUMP_SPEED
            self.on_ground = False

        # Update the vertical position and check for collisions with the ground or the screen edge
        self.rect.y += self.speed_y  # Update position

        # If the player goes below the ground, move it back and set the flag to true
        if self.rect.y > SCREEN_HEIGHT - self.rect.height - 100:
            self.rect.y = SCREEN_HEIGHT - self.rect.height - 100
            self.on_ground = True

        # If the player goes above the screen, move it back and set the speed to zero
        if self.rect.y < 0:
            self.rect.y = 0
            self.speed_y = 0


# Create a ground sprite that scrolls endlessly
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class constructor
        super().__init__()

        # Set the image and the rect attributes
        self.image = pygame.Surface((SCREEN_WIDTH * 2, GROUND_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        # Set the initial position and speed
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.speed_x = GROUND_SPEED

    def update(self):
        # Update the horizontal position and check for collisions with the screen edge
        self.rect.x += self.speed_x  # Update position

        # If the ground goes off the screen, move it back to create an endless effect
        if self.rect.x < -SCREEN_WIDTH:
            self.rect.x = 0


# Create an obstacle sprite that moves towards the player and can cause game over
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class constructor
        super().__init__()

        # Set the image and the rect attributes randomly (you can use any shape or image you want)
        shape = pygame.Surface((50, random.randint(10, 100)))
        shape.fill(
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )  # Random color
        self.image = shape
        self.rect = self.image.get_rect()

        # Set the initial position and speed
        self.rect.x = SCREEN_WIDTH  # Start at the right edge of the screen
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height
        # Random vertical position
        self.speed_x = OBSTACLE_SPEED

    def update(self):
        # Update the horizontal position and check for collisions with the screen edge
        self.rect.x += self.speed_x  # Update position

        # If the obstacle goes off the screen, remove it from the group and the list
        if self.rect.x < -self.rect.width:
            self.kill()  # Remove from all groups
            obstacles.remove(self)  # Remove from list

    def draw(self, surface):
        # Draw the obstacle on the surface
        surface.blit(self.image, self.rect)


# Define a main function that runs the game
def main():
    # Create a boolean variable to control the game loop
    running = True

    # Create a boolean variable to indicate if the game is over or not
    game_over = False

    # Create an integer variable to store the score
    score = 0

    # Create an integer variable to count the frames
    counter = 0

    # Create a sprite group for each type of sprite
    player_group = pygame.sprite.Group()
    ground_group = pygame.sprite.Group()
    obstacle_group = pygame.sprite.Group()

    # Create a player object and add it to the player group
    player = Player()
    player_group.add(player)

    # Create a ground object and add it to the ground group
    ground = Ground()
    ground_group.add(ground)

    # Start the game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            # If the user clicks the close button, exit the game loop
            if event.type == pygame.QUIT:
                running = False

        # Update the sprites
        player_group.update()
        ground_group.update()
        obstacle_group.update()

        # Check for collisions between the player and the obstacles
        collisions = pygame.sprite.spritecollide(player, obstacle_group, False)

        # If there are any collisions, set the game over flag to True
        if collisions:
            game_over = True

        # If the game is not over, increase the score and spawn new obstacles
        if not game_over:
            # Increase the score by one every frame
            score += 1

            # Increase the counter by one every frame
            counter += 1

            # If the counter reaches the obstacle frequency, reset it and spawn a new obstacle
            if counter == OBSTACLE_FREQUENCY:
                counter = 0

                # Create a new obstacle object and add it to the obstacle group and the list
                obstacle = Obstacle()
                obstacle_group.add(obstacle)
                obstacles.append(obstacle)

        # Draw the background color
        screen.fill(WHITE)

        # Draw the sprites
        player_group.draw(screen)
        ground_group.draw(screen)
        obstacle_group.draw(screen)

        # Draw the score text
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # If the game is over, draw the game over text
        if game_over:
            game_over_text = font.render("Game Over", True, RED)
            screen.blit(
                game_over_text,
                (
                    SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2,
                ),
            )

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(60)

    # Uninitialize pygame's joystick module
    # pygame.joystick.quit()
    # Quit pygame and exit the program
    pygame.quit()
    exit()


# Call the main function
if __name__ == "__main__":
    main()
