import pygame
import sqlite3
import sys
from passlib.hash import bcrypt_sha256

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 1400
screen_height = 800

# Set color scheme
neon_green = (57, 255, 20)
black = (0, 0, 0)
grey = (128, 128, 128)

# Create screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set window caption
pygame.display.set_caption('Login/Sign Up Area')

# Create a SQLite database connection
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username text UNIQUE, password text)''')

def user_exists(username):
    # Check if username exists in the database
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone() is not None

def login(username, password):
    # Check if credentials exist in the database
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    data = c.fetchone()
    if data is None:
        return False
    else:
        return bcrypt_sha256.verify(password, data[1])

def signup(username, password):
    # Insert new user into the database
    if username == '' or password == '':
        return 'Username and password cannot be empty!'
    elif user_exists(username):
        return 'Username already exists!'
    else:
        hashed_password = bcrypt_sha256.hash(password)
        c.execute("INSERT INTO users VALUES (?,?)", (username, hashed_password))
        conn.commit()
        return 'Sign up successful!'

class Button:
    def __init__(self, rect, text='', visible=True):
        self.rect = rect
        self.text = text
        self.visible = visible

class TextBox:
    def __init__(self, rect, text=''):
        self.rect = rect
        self.text = text
        self.active = False

# Create the buttons with adjusted positions and spacing
login_button = Button(pygame.Rect(screen_width//2 - 100, screen_height//2 + 60, 200, 50), 'Login')
signup_button = Button(pygame.Rect(screen_width//2 - 50, screen_height - 60, 100, 30), 'Sign Up')

buttons = [login_button, signup_button]

# Create the text boxes for entering credentials
username_box = TextBox(pygame.Rect(screen_width//2 - 100, screen_height//2 - 60, 200, 50), '')
password_box = TextBox(pygame.Rect(screen_width//2 - 100, screen_height//2 , 200, 50), '')

text_boxes = [username_box, password_box]

def draw_button(screen ,button):
    if button.visible:
        pygame.draw.rect(screen ,grey if button.rect.collidepoint(pygame.mouse.get_pos()) else neon_green ,button.rect)
        font = pygame.font.Font(None ,36)
        text = font.render(button.text ,True ,black)
        screen.blit(text ,(button.rect.x + button.rect.width // 2 - text.get_width() // 2,
                           button.rect.y + button.rect.height // 2 - text.get_height() // 2))

def draw_text_box(screen ,text_box):
    pygame.draw.rect(screen ,neon_green if text_box.active else grey ,text_box.rect)
    font = pygame.font.Font(None ,36)
    text = font.render(text_box.text ,True ,black)
    screen.blit(text ,(text_box.rect.x +10 ,text_box.rect.y +10))

def display_message(message):
    font = pygame.font.Font(None ,48)
    text_surface = font.render(message ,True ,neon_green)
    screen.blit(text_surface ,(screen_width //2 - text_surface.get_width() //2 ,
                               screen_height //2 + login_button.rect.height +80))
    pygame.display.flip()
    pygame.time.wait(2000)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for button in buttons:
                if button.rect.collidepoint(mouse_pos) and button.visible:
                    print(f"{button.text} button clicked!")
                    if button.text == 'Login':
                        if login(username_box.text ,password_box.text):
                            display_message('Login successful!')
                        else:
                            display_message('Wrong username or password!')
                    elif button.text == 'Sign Up':
                        message = signup(username_box.text ,password_box.text)
                        display_message(message)
                        if message == 'Sign up successful!':
                            username_box.text =''
                            password_box.text =''
                            login_button.visible = True

            for box in text_boxes:
                if box.rect.collidepoint(mouse_pos):
                    box.active = True
                else:
                    box.active = False

        elif event.type == pygame.KEYDOWN:
            for box in text_boxes:
                if box.active:
                    if event.key == pygame.K_BACKSPACE:
                        box.text = box.text[:-1]
                    else:
                        box.text += event.unicode

    # Fill the screen with black color
    screen.fill(black)

    # Draw title at the top left corner of the screen
    font = pygame.font.Font(None ,48)
    title_text = font.render('NUCLEAR SIMULATOR' ,True ,neon_green)
    screen.blit(title_text ,(20 ,20))

    # Draw buttons and text boxes
    for button in buttons:
        draw_button(screen ,button)

    for box in text_boxes:
        draw_text_box(screen ,box)

    # Update the display
    pygame.display.flip()
