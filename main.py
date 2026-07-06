import pygame
import time
import random
from data.sounds import *
from data.game_images import IMAGES
from engine.images import Images
from engine.animation import Animation
from engine.text import Text
from engine.richpresense import RichPresense
from engine.animatronic import Animatronic
from engine.mixer import MixerMusic
from engine.doors.door import Door
from save.save import *
from states.warning_screen import warning_main
from states.custom_night import custom_night_main
from states.load_night import load_night_main
from states.ingame import ingame_main
pygame.font.init()
mixer_sound=MixerMusic()
mixer_sound.connect()
#Discord Rich Presense
discord = RichPresense()
#save json

create_save()

SAVE = load_save()

#setup
BASE_WIDTH, BASE_HEIGHT = 1280, 720
#1040, 585
#853, 480
WIDTH, HEIGHT = 1280, 720 # screen resolution
UI_SCALE = HEIGHT / BASE_HEIGHT
print(F"Image Scale. {UI_SCALE} (16:9)")


VERSION = "1.0.1.9"


SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
LEFT_BORDER = WIDTH * 0.45
RIGHT_BORDER = WIDTH * 0.55

logo = pygame.image.load("./assets/sprites/Icon.png")
pygame.display.set_icon(logo)
pygame.display.set_caption(f"Five Nights With Your Mother {VERSION}")


PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

MAX_SPEED = 600
if HEIGHT == 1080:
    MAX_SPEED = 900

"""""""""""
Sound
"""""""""""
CHANNEL_MENU = 0
CHANNEL_AMBIENT = 1
CHANNEL_MUSIC = 2
CHANNEL_SFX = list(range(3,16))
CHANNEL_VOICE = {}



"""""""""""
Fonts 
"""""""""""
FONT_PATH = "./assets/fonts//OCRAEXT.TTF"
FONT_SIZE = [50,40,35,30,25,20,15]

CLOCK = pygame.font.Font(FONT_PATH, int(FONT_SIZE[0] * UI_SCALE))
H1 = pygame.font.Font(FONT_PATH, int(FONT_SIZE[1] * UI_SCALE))
H2 = pygame.font.Font(FONT_PATH, int(FONT_SIZE[2] * UI_SCALE))
H3 = pygame.font.Font(FONT_PATH, int(FONT_SIZE[3] * UI_SCALE))
H4 = pygame.font.Font(FONT_PATH, int(FONT_SIZE[4] * UI_SCALE))
H5 = pygame.font.Font(FONT_PATH, int(FONT_SIZE[5] * UI_SCALE))
P  = pygame.font.Font(FONT_PATH, int(FONT_SIZE[6] * UI_SCALE))


#surface es el dibujado a fondo
#screen.blit toma el surface y lo dibuja en pantalla
def drawMenu(elapsed_time, menu_elapsed_time,texts, img, CUSTOM_NIGHT_SCROLL, SETTINGS_SCROLL, delta_time):   
    SCREEN.fill("black")
    layered=None
    scroll_y = CUSTOM_NIGHT_SCROLL
    config_x = SETTINGS_SCROLL
    for image in img:

        if isinstance(image, Animation):
            image.update(delta_time)
        surface = image.get_scr().copy()
        surface.set_alpha(image.get_alpha())
        x = int(image.get_x() * UI_SCALE)
        match image.get_id():
            case "CN":
                y = int(
                    (image.get_y() + scroll_y)
                    * UI_SCALE
                )
            case _:
                y = int(image.get_y() * UI_SCALE)
        if image.is_trigeable():
            rect = surface.get_rect(topleft=(x, y))
            image.set_rect(rect)
            pygame.draw.rect(
                SCREEN,
                "green",
                rect,
                1
            )
        if image.get_id() != "GradientMask":
            SCREEN.blit(surface, (x, y))

