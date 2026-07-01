import pygame
import time
import random
from data.sounds import *
from data.game_images import IMAGES
from engine.images import Images
from engine.text import Text
from save.save import *
import pygame
from engine.richpresense import RichPresense
from engine.animatronic import Animatronic
from engine.mixer import MixerMusic
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


VERSION = "1.0.1.2"


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
CHANNEL_SFX = {3,4,5,6,7,8,9,10,11,12,13,14,15}
CHANNEL_VOICE = {}


FONT_PATH = "./assets/fonts//OCRAEXT.TTF"
FONT_SIZE = [50,40,35,30,25,20,15]

"""""""""""
Fonts 
"""""""""""
CLOCK = pygame.font.Font(FONT_PATH, int(FONT_SIZE[0] * UI_SCALE))
H1 = pygame.font.Font(FONT_PATH, int(FONT_SIZE[1] * UI_SCALE))
H2 = pygame.font.Font(FONT_PATH, int(FONT_SIZE[2] * UI_SCALE))
H3 = pygame.font.Font(FONT_PATH, int(FONT_SIZE[3] * UI_SCALE))
H4 = pygame.font.Font(FONT_PATH, int(FONT_SIZE[4] * UI_SCALE))
H5 = pygame.font.Font(FONT_PATH, int(FONT_SIZE[5] * UI_SCALE))
P  = pygame.font.Font(FONT_PATH, int(FONT_SIZE[6] * UI_SCALE))

def drawMenu(elapsed_time, menu_elapsed_time,texts, img, CUSTOM_NIGHT_SCROLL, SETTINGS_SCROLL):   
    SCREEN.fill("black")
    layered=None
    scroll_y = CUSTOM_NIGHT_SCROLL
    config_x = SETTINGS_SCROLL
    for image in img:

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

def drawIngame(player, elapsed_time, texts, img):
    SCREEN.fill("black")
    pygame.draw.rect(SCREEN, "red", player)
    for image in img:
        if image.get_id() != "fadein":
            surface = image.get_scr().copy()
            surface.set_alpha(image.get_alpha())
            x = int(image.get_x() * UI_SCALE)
            y = int(image.get_y() * UI_SCALE)
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
    start_timer=0
    menu_start_time = time.time()
    menu_elapsed_time = 0
    LOAD_NIGHT_TIMER = 0
    night_timer=0
    hour=-4

    run = True

    player = pygame.Rect(0, HEIGHT * 0.5, PLAYER_WIDTH, PLAYER_HEIGHT)
    player_x = 0.0

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    

