import pygame
pygame.init()
import vlc


# Set the screen size
screen_width = 1400
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))


# Initialize VLC
instance = vlc.Instance('--no-xlib')
player = instance.media_player_new()
media = instance.media_new('C:/Users/Danie/OneDrive/Desktop/Sublime Coding/RPReplay_Final1677529967.mov')
player.set_media(media)

# Set the window handle for VLC
player.set_hwnd(pygame.display.get_wm_info()['window'])



# Set the font and font size
font = pygame.font.Font(None, 60)

# Set the colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set the brand and title text
brand_text = "jjhhh Studios Uplink Launcher"
title_text = "Launch Operations Center"

# Render the brand and title text
brand_surface = font.render(brand_text, True, white)
title_surface = font.render(title_text, True, white)


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.hover_color = (color[0]+50, color[1]+50, color[2]+50) # Set hover color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
    
    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        
        if self.is_hovered(pygame.mouse.get_pos()): # Check if button is being hovered
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height), 0)
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.Font(None, 30)
            text = font.render(self.text, True, (255,255,255))
            screen.blit(text, (self.x + (self.width // 2 - text.get_width() // 2), self.y - text.get_height() - 10))

    
    def is_clicked(self, mouse_pos):
        if mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width:
            if mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height:
                return True
        return False
    
    def is_hovered(self, mouse_pos):
        if mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width:
            if mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height:
                return True
        return False


  
# Set the button dimensions
button_width = 200
button_height = 50

# Set the button colors
button_color = (50, 50, 50)
button_hover_color = (100, 100, 100)
hover_color = (200, 200, 200)


# Set the button text
login_text = "login"
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
message1_pos = (screen_width // 2 - text_width // 2, screen_height // 3 - text_height // 2)
message2_pos = (screen_width // 2 - text_width // 2, screen_height // 3 + text_height // 2)

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
login_pos = (300, 350)  
running = True 


# Create the login button
login_button = Button((255, 255, 255), 350, 350, 100, 50, 'Login')
login_rect = pygame.Rect(login_button.x, login_button.y, login_button.width, login_button.height)
configure_button = Button((255, 255, 255), button_x, button_y + 100, button_width, button_height, 'Configure')
configure_rect = pygame.Rect(configure_button.x, configure_button.y, configure_button.width, configure_button.height)
panic_button = Button((255, 255, 255), button_x, button_y + 200, button_width, button_height, 'Panic')
panic_rect = pygame.Rect(panic_button.x, panic_button.y, panic_button.width, panic_button.height)








# Start the main loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if login_rect.collidepoint(mouse_pos):
                print("Login button pressed")
            elif configure_rect.collidepoint(mouse_pos):
                print("Configure button pressed")
            elif panic_rect.collidepoint(mouse_pos):
                print("Panic button pressed")
                player.play()
            player.stop()
    # Get the mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Check if mouse is hovering over buttons and change color if true
    if login_rect.collidepoint(mouse_pos):
        login_color = hover_color
    else:
        login_color = button_color

    if configure_rect.collidepoint(mouse_pos):
        configure_color = hover_color
    else:
        configure_color = button_color

    if panic_rect.collidepoint(mouse_pos):
        panic_color = hover_color
    else:
        panic_color = button_color
    
    # Draw the brand and title text
    screen.blit(brand_surface, (0, 0))
    screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, screen_height // 6 - title_surface.get_height() // 2))
    
    # Draw the text messages
    screen.blit(message1_surface, message1_pos)
    screen.blit(message2_surface, message2_pos)
    
    # Draw the buttons
    pygame.draw.rect(screen, login_color, login_rect)
    pygame.draw.rect(screen, configure_color, configure_rect)
    pygame.draw.rect(screen, panic_color, panic_rect)
    screen.blit(login_surface, (login_pos[0] + button_width // 2 - login_surface.get_width() // 2, login_pos[1] + button_height // 2 - login_surface.get_height() // 2))
    screen.blit(configure_surface, (configure_pos[0] + button_width // 2 - configure_surface.get_width() // 2, configure_pos[1] + button_height // 2 - configure_surface.get_height() // 2))

    # Draw the panic button and check for hover
    panic_rect = pygame.Rect(panic_pos[0], panic_pos[1], button_width, button_height)
    panic_hover = panic_rect.collidepoint(pygame.mouse.get_pos())
    if panic_hover:
        pygame.draw.rect(screen, button_hover_color, panic_rect)
    else:
        pygame.draw.rect(screen, button_color, panic_rect)
    screen.blit(panic_surface, (panic_pos[0] + button_width // 2 - panic_surface.get_width() // 2, panic_pos[1] + button_height // 2 - panic_surface.get_height() // 2))

    # Check for button hover and click events
    mouse_pos = pygame.mouse.get_pos()
    login_hover = login_rect.collidepoint(mouse_pos)
    configure_hover = configure_rect.collidepoint(mouse_pos)
    panic_hover = panic_rect.collidepoint(mouse_pos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if login_hover:
                print("Login button pressed")
            elif configure_hover:
                print("Configure button pressed")
            elif panic_hover:
                player.play()


    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()