#
#   ESTE BUCLE HACE QUE CUALQUIER OBJETO CON SUB ID DE 'LAYERED' ESTE DEBAJO DE IMAGENES
#

    for text in texts:
        if text.get_subid() == "layered":
            surface=text.get_size().render(text.get_text(), 1, text.get_color())
            surface.set_alpha(text.get_alpha())
            x = int(text.get_x() * UI_SCALE)
            y = int((text.get_y() + scroll_y) * UI_SCALE)
            match text.get_id():
                case 111:
                    if int(text.get_text()) > 9:
                        text.set_x(140)
                    else:
                        text.set_x(148)
            SCREEN.blit(surface, (x, y))
    for image in img:
        if image.get_id() == "GradientMask":
            surface = image.get_scr().copy()
            surface.set_alpha(image.get_alpha())
            x = int(image.get_x() * UI_SCALE)
            y = int(image.get_y() * UI_SCALE)
            SCREEN.blit(surface, (x, y))    

    for text in texts:
        if text.get_subid() == "2ndlayered":
            surface=text.get_size().render(text.get_text(), 1, text.get_color())
            surface.set_alpha(text.get_alpha())
            x = int(text.get_x() * UI_SCALE)
            y = int(text.get_y() * UI_SCALE)
            if text.is_trigeable():
                rect = surface.get_rect(topleft=(x, y))
                text.set_rect(rect)
                pygame.draw.rect(SCREEN, "red", rect, 1)
            SCREEN.blit(surface, (x, y))
    for image in img:
        if image.get_id() == "Config":
            if isinstance(image, Animation):
                image.update(delta_time)
            surface = image.get_scr().copy()
            surface.set_alpha(image.get_alpha())
            x = int((image.get_x() + config_x) * UI_SCALE)
            y = int(image.get_y() * UI_SCALE)
            SCREEN.blit(surface, (x, y)) 
    for text in texts:
        if text.get_subid() == "Config":
            surface=text.get_size().render(text.get_text(), 1, text.get_color())
            surface.set_alpha(text.get_alpha())
            x = int((text.get_x() + config_x) * UI_SCALE)
            y = int(text.get_y() * UI_SCALE)
            if text.is_trigeable():
                rect = surface.get_rect(topleft=(x, y))
                text.set_rect(rect)
                pygame.draw.rect(SCREEN, "red", rect, 1)
            SCREEN.blit(surface, (x, y))

#
#   AQUI CONTINUA EL DIBUJADO NORMAL.
#

    for text in texts:
        if text.get_subid() != "layered" and text.get_subid() != "2ndlayered" and text.get_subid() != "Config":
            x = int(text.get_x() * UI_SCALE)

            match text.get_id():
                case 111:
                    y = int(
                        (text.get_y() + scroll_y)
                        * UI_SCALE
                    )
                    if int(text.get_text()) > 9:
                        text.set_x(140)
                    else:
                        text.set_x(148)
                case _:
                    y = int(text.get_y() * UI_SCALE)
                    
            for line_index, surface in enumerate(
                text.get_rendered_lines()
            ):

                surface.set_alpha(text.get_alpha())

                SCREEN.blit(
                    surface,
                    (x, y + (line_index * surface.get_height())))
            if text.is_trigeable():
                rect = surface.get_rect(topleft=(x, y))
                text.set_rect(rect)
                pygame.draw.rect(SCREEN, "red", rect, 1)

    time_text = H4.render(f"Time: {round(elapsed_time)}s", 1, "white")
    time_text1 = H4.render(f"Menu: {round(menu_elapsed_time)}s", 1, "white")
    SCREEN.blit(time_text, (10, 10))
    SCREEN.blit(time_text1, (10, 40))
    pygame.display.update()

