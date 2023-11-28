import pygame
import sqlite3
import sys
from passlib.hash import bcrypt_sha256

pygame.init()

screen_width = 1400
screen_height = 800


neon_green = (57, 255, 20)
black = (0, 0, 0)
grey = (128, 128, 128)
lighter_grey = (192, 192, 192)  
darker_grey = (105, 105, 105)  
red = (255, 0, 0)


screen = pygame.display.set_mode((screen_width, screen_height))


pygame.display.set_caption('Login/Sign Up Area')


conn = sqlite3.connect('users.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (username text UNIQUE, password text)''')

def user_exists(username):

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone() is not None

def login(username, password):

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    data = c.fetchone()
    if data is None:
        return False
    else:
        return bcrypt_sha256.verify(password, data[1])

def validate_input(username, password):
    if len(username) < 5 or len(password) < 8:
        return 'Username must be at least 5 characters and password must be at least 8 characters!'
    if not any(char.isdigit() for char in password):
        return 'Password must contain at least one digit!'
    if not any(char.isalpha() for char in password):
        return 'Password must contain at least one letter!'
    if not any(char.isupper() for char in password):
        return 'Password must contain at least one uppercase letter!'
    if not any(char.islower() for char in password):
        return 'Password must contain at least one lowercase letter!'
    return ''
def signup(username, password):
    validation_message = validate_input(username, password)
    if validation_message != '':
        return validation_message
    elif username == '' or password == '':
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
    def __init__(self, rect, text='', hidden=False, placeholder=''):
        self.rect = rect
        self.text = text
        self.active = False
        self.hidden = hidden
        self.placeholder = placeholder

    def get_display_text(self):
        if self.text == '' and not self.active:
            return self.placeholder
        elif self.hidden:
            return '*' * len(self.text)
        else:
            return self.text

def draw_button(screen, button):
    if button.visible:
        if button.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:  
                pygame.draw.rect(screen, darker_grey, button.rect, border_radius=5)
            else:  
                pygame.draw.rect(screen, lighter_grey, button.rect, border_radius=5)
        else:  
            pygame.draw.rect(screen, grey, button.rect, border_radius=5)

        font = pygame.font.Font(None, 36)
        text = font.render(button.text, True, black)
        screen.blit(text, (button.rect.x + button.rect.width // 2 - text.get_width() // 2,
                           button.rect.y + button.rect.height // 2 - text.get_height() // 2))

def draw_text_box(screen, text_box):
    pygame.draw.rect(screen, neon_green, text_box.rect, 2)  
    font = pygame.font.Font(None, 36)
    text = font.render(text_box.get_display_text(), True, neon_green)
    screen.blit(text, (text_box.rect.x + 10, text_box.rect.y + 10))

def display_message(message, error=False):
    red = (255, 0, 0)  
    font = pygame.font.Font(None, 48)
    text_surface = font.render(message, True, red if error else neon_green)
    screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, screen_height // 2 + login_button.rect.height + 120))  # Moved down
    pygame.display.flip()
    pygame.time.wait(2000)

def signup_screen():
    username_box = TextBox(pygame.Rect(screen_width//2 - 150, screen_height//2 - 20, 300, 50), '', False, 'Username')
    password_box = TextBox(pygame.Rect(screen_width//2 - 150, screen_height//2 + 40, 300, 50), '', True, 'Password')

    text_boxes = [username_box, password_box]

    signup_button = Button(pygame.Rect(screen_width//2 - 150, screen_height//2 + 220, 300, 50), 'Sign Up')  # Moved further down

    buttons = [signup_button]


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
                        if button.text == 'Sign Up':
                            message = signup(username_box.text, password_box.text)
                            display_message(message, message != 'Sign up successful!')
                            if message == 'Sign up successful!':
                                username_box.text = ''
                                password_box.text = ''
                                return  

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

        screen.fill(black)


        font = pygame.font.Font(None, 48)
        title_text = font.render('NUCLEAR SIMULATOR', True, neon_green)
        screen.blit(title_text, (20, 20))

        for button in buttons:
            draw_button(screen, button)

        for box in text_boxes:
            draw_text_box(screen, box)


        pygame.display.flip()

login_button = Button(pygame.Rect(screen_width//2 - 150, screen_height//2 + 100, 300, 50), 'Login')
signup_button = Button(pygame.Rect(screen_width//2 - 150, screen_height//2 + 290, 300, 50), 'Sign Up')

buttons = [login_button, signup_button]

username_box = TextBox(pygame.Rect(screen_width//2 - 150, screen_height//2 - 20, 300, 50), '', False, 'Username')
password_box = TextBox(pygame.Rect(screen_width//2 - 150, screen_height//2 + 40, 300, 50), '', True, 'Password')

text_boxes = [username_box, password_box]


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
                        if login(username_box.text, password_box.text):
                            display_message('Login successful!')
                        else:
                            display_message('Wrong username or password!', True)
                    elif button.text == 'Sign Up':
                        signup_screen()

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


    screen.fill(black)

   

    font = pygame.font.Font(None, 48)
    title_text = font.render('NUCLEAR SIMULATOR', True, neon_green)
    screen.blit(title_text, (20, 20))


    for button in buttons:
        draw_button(screen, button)

    for box in text_boxes:
        draw_text_box(screen, box)

    pygame.display.flip()
