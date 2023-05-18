import pygame
import time
import sys
# Initialize Pygame
pygame.init()

# Set the screen size
screen_width = 1400
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the font and font size
font = pygame.font.Font(None, 60)

# Rest of the code...

# Set the colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# Set the button dimensions
button_width = 200
button_height = 50
button_padding = 20 

# Set the button colors
button_color = (50, 50, 50)
button_hover_color = (100, 100, 100)
hover_color = (200, 200, 200)

# Set the button text
login_text = "Login"
configure_text = "Configure"
panic_text = "Panic"

# Set the text dimensions
text_width = 500
text_height = 100

# Set the text color
text_color = (255, 255, 255)

# Set the text font and size
text_font = pygame.font.Font(None, 30)

# Set the text messages
message1_text = "Warning: This system is for authorized users only."
message2_text = "Unauthorized access is strictly prohibited."

# Render the text messages
message1_surface = text_font.render(message1_text, True, text_color)
message2_surface = text_font.render(message2_text, True, text_color)


# Set the text positions
message1_pos = (screen_width - text_width - 20, screen_height - text_height - 80)
message2_pos = (screen_width - text_width - 20, screen_height - text_height - 20)



# Set the button surfaces
login_surface = font.render(login_text, True, white)
configure_surface = font.render(configure_text, True, white)
panic_surface = font.render(panic_text, True, white)

# Set the button positions
button_x = screen_width // 2 - button_width // 2
button_y = screen_height // 2 - button_height // 2
launch_pos = (button_x, button_y)





configure_pos = (button_x, button_y + 100)
panic_pos = (button_x, button_y + 200)
login_pos = (button_x - 405 , button_y  -38 )




running = True


# Set the button positions
button_x = 100  # X-coordinate for the buttons
button_y = screen_height // 2 - (button_height + button_padding)  # Starting Y-coordinate for the buttons

# Create the login button
login_button = pygame.Rect(button_x + 50, button_y, button_width, button_height)
configure_button = pygame.Rect(button_x + 50, button_y + button_height + button_padding, button_width, button_height)
panic_button = pygame.Rect(button_x + 50, button_y + (button_height + button_padding) * 2, button_width, button_height)



def draw_button(screen, button_rect, color, text_surface):
    pygame.draw.rect(screen, color, button_rect)
    screen.blit(text_surface, (button_rect.x + button_rect.width // 2 - text_surface.get_width() // 2,
                               button_rect.y + button_rect.height // 2 - text_surface.get_height() // 2))


def display_bsod(screen, buttons, brand_surface, title_surface, message1_surface, message2_surface):
    # Hide the buttons
    for button in buttons:
        button["visible"] = False

    # Hide the brand and title text
    brand_surface.set_alpha(0)
    title_surface.set_alpha(0)
    message1_surface.set_alpha(0)
    message2_surface.set_alpha(0)

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
        button["visible"] = True

    # Show the brand and title text
    brand_surface.set_alpha(255)
    title_surface.set_alpha(255)
    message1_surface.set_alpha(255)
    message2_surface.set_alpha(255)

    # Wait for 5 more seconds
    time.sleep(5)

    # Quit the application
    pygame.quit()
    sys.exit()


# Create the buttons
buttons = [
    {"rect": configure_button, "color": button_color, "hover_color": button_hover_color, "text_surface": configure_surface, "visible": True},
    {"rect": panic_button, "color": button_color, "hover_color": button_hover_color, "text_surface": panic_surface, "visible": True},
    {"rect": login_button, "color": button_color, "hover_color": button_hover_color, "text_surface": login_surface, "visible": True},
]


# Create the brand and title text surfaces
brand_text = "jjhhh Studios Uplink Launcher"
title_text = "Launch Operations Center"
brand_surface = font.render(brand_text, True, white)
title_surface = font.render(title_text, True, white)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if login_button.collidepoint(mouse_pos):
                print("Login button clicked!")
            for button in buttons:
                if button["rect"].collidepoint(mouse_pos):
                    if button["text_surface"] == panic_surface:
                        display_bsod(screen, buttons, brand_surface, title_surface, message1_surface, message2_surface)

    screen.fill(black)

    screen.blit(brand_surface, (20, 20))
    screen.blit(title_surface, (20, 100))

    screen.blit(message1_surface, message1_pos)
    screen.blit(message2_surface, message2_pos)

    pygame.draw.rect(screen, button_color, login_button)
    screen.blit(login_surface, login_pos)

    for button in buttons:
        button_rect = button["rect"]
        color = button["color"]
        hover_color = button["hover_color"]
        text_surface = button["text_surface"]

        if button["visible"] and button_rect.collidepoint(pygame.mouse.get_pos()):
            color = hover_color

        draw_button(screen, button_rect, color, text_surface)
    pygame.display.flip()

pygame.quit()