def drawIngame(player, elapsed_time, texts, img, delta_time):
    SCREEN.fill("black")
    pygame.draw.rect(SCREEN, "red", player)
    for image in img:
        if image.get_id() != "fadein":
            if isinstance(image, Animation):
                image.update(delta_time)
            surface = image.get_scr().copy()
            surface.set_alpha(image.get_alpha())
            x = int(image.get_x() * UI_SCALE)
            y = int(image.get_y() * UI_SCALE)
            rect = surface.get_rect(topleft=(x, y))
            image.set_rect(rect)
            SCREEN.blit(surface,(x, y))
    for text in texts:
        x = int(text.get_x() * UI_SCALE)
        y = int(text.get_y() * UI_SCALE)

        for line_index, surface in enumerate(
            text.get_rendered_lines()
        ):
            surface.set_alpha(text.get_alpha())

            SCREEN.blit(surface,(x,y + (line_index * surface.get_height())))
    for image in img:
        if image.get_id() == "fadein":
            surface = image.get_scr().copy()
            surface.set_alpha(image.get_alpha())

            SCREEN.blit(surface,(image.get_x(), image.get_y()))
    time_text = H4.render(f"Time: {round(elapsed_time)}s", 1, "white")
    SCREEN.blit(time_text, (10, 10))

    pygame.display.update()

def create_images(group, width, height, scale):

    images = []

    for data in IMAGES[group]:

        surface = pygame.image.load(data["path"]).convert_alpha()

        if "size" in data:
            surface = pygame.transform.smoothscale(
                surface,
                data["size"]
            )

        images.append(
            Images(
                data["id"],
                surface,
                data["trigger"],
                data["alpha"],
                data["x"],
                data["y"],
                width,
                height,
                scale,
                data["fullscreen"],
                data["subid"]
            )
        )

    return images

def get_image(images, image_id, image_subid=None):
    for image in images:
        if (image.get_id() == image_id and
            (image_subid is None or image.get_subid() == image_subid)):
            return image

    return None

def main():
    discord.initiate_rpc()

    GAMESTATE="menu"
    SUBGAMESTATE="warningscreen"
    MENUSTATE="fade_in"

    CUSTOM_NIGHT_SCROLL = -10
    SETTINGS_SCROLL = 0
    SETTINGS_SPEED = 4800
    SETTINGS_STATE = "closed"
    MUSIC_STOPPED = False

    INGAME_FADE_ALPHA = 255
    INGAME_FADE_SPEED = 500

    fadein_speed = 712.5
    fadeout_speed = 166.30
    timer=0
    menu_start_time = time.time()
    menu_elapsed_time = 0
    LOAD_NIGHT_TIMER = 0
    night_timer=0

    run = True

    player = pygame.Rect(0, HEIGHT * 0.5, PLAYER_WIDTH, PLAYER_HEIGHT)
    player_x = 0.0

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    
#   Estos son const o variables que se usan en el game loop de las noches.

#   Dirige el tiempo (-4 = 8 PM, -2 = 10 PM, 0 = 12 AM)
    hour=-4
#   Indica que tipo de noche (1 = Normal... 4 = XXL)
    night_type = 1
    officetype = "Compact"

#   Animatronicos

    maurello=Animatronic(1,"Maurello",get_fromSave("animatronics.Maurello.ai"))
    furry=Animatronic(1,"Maurello",get_fromSave("animatronics.Maurello.ai"))

