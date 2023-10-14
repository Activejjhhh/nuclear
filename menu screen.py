import pygame
import sys
import time 

# Initialize Pygame
pygame.init()

# Set the screen size
screen_width = 1400
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the colors
black = (0, 0, 0)
green = (0, 255, 0)
grey = (128, 128, 128) # New color
blue = (0, 0, 255) # New color for BSOD

# Set the font and font size
font = pygame.font.Font(None, 60)
status_font = pygame.font.Font(None, 40) # New font for status text

# Set the button dimensions
button_width = 400 # Increased button width
button_height = 100 # Increased button height

# Set the button text
button_texts = ["Start", "Configure", "Panic"]

class Button:
    def __init__(self, rect, visible=True):
        self.rect = rect
        self.visible = visible

# Create the buttons with adjusted positions and spacing
buttons = [Button(pygame.Rect(screen_width//4 - button_width//2 - 100, screen_height//3 + i*150, button_width, button_height)) for i in range(3)]

def draw_button(screen, button_rect, color, text_surface):
    pygame.draw.rect(screen, color, button_rect.rect, 3) # Outline width set to 3
    screen.blit(text_surface, (button_rect.rect.x + button_rect.rect.width // 2 - text_surface.get_width() // 2,
                               button_rect.rect.y + button_rect.rect.height // 2 - text_surface.get_height() // 2))

def display_bsod(screen, buttons):
    # Hide the buttons
    for button in buttons:
        button.visible = False

    # Fill the screen with blue
    screen.fill(blue)

    # Load the BSOD image and play the sound effect
    bsod_image = pygame.image.load("C:/Users/Danie/Downloads/mFxX21T-blue-screen-of-death-wallpaper.jpg").convert()
    bsod_image = pygame.transform.smoothscale(bsod_image, (screen_width, screen_height))
    bsod_sound = pygame.mixer.Sound("C:/Users/Danie/Downloads/blue-screen-of-death.mp3")
    bsod_sound.play()
    
    # Display the BSOD image
    screen.blit(bsod_image, (screen_width // 2 - bsod_image.get_width() // 2,
                             screen_height // 2 - bsod_image.get_height() // 2))

    # Update the screen
    pygame.display.flip()

    # Wait for 5 seconds
    time.sleep(5)

    # Clear the screen
    screen.fill(black)

    # Show the buttons
    for button in buttons:
        button.visible = True

    # Wait for 5 more seconds
    time.sleep(5)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for i in range(len(buttons)):
                if buttons[i].rect.collidepoint(mouse_pos) and buttons[i].visible:
                    print(f"{button_texts[i]} button clicked!")
                    if button_texts[i] == "Panic":
                        display_bsod(screen, buttons)

    screen.fill(black)

    # Draw title
    title_surface = font.render("NUCLEAR SIMULATOR", True, green)
    screen.blit(title_surface, (20, 20))

    # Draw buttons only if they are visible
    for i in range(3):
        if buttons[i].visible:
            button_surface = font.render(button_texts[i], True, green)
            draw_button(screen, buttons[i], grey if buttons[i].rect.collidepoint(pygame.mouse.get_pos()) else green , button_surface)

    # Draw verification status box and text only if all buttons are visible 
    if all(button.visible for button in buttons):
        status_box = pygame.Rect(screen_width//2 - button_width//2 , screen_height - screen_height//4 , button_width , button_height) # Made status_box smaller
        
        status_text_surface = status_font.render("Authentication Status:", True, green) # Used the new font for status text
        
        verified_text_surface = font.render("Verified", True , green)
        
        screen.blit(status_text_surface , (status_box.x + status_box.width//2 - status_text_surface.get_width()//2 , screen_height - status_text_surface.get_height() - verified_text_surface.get_height())) # Moved the "Authentication Status:" text to the bottom of the screen
        
        screen.blit(verified_text_surface , (status_box.x + status_box.width//2 - verified_text_surface.get_width()//2 , screen_height - verified_text_surface.get_height())) # Moved "Verified" underneath the "Authentication Status:" box

    pygame.display.flip()

pygame.quit()
sys.exit()

