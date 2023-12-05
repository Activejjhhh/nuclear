import pygame
import sys
import time 
import random
import pygame_gui 


pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()



class Button:
    def __init__(self, rect, visible=True):
        self.rect = rect
        self.visible = visible


screen_width = 1400
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

manager = pygame_gui.UIManager((screen_width, screen_height))


master_volume = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((screen_width//2 - 200, 100), (400, 40)),
                                                       start_value=100,
                                                       value_range=(0, 100),
                                                       manager=manager,
                                                       visible=False)

music = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((screen_width//2 - 200, 200), (400, 40)),
                                               start_value=100,
                                               value_range=(0, 100),
                                               manager=manager,
                                               visible=False)

sound_effects = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((screen_width//2 - 200, 300), (400, 40)),
                                                       start_value=100,
                                                       value_range=(0, 100),
                                                       manager=manager,
                                                       visible=False)

back_button = Button(pygame.Rect((screen_width//2 - 200, 540), (400, 50)), visible=False)

def create_gui():
    global title, master_volume_label, master_volume, music_label, music, sound_effects_label, sound_effects, measurements_button, colour_scheme_button



    title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((screen_width//2 - 75, 20), (150, 40)),
                                        text='NUCLEAR SIMULATOR',
                                        manager=manager,
                                        visible=True)

    master_volume_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((screen_width//2 - 200, 80), (400, 20)),
                                                      text='Master Volume',
                                                      manager=manager,
                                                      visible=True)
    master_volume = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((screen_width//2 - 200, 100), (400, 40)),
                                                           start_value=100,
                                                           value_range=(0, 100),
                                                           manager=manager,
                                                           visible=True)

    music_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((screen_width//2 - 200, 180), (400, 20)),
                                              text='Music',
                                              manager=manager,
                                              visible=True)
    music = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((screen_width//2 - 200, 200), (400, 40)),
                                                   start_value=100,
                                                   value_range=(0, 100),
                                                   manager=manager,
                                                   visible=True)

    sound_effects_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((screen_width//2 - 200, 280), (400, 20)),
                                                      text='Sound Effects',
                                                      manager=manager,
                                                      visible=True)
    sound_effects = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((screen_width//2 - 200, 300), (400, 40)),
                                                           start_value=100,
                                                           value_range=(0, 100),
                                                           manager=manager,
                                                           visible=True)

    measurements_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen_width//2 - 200, 380), (400, 50)),
                                                       text='Measurements',
                                                       manager=manager,
                                                       visible=True)
    colour_scheme_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen_width//2 - 200, 460), (400, 50)),
                                                        text='Colour Scheme',
                                                        manager=manager,
                                                        visible=True)

    back_button = Button(pygame.Rect((screen_width//2 - 200, 540), (400, 50)), visible=False)



black = (0, 0, 0)
green = (0, 255, 0)
grey = (128, 128, 128)
blue = (0, 0, 255) 

font = pygame.font.Font(None, 60)
status_font = pygame.font.Font(None, 40) 

button_width = 400 
button_height = 100 

button_texts = ["Start", "Configure", "Panic"]

sound1 = pygame.mixer.Sound('C:/Users/Danie/OneDrive/Desktop/Sublime Coding/Nuclear/GEIGERCOUNTER.mp3')
sound2 = pygame.mixer.Sound('C:/Users/Danie/OneDrive/Desktop/Sublime Coding/Nuclear/MENU INTRO.mp3')

buttons = [Button(pygame.Rect(screen_width//4 - button_width//2 - 100, screen_height//3 + i*150, button_width, button_height)) for i in range(3)]

def draw_button(screen, button_rect, color, text_surface):
    pygame.draw.rect(screen, color, button_rect.rect, 3)  
    screen.blit(text_surface, (button_rect.rect.x + button_rect.rect.width // 2 - text_surface.get_width() // 2,
                               button_rect.rect.y + button_rect.rect.height // 2 - text_surface.get_height() // 2))  


def display_bsod(screen, buttons):
    for button in buttons:
        button.visible = False
    screen.fill(blue)
    bsod_image = pygame.image.load("C:/Users/Danie/Downloads/mFxX21T-blue-screen-of-death-wallpaper.jpg").convert()
    bsod_image = pygame.transform.smoothscale(bsod_image, (screen_width, screen_height))
    bsod_sound = pygame.mixer.Sound("C:/Users/Danie/Downloads/blue-screen-of-death.mp3")
    bsod_sound.play()
    screen.blit(bsod_image, (screen_width // 2 - bsod_image.get_width() // 2, screen_height // 2 - bsod_image.get_height() // 2))
    pygame.display.flip()
    time.sleep(5)
    screen.fill(black)
    for button in buttons:
        button.visible = True
    time.sleep(5)





image = pygame.image.load(r'C:\Users\Danie\Downloads\OIG.jpeg')

new_width = 500
new_height = 500

image = pygame.transform.scale(image, (new_width, new_height))

counter = 0
particles = []
show_gui = False
show_menu = True

position = (screen_width // 2 - new_width // 2, screen_height // 2 - new_height // 2)
configure_clicked = False

running = True


while running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if back_button.rect.collidepoint(mouse_pos) and back_button.visible:
                print("Back button clicked!")
                configure_clicked = False  
                back_button.visible = False  
                for gui_element in [title, master_volume_label, master_volume, music_label, music, sound_effects_label, sound_effects, measurements_button, colour_scheme_button]:
                    gui_element.kill()  
                for button in buttons:
                    button.visible = True
            else:
                for i in range(len(buttons)):
                    if buttons[i].rect.collidepoint(mouse_pos) and buttons[i].visible:
                        print(f"{button_texts[i]} button clicked!")
                        if button_texts[i] == "Configure":
                            create_gui()  
                            configure_clicked = True  
                            buttons.append(back_button)  
                            back_button.visible = True 
                            buttons.append(back_button)  
                        elif buttons[i].rect.collidepoint(mouse_pos) and buttons[i].visible:
                            print(f"{button_texts[i]} button clicked!")
                            if button_texts[i] == "Panic":
                                sound1.stop()
                                sound2.stop()
                                display_bsod(screen, buttons)
        manager.process_events(event)
    manager.update(time_delta)




    master_volume_value = master_volume.get_current_value() / 100  
    music_value = music.get_current_value() / 100
    sound_effects_value = sound_effects.get_current_value() / 100

    sound1.set_volume(master_volume_value * music_value)  
    sound2.set_volume(master_volume_value * sound_effects_value)  


    screen.fill(black)

    if configure_clicked:
        manager.draw_ui(screen)
        if back_button.visible:  
            button_surface = font.render("Back", True, green)  
            draw_button(screen, back_button, grey if back_button.rect.collidepoint(pygame.mouse.get_pos()) else green , button_surface) 
    else:
        title_surface = font.render("NUCLEAR SIMULATOR", True, green)
        screen.blit(title_surface, (20, 20))
        for i in range(3):
            if buttons[i].visible:
                button_surface = font.render(button_texts[i], True, green)
                draw_button(screen, buttons[i], grey if buttons[i].rect.collidepoint(pygame.mouse.get_pos()) else green , button_surface) 
        if all(button.visible for button in buttons):
            status_box = pygame.Rect(screen_width//2 - button_width//2 , screen_height - screen_height//4 , button_width , button_height)
            
            status_text_surface = status_font.render("Authentication Status:", True, green) 
            
            verified_text_surface = font.render("Verified", True , green)
            
            screen.blit(status_text_surface , (status_box.x + status_box.width//2 - status_text_surface.get_width()//2 , screen_height - status_text_surface.get_height() - verified_text_surface.get_height())) 
            screen.blit(verified_text_surface , (status_box.x + status_box.width//2 - verified_text_surface.get_width()//2 , screen_height - verified_text_surface.get_height()))


    if show_gui:
        manager.draw_ui(screen)

    sound1.play(-1) 
    sound2.play(-1)  
    counter += 1

    if counter % 5 != 0 and not configure_clicked:
       screen.blit(image, position)
    for particle in particles:
        particle['pos'][0] += particle['vel'][0]
        particle['pos'][1] += particle['vel'][1]
        particle['life'] -= 1
        particle['size'] -= 0.1  
        pygame.draw.circle(screen, (255, 255, 255), (int(particle['pos'][0]), int(particle['pos'][1])), int(particle['size']))
    particles = [particle for particle in particles if particle['life'] > 0 and particle['size'] > 0]

    if len(particles) < 100:
        particles.append({
            'pos': [random.randint(position[0], position[0] + new_width), random.randint(position[1], position[1] + new_height)], 
            'vel': [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)],  
            'life': random.randint(10, 50),
            'size': random.randint(2, 5),  
        })

    pygame.display.flip()

pygame.quit()
sys.exit()

