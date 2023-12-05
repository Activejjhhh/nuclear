import pygame
import subprocess
import random

pygame.init()

display_width = 1400
display_height = 800
screen = pygame.display.set_mode((display_width, display_height))


font_path = "C:/Users/Danie/OneDrive/Desktop/Sublime Coding/Fonts/disposabledroid-bb.regular.ttf"
font = pygame.font.Font(font_path, 32)

text_surface = font.render("Missile Control Panel Loading Up", True, (255, 255, 255))


text_x = (display_width - text_surface.get_width()) / 2
text_y = (display_height - text_surface.get_height()) / 2

jjhhh_font_path = "C:/Users/Danie/OneDrive/Desktop/Sublime Coding/Fonts/Inconsolata-Regular.ttf"
jjhhh_font = pygame.font.Font(jjhhh_font_path, 16)
jjhhh_surface = jjhhh_font.render("jjhhh studios", True, (255, 255, 255))

jjhhh_x = 10
jjhhh_y = 10
s
start_time = pygame.time.get_ticks()
dot_interval = 500

dots_visible = True


loading_bar_width = display_width - 200
loading_bar_height = 20
loading_bar_x = (display_width - loading_bar_width) / 2
loading_bar_y = display_height - 50 
loading_bar_color = (0, 255, 0)  

border_width = loading_bar_width + 10
border_height = loading_bar_height + 10
border_x = loading_bar_x - 5
border_y = loading_bar_y - 5
border_color = (255, 255, 255)  

quotes = [
    "\"War is cruelty. There is no use trying to reform it. The crueler it is, the sooner it will be over.\" - William Tecumseh Sherman",
    "\"The true soldier fights not because he hates what is in front of him, but because he loves what is behind him.\" - Gilbert K. Chesterton",
    "\"Only the dead have seen the end of war.\" - Plato",
    "\"War does not determine who is right - only who is left.\" - Bertrand Russell",
    "\"Man has no right to kill his brother. It is no excuse that he does so in uniform: he only adds the infamy of servitude to the crime of murder.\" - Percy Bysshe Shelley",
    "\"A world without nuclear weapons would be less stable and more dangerous for all of us.\" - Margaret Thatcher",
    "\"A nuclear war cannot be won and must never be fought. The only value in our two nations possessing nuclear weapons is to make sure they will never be used. But then would it not be better to do away with them entirely?\" - Ronald Reagan",
    "\"For the first time in the history of mankind, one generation literally has the power to destroy the past, the present and the future, the power to bring time to an end.\" - Hubert H. Humphrey",
    "\"I know not with what weapons World War III will be fought, but World War IV will be fought with sticks and stones.\" - Albert Einstein",
    "\"The unleashed power of the atom has changed everything save our modes of thinking and we thus drift toward unparalleled catastrophe.\" - Albert Einstein",
    "\"The existence of nuclear weapons presents a clear and present danger to life on Earth.\" - Oscar Arias",
    "\"Every inhabitant of this planet must contemplate the day when this planet may no longer be habitable .. The weapons of war must be abolished before they abolish us.\" - John F. Kennedy",
    "\"Ours is a world of nuclear giants and ethical infants. We know more about war that we know about peace, more about killing that we know about living.\" - Omar N. Bradley",
    "\"“Now I am become Death, the destroyer of worlds.\" - Robert J. Oppenheimer"
]

quote = random.choice(quotes)


quote_text, quote_author = quote.rsplit(" - ", 1)

def wrap_text(text, author, font, max_width):
    words = text.split(' ')
    lines = []  
    current_line = []  

    for word in words:
        if font.size(' '.join(current_line + [word]))[0] <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    else:
        lines.append(' '.join(current_line))
    lines.append(author)

    return lines
max_width = display_width - 200 
quote_lines = wrap_text(quote_text, quote_author, font, max_width)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time >= 10000:
        pygame.display.quit()  
        subprocess.run(["python", "C:/Users/Danie/OneDrive/Desktop/Sublime Coding/Nuclear/menu screen.py"])
        running = False


    if elapsed_time % dot_interval == 0:
        dots_visible = not dots_visible

    dots = "." * (int(elapsed_time / dot_interval) % 4)
    if not dots_visible:
        dots = ""

    text_with_dots = font.render("Missile Control Panel Loading Up" + dots, True, (255, 255, 255))


    text_with_dots_x = (display_width - text_with_dots.get_width()) / 2
    text_with_dots_y = (display_height - text_with_dots.get_height()) / 2


    screen.fill((0, 0, 0))
    screen.blit(text_with_dots, (text_with_dots_x, text_with_dots_y))
    screen.blit(jjhhh_surface, (jjhhh_x, jjhhh_y))
    pygame.draw.rect(screen, loading_bar_color, pygame.Rect(loading_bar_x, loading_bar_y, loading_bar_width * (elapsed_time / 10000), loading_bar_height))
    pygame.draw.rect(screen, border_color, pygame.Rect(border_x, border_y, border_width, border_height), 2)


    for i, line in enumerate(quote_lines):
        quote_surface = font.render(line, True, (255, 255, 255))


        quote_x = (display_width - quote_surface.get_width()) / 2
        quote_y = text_with_dots_y + 50 + i * font.get_height()  

        screen.blit(quote_surface, (quote_x, quote_y))


    pygame.display.update()

pygame.quit()
