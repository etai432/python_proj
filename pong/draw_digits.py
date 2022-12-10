import pygame

# Initialize the pygame library
pygame.init()

# Set the width and height of the screen
screen = pygame.display.set_mode((400, 300))

# Set the title of the window
pygame.display.set_caption("Pygame: Drawing digits")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the font and font size
font = pygame.font.Font(None, 32)

# This function will draw a digit on the screen
def draw_digit(digit, x, y):
  # Render the text for the digit
  text = font.render(str(digit), True, BLACK, WHITE)
  
  # Get the rectangle for the text
  text_rect = text.get_rect()
  
  # Center the text on the screen
  text_rect.center = (x, y)
  
  # Draw the text on the screen
  screen.blit(text, text_rect)

# This is the main game loop
done = False
while not done:
  # Handle events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
  
  # Clear the screen
  screen.fill(WHITE)
  
  # Draw each digit on the screen
  for i in range(10):
    draw_digit(i, 50 + i * 30, 50)
  
  # Update the screen
  pygame.display.flip()

# Quit the game
pygame.quit()