# Import the necessary Pygame modules
import pygame

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
width = 800
height = 600

# Create a screen with the specified dimensions in full screen mode
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

# Set the title of the window
pygame.display.set_caption("Pygame Text")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# This function will take a string, dimensions, and position as arguments and render it on the screen
def render_text(string, width, height, x, y):
  # Create a font with the specified dimensions
  font = pygame.font.SysFont("Arial", width, height)

  # Create a surface with the specified string rendered in white
  surface = font.render(string, True, WHITE)

  # Blit (draw) the surface onto the screen at the specified position
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

  # Render the string "Hello, World!" on the screen with dimensions 50x50 at position (100, 100)
  render_text("Hello, World!", 50, 50, 100, 100)

  # Update the display
  pygame.display.flip()

# Close the win