#   TEXTOS


    WARNING_TEXTS = [
        Text(0,"Warning", H3, "white", 0, False, 575, 300),

        Text(0,
            "This game was made with only joke purposes \n"
            "     and must no be taken offensively. \n"
            "      This game contains loud noises, \n"
            "             and jumpscares.",
            H3,
            "white",
            0,
            False,
            275,
            350
        )
    ]

    CUSTOM_NIGHT_TEXTS = [
        Text(0, "Custom Night", H1, "white", 255, False, 450, 50,"2ndlayered"),
        Text(1, "Set All 0",H2,"white",255,True,1070,430),
        Text(2, "Add All 1",H2,"white",255,True,1070,475),
        Text(3, "Set All 5",H2,"white",255,True,1070,520),
        Text(4, "Set All 10",H2,"white",255,True,1065,565),
        Text(5, "Set All 20",H2,"white",255,True,1065,610),
        Text(6, "START",H1,"white",255,True,1110,665),
        Text(7, "Settings",H2,"white",255,True,1075,370),
        Text(8, "Back", H1, "white", 255, True, -1020, 640, "Config"),
        Text(101, str(maurello.get_nombre()), H3, "white", 255, False, 90 ,202,"layered"),
        Text(111, str(maurello.get_ai()), H1, "white", 255, False, 148 ,365,"layered"),
    ]

    RANDOM_TIPS = [
        "If you watch cam H1 while recharging Cat Spawner, It'll charge twice as fast!",
        "You can get rid of Pou by pressing 'Shift' if he's in a top position.",
        "You can slow down Sonic when the cameras are up, making him unable to jump cams. \nWell... most of the time.",
        "Bob doesn't like being watched.",
        "Hold 'Shift' to keep using the keyboard shortcuts when the password \nprompt is up!",
        "Agressive Dad makes noise when reaching the closet, but regular dad doesn't.",
        "Hellish can imitate hazards like Darkbloom, be careful with what you hear.",

    ]

    LOAD_NIGHT_TEXTS = [
        Text(0, "\n Night", H1, "white", 0, False, 550, 280),
        Text(1, "12", H1, "white", 0, False, 570, 280, "Hour"),
        Text(2, "AM", H1, "white", 0, False, 630, 280, "Period"),
        Text(3, "Tip: " + RANDOM_TIPS[random.randrange(7)], H4, "white", 0, False, 30, 800, "Tips")
    ]

    INGAME_TEXTS = [
        Text(0, "12", H1, "white", 255, False, 1150, 15, "Hour"),
        Text(0, "AM", H1, "white", 255, False, 1210, 15, "Period"),
        Text(0, "Custom Night", H4, "white", 255, False, 1080, 60),
    ]


    texts=[]
    texts=WARNING_TEXTS.copy()


