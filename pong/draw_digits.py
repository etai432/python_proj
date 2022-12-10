# Import the necessary Pygame modules
import pygame

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
width = 800
height = 600

# Create a screen with the specified dimensions
screen = pygame.display.set_mode((width, height))

# Set the title of the window
pygame.display.set_caption("Pygame Digits")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create a font for rendering the digits
font = pygame.font.SysFont("Arial", 24)

# This function will take a digit and dimensions as arguments and render it on the screen
def render_digit(digit, width, height):
  # Create a font with the specified dimensions
  font = pygame.font.SysFont("Arial", width, height)

  # Create a surface with the specified digit rendered in white
  surface = font.render(str(digit), True, WHITE)

  # Calculate the x and y position of the surface on the screen
  x = (screen.get_width() - width) / 2
  y = (screen.get_height() - height) / 2

  # Blit (draw) the surface onto the screen
  screen.blit(surface, (x, y))

# Main game loop
running = True
while running:
  # Process events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Clear the screen
  screen.fill(BLACK)

  # Render the digit 5 on the screen with dimensions 50x50
  render_digit(5, 600, 600)

  # Update the display
  pygame.display.flip()

# Close the window and clean up Pygame
pygame.quit()