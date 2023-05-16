import pygame
import subprocess

# initialize pygame
pygame.init()

# set the display size and create the window
display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))

# set the font and create the text surface
font_path = "C:/Users/Danie/OneDrive/Desktop/Sublime Coding/Fonts/disposabledroid-bb.regular.ttf"
font = pygame.font.Font(font_path, 32)
text_surface = font.render("Script initializing", True, (255, 255, 255))

# set the position of the text
text_x = (display_width - text_surface.get_width()) / 2
text_y = (display_height - text_surface.get_height()) / 2

# set the jjhhh studios text
jjhhh_font_path = "C:/Users/Danie/OneDrive/Desktop/Sublime Coding/Fonts/Inconsolata-Regular.ttf"
jjhhh_font = pygame.font.Font(jjhhh_font_path, 16)
jjhhh_surface = jjhhh_font.render("jjhhh studios", True, (255, 255, 255))

# set the position of the jjhhh studios text
jjhhh_x = 10
jjhhh_y = 10

# set the start time and interval for the dots
start_time = pygame.time.get_ticks()
dot_interval = 500

# set the initial visibility of the dots
dots_visible = True


# main game loop
running = True
while running:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # check if it's been 3 seconds
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time >= 3000:
        subprocess.run(["python", "C:/Users/Danie/OneDrive/Desktop/Sublime Coding/Nuclear/menu screen.py"])
        running = False

    # check if the dots should be visible
    if elapsed_time % dot_interval == 0:
        dots_visible = not dots_visible

    # create the dots string
    dots = "." * (int(elapsed_time / dot_interval) % 4)
    if not dots_visible:
        dots = ""

    # create the text surface with the dots
    text_with_dots = font.render("Script initializing" + dots, True, (255, 255, 255))

    # set the position of the text with the dots
    text_with_dots_x = (display_width - text_with_dots.get_width()) / 2
    text_with_dots_y = (display_height - text_with_dots.get_height()) / 2

    # draw the black screen, the text, and the jjhhh studios text
    screen.fill((0, 0, 0))
    screen.blit(text_with_dots, (text_with_dots_x, text_with_dots_y))
    screen.blit(jjhhh_surface, (jjhhh_x, jjhhh_y))

    # update the screen
    pygame.display.update()

# quit pygame
pygame.quit()