#   IMAGENES


    WARNING_IMG = create_images("WARNING", WIDTH, HEIGHT, UI_SCALE)

    CUSTOM_NIGHT_IMG = create_images("CUSTOM_NIGHT", WIDTH, HEIGHT, UI_SCALE)

    LOAD_NIGHT_IMG = create_images("LOAD_NIGHT", WIDTH, HEIGHT, UI_SCALE)

    INGAME_IMG = create_images("INGAME_COMPACTOFFICE", WIDTH, HEIGHT, UI_SCALE)

    img=[]
    img=WARNING_IMG.copy()



    while run:
        mouse_clicked = False
        delta_time = clock.tick(60) / 1000
        elapsed_time = time.time() - start_time
        menu_elapsed_time = time.time() - menu_start_time
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEWHEEL and SUBGAMESTATE == "CustomNight":

                CUSTOM_NIGHT_SCROLL += event.y * 25
            for text in texts:
                match text.get_id():
                    case 111:
                        text.set_text(
                            str(maurello.get_ai())
                        )
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
                if GAMESTATE == "menu" and SUBGAMESTATE == "CustomNight":
                    for text in texts:
                        if text.is_trigeable():
                            rect = text.get_rect()
                            if rect and rect.collidepoint(mouse_x, mouse_y):
                                match text.get_id():
                                    case 1:
                                        maurello.set_ai(0)
                                    case 2:
                                        maurello.add_ai(1)
                                    case 3:
                                        maurello.set_ai(5)
                                    case 4:
                                        maurello.set_ai(10)
                                    case 5:
                                        maurello.set_ai(20)
                                    case 6:
                                        print("Start game")
                                        menu_start_time = time.time()
                                        mixer_sound.set_volume(CHANNEL_MENU, 0.05)
                                        texts = LOAD_NIGHT_TEXTS
                                        img = LOAD_NIGHT_IMG
                                        discord.update_rpc("Loading night","In a Menu")
                                        SUBGAMESTATE = "LoadNight"
                                    case 7:
                                        mixer_sound.set_volume(CHANNEL_MENU, 0.05)
                                        text.set_trigeable(False)
                                        SETTINGS_STATE = "opening"
                                        
                                    case 8:
                                        mixer_sound.set_volume(CHANNEL_MENU,0.1)
                                        text.set_trigeable(False)
                                        SETTINGS_STATE = "closing"

                    for image in img:
                        if image.is_trigeable():
                            rect = image.get_rect()
                            if rect and rect.collidepoint(mouse_x, mouse_y):
                                match image.get_subid():
                                    case "MaurelloMinusAi":
                                        maurello.minus_ai(1)
                                    case "MaurelloAddAi":
                                        maurello.add_ai(1)
                elif GAMESTATE == "ingame":
                    for text in texts:
                        pass
                    for image in img:
                        if not image.is_trigeable():
                            continue

                        rect = image.get_rect()
                        if not rect or not rect.collidepoint(mouse_x, mouse_y):
                            continue

                        if image.get_id().endswith("Button"):
                                pass        
        if GAMESTATE == "menu":
            if SUBGAMESTATE == "warningscreen":     
                (SUBGAMESTATE, MENUSTATE, timer, menu_start_time) = warning_main(
                    texts=texts,
                    img=img,
                    delta_time=delta_time,
                    fadein_speed=fadein_speed,
                    fadeout_speed=fadeout_speed,
                    timer=timer,
                    menu_state=MENUSTATE,
                    mouse_clicked=mouse_clicked,
                    menu_start_time=menu_start_time,
                    mixer_sound=mixer_sound,
                    discord=discord,
                    channel_menu=CHANNEL_MENU
                )

                    
            if SUBGAMESTATE == "CustomNight":
                texts = CUSTOM_NIGHT_TEXTS
                img = CUSTOM_NIGHT_IMG
                menu_start_time = time.time()
                (CUSTOM_NIGHT_SCROLL,SETTINGS_SCROLL,SETTINGS_STATE) = custom_night_main(
                    texts=texts,
                    delta_time=delta_time,
                    custom_night_scroll=CUSTOM_NIGHT_SCROLL,
                    settings_scroll=SETTINGS_SCROLL,
                    settings_speed=SETTINGS_SPEED,
                    settings_state=SETTINGS_STATE
                )
            if SUBGAMESTATE == "LoadNight":
                (
                    GAMESTATE,
                    SUBGAMESTATE,
                    LOAD_NIGHT_TIMER,
                    MUSIC_STOPPED
                ) = load_night_main(

                    texts=texts,
                    img=img,
                    delta_time=delta_time,
                    load_night_timer=LOAD_NIGHT_TIMER,
                    music_stopped=MUSIC_STOPPED,
                    hour=hour,
                    mixer_sound=mixer_sound,
                    channel_menu=CHANNEL_MENU,
                    channel_ambient=CHANNEL_AMBIENT,
                    office_ambience=OfficeAmbience
                )

            drawMenu(elapsed_time, menu_elapsed_time,texts, img, CUSTOM_NIGHT_SCROLL, SETTINGS_SCROLL, delta_time)


        elif GAMESTATE == "ingame":
            
            texts = INGAME_TEXTS
            img = INGAME_IMG

            (player_x,night_timer,hour,INGAME_FADE_ALPHA) = ingame_main(

                texts=texts,
                img=img,

                player=player,
                player_x=player_x,
                mouse_x=mouse_x,

                delta_time=delta_time,

                night_timer=night_timer,
                hour=hour,

                fade_alpha=INGAME_FADE_ALPHA,
                fade_speed=INGAME_FADE_SPEED,

                left_border=LEFT_BORDER,
                right_border=RIGHT_BORDER,
                width=WIDTH,
                max_speed=MAX_SPEED,

                discord=discord
            )
            maurello.update(delta_time)
            drawIngame(player, elapsed_time, texts, img, delta_time)
    pygame.quit()
# The game will only start only if this python file is executed.
if __name__ == "__main__":
    main()