# Animatronicos


    maurello=Animatronic(1,"Maurello",get_fromSave("animatronics.Maurello"))


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

    INGAME_IMG = create_images("INGAME", WIDTH, HEIGHT, UI_SCALE)

    img=[]
    img=WARNING_IMG.copy()



    while run:
        set_fromSave("animatronics.Maurello", maurello)
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
                            match image.get_subid():
                                case "MaurelloAddAi":
                                    maurello.add_ai(1)


        keys = pygame.key.get_pressed()

        if SUBGAMESTATE == "CustomNight":
            CUSTOM_NIGHT_SCROLL = max(
                -500,
                min(
                    CUSTOM_NIGHT_SCROLL,
                    0
                )
            )
        if GAMESTATE == "menu":
            if SUBGAMESTATE == "warningscreen":
                if MENUSTATE == "fade_in":
                    for text in texts:
                        text.set_alpha(
                            text.get_alpha() +
                            fadein_speed * delta_time
                        )
                    for image in img:
                        image.set_alpha(
                            image.get_alpha() +
                            fadein_speed * delta_time
                        )
                    if texts[0].get_alpha() >= 255:
                        MENUSTATE = "wait"

                elif MENUSTATE == "wait":
                    timer += delta_time
                    if timer >= 4:
                        MENUSTATE = "fade_out"

                elif MENUSTATE == "fade_out":
                    for image in img:
                        image.set_alpha(
                            image.get_alpha() -
                            fadeout_speed * delta_time
                        )
                    for text in texts:
                        text.set_alpha(
                            text.get_alpha() -
                            fadeout_speed * delta_time,
                        )
                        print(text.get_alpha())
                    if texts[0].get_alpha() <= 0:
                        pygame.time.wait(500)
                        SUBGAMESTATE = "CustomNight"
                        texts = CUSTOM_NIGHT_TEXTS  
                        img=CUSTOM_NIGHT_IMG
                        menu_start_time = time.time()
                        mixer_sound.play(Custom_Menu,0.1,CHANNEL_MENU,True)

                        discord.update_rpc("Custom Night", "In a Menu:")
                current_time=pygame.time.get_ticks()
                if mouse_clicked:
                    print(mouse_clicked)
                    print("Changing menu")
                    SUBGAMESTATE = "CustomNight"
                    mixer_sound.play(Custom_Menu,0.1,CHANNEL_MENU,True)

                    texts = CUSTOM_NIGHT_TEXTS
                    img=CUSTOM_NIGHT_IMG
                    menu_start_time = time.time()
                    discord.update_rpc("Custom Night", "In a Menu:")
                    
            if SUBGAMESTATE == "CustomNight":
                if SETTINGS_STATE == "opening":
                    SETTINGS_SCROLL += SETTINGS_SPEED * delta_time

                    if SETTINGS_SCROLL >= 1050:
                        SETTINGS_SCROLL = 1050
                        SETTINGS_STATE = "open"
                        for text in texts:
                            if text.get_id() == 8:
                                text.set_trigeable(True)

                elif SETTINGS_STATE == "closing":
                    SETTINGS_SCROLL -= SETTINGS_SPEED * delta_time

                    if SETTINGS_SCROLL <= 0:
                        SETTINGS_SCROLL = 0
                        SETTINGS_STATE = "closed"
                        for text in texts:
                            if text.get_id() == 7:
                                text.set_trigeable(True)
            if SUBGAMESTATE == "LoadNight":
                LOAD_NIGHT_TIMER += delta_time
                if hour == -4:
                    texts[1].set_text("8")
                    texts[1].set_x(590)
                    texts[2].set_text("PM")
                elif hour == -2:
                    texts[1].set_text("10")
                    texts[2].set_text("PM")
                    
                if LOAD_NIGHT_TIMER < 0.12:
                    img[0].set_alpha(255)
                    img[1].set_alpha(0)
                    img[2].set_alpha(0)
                    texts[0].set_alpha(texts[0].get_alpha()+15)
                    texts[1].set_alpha(texts[0].get_alpha()+15)
                    texts[2].set_alpha(texts[0].get_alpha()+15)
                    texts[3].set_alpha(0)

                elif LOAD_NIGHT_TIMER < 0.24:
                    img[0].set_alpha(0)
                    img[1].set_alpha(255)
                    img[2].set_alpha(0)
                    texts[0].set_alpha(texts[0].get_alpha()+15)
                    texts[1].set_alpha(texts[0].get_alpha()+15)
                    texts[2].set_alpha(texts[0].get_alpha()+15)
                    texts[3].set_alpha(0)

                elif LOAD_NIGHT_TIMER < 0.36:
                    img[0].set_alpha(0)
                    img[1].set_alpha(0)
                    img[2].set_alpha(255)
                    texts[0].set_alpha(texts[0].get_alpha()+15)
                    texts[1].set_alpha(texts[0].get_alpha()+15)
                    texts[2].set_alpha(texts[0].get_alpha()+15)
                    texts[3].set_alpha(0)
                    texts[3].set_y(640)

                elif LOAD_NIGHT_TIMER > 0.36 and LOAD_NIGHT_TIMER < 3.50 and texts[0].get_alpha() <= 255:
                    img[2].set_alpha(0)
                    texts[0].set_alpha(texts[0].get_alpha()+15)
                    texts[1].set_alpha(texts[0].get_alpha()+15)
                    texts[2].set_alpha(texts[0].get_alpha()+15)
                elif LOAD_NIGHT_TIMER > 3.50 and LOAD_NIGHT_TIMER < 10.00:
                    if LOAD_NIGHT_TIMER >= 9.50 and not MUSIC_STOPPED:
                        mixer_sound.crossfade(CHANNEL_MENU,CHANNEL_AMBIENT,OfficeAmbience[random.randrange(4)],volume=0.08,looping=True,fade_ms=2500)
                        MUSIC_STOPPED = True
                    img[3].set_alpha(255)
                    texts[0].set_alpha(0)
                    texts[1].set_alpha(0)
                    texts[2].set_alpha(0)
                    texts[3].set_alpha(255)
                else:
                    MUSIC_STOPPED = False
                    texts = INGAME_TEXTS
                    img = INGAME_IMG
                    GAMESTATE = "ingame"    
            drawMenu(elapsed_time, menu_elapsed_time,texts, img, CUSTOM_NIGHT_SCROLL, SETTINGS_SCROLL)
        elif GAMESTATE == "ingame":    
            try:
                discord.update_rpc(state=f"No Challenge ({texts[0].get_text()} {texts[1].get_text()})", details="In a Night")
            except:
                pass
            night_timer += delta_time
            if night_timer >= 0.0 and night_timer <= 1.0:
                for text in texts:
                    if hour == -4:
                        if text.get_subid() == "Period":
                            text.set_text("PM")
                        if text.get_subid() == "Hour":
                            text.set_text("8")
                            text.set_x(1170)
                    elif hour == -2:
                        if text.get_subid() == "Period":
                            text.set_text("PM")
                        if text.get_subid() == "Hour":
                            text.set_text("10")
                            text.set_x(1150)
                    elif hour == 0:
                        if text.get_subid() == "Period":
                            text.set_text("AM")
                        if text.get_subid() == "Hour":
                            text.set_text("12")
                    elif hour == 1:
                        if text.get_subid() == "Hour":
                            text.set_text("1")
                            text.set_x(1170)
            if night_timer > 75.0:
                hour += 1
                texts[0].set_text(str(int(texts[0].get_text())+1))
                night_timer = 0
            if INGAME_FADE_ALPHA > 0:
                INGAME_FADE_ALPHA -= INGAME_FADE_SPEED * delta_time

                if INGAME_FADE_ALPHA < 0:
                    INGAME_FADE_ALPHA = 0
                img[3].set_alpha(INGAME_FADE_ALPHA)
                
            if mouse_x < LEFT_BORDER:
                distance = LEFT_BORDER - mouse_x
                speed = (distance / LEFT_BORDER) * MAX_SPEED
                player_x -= speed * delta_time

            elif mouse_x > RIGHT_BORDER:
                distance = mouse_x - RIGHT_BORDER
                speed = (distance / (WIDTH - RIGHT_BORDER)) * MAX_SPEED
                player_x += speed * delta_time
            player_x = max(0, min(player_x, WIDTH - player.width))
            player.x = int(player_x)

            drawIngame(player, elapsed_time, texts, img)
    pygame.quit()
# The game will only start only if this python file is executed.
if __name__ == "__main__":
    main()
