import pygame
import time
import random

from data.sounds import *
from data.game_images import IMAGES

from engine.images import Images
from engine.animation import Animation
from engine.text import Text

from save.save import *

from engine.richpresense import RichPresense
from engine.animatronic import Animatronic
from engine.mixer import MixerMusic

from states.warning_screen import warning_main
from states.custom_night import custom_night_main
from states.load_night import load_night_main
from states.ingame import ingame_main

from scripts.power import PowerScript


class Game:

    def __init__(self):

        pygame.init()
        pygame.font.init()

        # -------------------------
        # Save
        # -------------------------

        create_save()
        self.SAVE = load_save()

        # -------------------------
        # Discord
        # -------------------------

        self.discord = RichPresense()

        # -------------------------
        # Audio
        # -------------------------

        self.mixer = MixerMusic()
        self.mixer.connect()

        # -------------------------
        # Resolution
        # -------------------------

        self.BASE_WIDTH = 1280
        self.BASE_HEIGHT = 720

        self.WIDTH = 1280
        self.HEIGHT = 720

        self.UI_SCALE = self.HEIGHT / self.BASE_HEIGHT

        print(f"Image Scale: {self.UI_SCALE}")

        # -------------------------
        # Version
        # -------------------------

        self.VERSION = "1.0.2.2"

        # -------------------------
        # Window
        # -------------------------

        self.SCREEN = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )

        self.LEFT_BORDER = self.WIDTH * 0.45
        self.RIGHT_BORDER = self.WIDTH * 0.55

        logo = pygame.image.load(
            "./assets/sprites/Icon.png"
        )

        pygame.display.set_icon(logo)

        pygame.display.set_caption(
            f"Five Nights With Your Mother {self.VERSION}"
        )

        # -------------------------
        # Player
        # -------------------------

        self.PLAYER_WIDTH = 40
        self.PLAYER_HEIGHT = 60

        self.MAX_SPEED = 600

        if self.HEIGHT == 1080:
            self.MAX_SPEED = 900

        # -------------------------
        # Audio Channels
        # -------------------------

        self.CHANNEL_MENU = 0
        self.CHANNEL_AMBIENT = 1
        self.CHANNEL_MUSIC = 2

        self.CHANNEL_SFX = list(range(3, 16))
        self.CHANNEL_VOICE = {}

        # -------------------------
        # Fonts
        # -------------------------

        self.FONT_PATH = "./assets/fonts/OCRAEXT.TTF"

        self.FONT_SIZE = [
            50,
            40,
            35,
            30,
            25,
            20,
            15
        ]

        self.CLOCK = pygame.font.Font(
            self.FONT_PATH,
            int(self.FONT_SIZE[0] * self.UI_SCALE)
        )

        self.H1 = pygame.font.Font(
            self.FONT_PATH,
            int(self.FONT_SIZE[1] * self.UI_SCALE)
        )

        self.H2 = pygame.font.Font(
            self.FONT_PATH,
            int(self.FONT_SIZE[2] * self.UI_SCALE)
        )

        self.H3 = pygame.font.Font(
            self.FONT_PATH,
            int(self.FONT_SIZE[3] * self.UI_SCALE)
        )

        self.H4 = pygame.font.Font(
            self.FONT_PATH,
            int(self.FONT_SIZE[4] * self.UI_SCALE)
        )

        self.H5 = pygame.font.Font(
            self.FONT_PATH,
            int(self.FONT_SIZE[5] * self.UI_SCALE)
        )

        self.P = pygame.font.Font(
            self.FONT_PATH,
            int(self.FONT_SIZE[6] * self.UI_SCALE)
        )

        # -------------------------
        # Clock
        # -------------------------

        self.clock = pygame.time.Clock()

        self.start_time = time.time()
        self.menu_start_time = time.time()

        self.elapsed_time = 0
        self.menu_elapsed_time = 0
        self.delta_time = 0

        # -------------------------
        # Mouse
        # -------------------------

        self.mouse_x = 0
        self.mouse_y = 0

        self.mouse_clicked = False

        # -------------------------
        # Game States
        # -------------------------

        self.GAMESTATE = "menu"
        self.SUBGAMESTATE = "warningscreen"
        self.MENUSTATE = "fade_in"

        # -------------------------
        # Misc
        # -------------------------

        self.CUSTOM_NIGHT_SCROLL = -10

        self.SETTINGS_SCROLL = 0
        self.SETTINGS_SPEED = 4800
        self.SETTINGS_STATE = "closed"

        self.MUSIC_STOPPED = False

        self.INGAME_FADE_ALPHA = 255
        self.INGAME_FADE_SPEED = 500

        self.fadein_speed = 712.5
        self.fadeout_speed = 166.30

        self.timer = 0
        self.LOAD_NIGHT_TIMER = 0
        self.night_timer = 0

        # -------------------------
        # Player
        # -------------------------

        self.player = pygame.Rect(
            0,
            self.HEIGHT * 0.5,
            self.PLAYER_WIDTH,
            self.PLAYER_HEIGHT
        )

        self.player_x = 0.0

        # -------------------------
        # Night Variables
        # -------------------------

        self.hour = -4
        self.night_type = 1
        self.officetype = "Compact"

        self.LEFT_DOOR = "Open"
        self.RIGHT_DOOR = "Open"
        self.blackout = False

        # -------------------------
        # Runtime Containers
        # -------------------------

        self.texts = []
        self.images = []

        # -------------------------
        # Script Container 
        # -------------------------

        self.scripts = []

    def drawMenu(self):

        self.SCREEN.fill("black")

        scroll_y = self.CUSTOM_NIGHT_SCROLL
        config_x = self.SETTINGS_SCROLL

        #
        # IMÁGENES
        #

        for image in self.images:

            if isinstance(image, Animation):
                image.update(self.delta_time)

            surface = image.get_scr().copy()
            surface.set_alpha(image.get_alpha())

            x = int(image.get_x() * self.UI_SCALE)

            if image.get_id() == "CN":
                y = int((image.get_y() + scroll_y) * self.UI_SCALE)
            else:
                y = int(image.get_y() * self.UI_SCALE)

            if image.is_trigeable():

                rect = surface.get_rect(topleft=(x, y))
                image.set_rect(rect)

                pygame.draw.rect(
                    self.SCREEN,
                    "green",
                    rect,
                    1
                )

            if image.get_id() != "GradientMask":
                self.SCREEN.blit(surface, (x, y))

        #
        # TEXTOS LAYERED
        #

        for text in self.texts:

            if text.get_subid() != "layered":
                continue

            surface = text.get_size().render(
                text.get_text(),
                True,
                text.get_color()
            )

            surface.set_alpha(text.get_alpha())

            x = int(text.get_x() * self.UI_SCALE)
            y = int((text.get_y() + scroll_y) * self.UI_SCALE)

            if text.get_id() == 111:

                if int(text.get_text()) > 9:
                    text.set_x(140)
                else:
                    text.set_x(148)

            self.SCREEN.blit(surface, (x, y))

        #
        # Gradient
        #

        for image in self.images:

            if image.get_id() != "GradientMask":
                continue

            surface = image.get_scr().copy()
            surface.set_alpha(image.get_alpha())

            self.SCREEN.blit(
                surface,
                (
                    int(image.get_x() * self.UI_SCALE),
                    int(image.get_y() * self.UI_SCALE)
                )
            )

        #
        # SEGUNDA CAPA
        #

        for text in self.texts:

            if text.get_subid() != "2ndlayered":
                continue

            surface = text.get_size().render(
                text.get_text(),
                True,
                text.get_color()
            )

            surface.set_alpha(text.get_alpha())

            x = int(text.get_x() * self.UI_SCALE)
            y = int(text.get_y() * self.UI_SCALE)

            if text.is_trigeable():

                rect = surface.get_rect(topleft=(x, y))
                text.set_rect(rect)

                pygame.draw.rect(
                    self.SCREEN,
                    "red",
                    rect,
                    1
                )

            self.SCREEN.blit(surface, (x, y))

        #
        # CONFIG IMAGES
        #

        for image in self.images:

            if image.get_id() != "Config":
                continue

            if isinstance(image, Animation):
                image.update(self.delta_time)

            surface = image.get_scr().copy()
            surface.set_alpha(image.get_alpha())

            x = int((image.get_x() + config_x) * self.UI_SCALE)
            y = int(image.get_y() * self.UI_SCALE)

            self.SCREEN.blit(surface, (x, y))

        #
        # CONFIG TEXTS
        #

        for text in self.texts:

            if text.get_subid() != "Config":
                continue

            surface = text.get_size().render(
                text.get_text(),
                True,
                text.get_color()
            )

            surface.set_alpha(text.get_alpha())

            x = int((text.get_x() + config_x) * self.UI_SCALE)
            y = int(text.get_y() * self.UI_SCALE)

            if text.is_trigeable():

                rect = surface.get_rect(topleft=(x, y))
                text.set_rect(rect)

                pygame.draw.rect(
                    self.SCREEN,
                    "red",
                    rect,
                    1
                )

            self.SCREEN.blit(surface, (x, y))

        #
        # RESTO DE TEXTOS
        #

        for text in self.texts:

            if text.get_subid() in ("layered", "2ndlayered", "Config"):
                continue

            x = int(text.get_x() * self.UI_SCALE)

            if text.get_id() == 111:

                y = int((text.get_y() + scroll_y) * self.UI_SCALE)

                if int(text.get_text()) > 9:
                    text.set_x(140)
                else:
                    text.set_x(148)

            else:

                y = int(text.get_y() * self.UI_SCALE)

            for line_index, surface in enumerate(text.get_rendered_lines()):

                surface.set_alpha(text.get_alpha())

                self.SCREEN.blit(
                    surface,
                    (
                        x,
                        y + line_index * surface.get_height()
                    )
                )

            if text.is_trigeable():

                rect = surface.get_rect(topleft=(x, y))
                text.set_rect(rect)

                pygame.draw.rect(
                    self.SCREEN,
                    "red",
                    rect,
                    1
                )

        #
        # DEBUG
        #

        time_text = self.H4.render(
            f"Time: {round(self.elapsed_time)}s",
            True,
            "white"
        )

        menu_text = self.H4.render(
            f"Menu: {round(self.menu_elapsed_time)}s",
            True,
            "white"
        )

        self.SCREEN.blit(time_text, (10, 10))
        self.SCREEN.blit(menu_text, (10, 40))

        pygame.display.update() 
    def drawIngame(self):

        self.SCREEN.fill("black")

        pygame.draw.rect(
            self.SCREEN,
            "red",
            self.player
        )

        #
        # IMÁGENES
        #

        for image in self.images:

            if image.get_id() == "fadein":
                continue

            if isinstance(image, Animation):
                image.update(self.delta_time)

            surface = image.get_scr().copy()
            surface.set_alpha(image.get_alpha())

            x = int(image.get_x() * self.UI_SCALE)
            y = int(image.get_y() * self.UI_SCALE)

            rect = surface.get_rect(topleft=(x, y))
            image.set_rect(rect)

            self.SCREEN.blit(surface, (x, y))

        #
        # TEXTOS
        #

        for text in self.texts:

            x = int(text.get_x() * self.UI_SCALE)
            y = int(text.get_y() * self.UI_SCALE)

            for line_index, surface in enumerate(text.get_rendered_lines()):

                surface.set_alpha(text.get_alpha())

                self.SCREEN.blit(
                    surface,
                    (
                        x,
                        y + line_index * surface.get_height()
                    )
                )

        #
        # FADE (SIEMPRE ENCIMA)
        #

        for image in self.images:

            if image.get_id() != "fadein":
                continue

            surface = image.get_scr().copy()
            surface.set_alpha(image.get_alpha())

            self.SCREEN.blit(
                surface,
                (
                    image.get_x(),
                    image.get_y()
                )
            )

        #
        # DEBUG
        #

        time_text = self.H4.render(
            f"Time: {round(self.elapsed_time)}s",
            True,
            "white"
        )

        self.SCREEN.blit(
            time_text,
            (10, 10)
        )

        pygame.display.update()        
    def create_images(self, group):

        images = []

        for data in IMAGES[group]:

            #
            # Animaciones
            #

            if data.get("type", "image") == "animation":

                images.append(

                    Animation(

                        id=data["id"],
                        folder=data["folder"],

                        trigger=data["trigger"],
                        alpha=data["alpha"],

                        x=data["x"],
                        y=data["y"],

                        width=self.WIDTH,
                        height=self.HEIGHT,
                        scale=self.UI_SCALE,

                        fullscreen=data.get("fullscreen", False),
                        subid=data.get("subid"),

                        fps=data.get("fps", 12),
                        loop=data.get("loop", True),

                        size=data.get("size")

                    )

                )

            #
            # Imágenes normales
            #

            else:

                surface = pygame.image.load(
                    data["path"]
                ).convert_alpha()

                if "size" in data:

                    surface = pygame.transform.smoothscale(
                        surface,
                        data["size"]
                    )

                images.append(

                    Images(

                        id=data["id"],
                        scr=surface,

                        trigeable=data["trigger"],
                        alpha_cn=data["alpha"],

                        xPos=data["x"],
                        yPos=data["y"],

                        width=self.WIDTH,
                        height=self.HEIGHT,
                        ui_scale=self.UI_SCALE,

                        isBG=data.get("fullscreen", False),
                        sub_id=data.get("subid")

                    )

                )

        return images
    
    def get_image(self, image_id, image_subid=None):

        for image in self.images:

            if image.get_id() != image_id:
                continue

            if image_subid is None:
                return image

            if image.get_subid() == image_subid:
                return image

        return None
    
    def toggle_door(self, button):

        side = button.get_id().replace("Button", "")

        door = self.get_image(f"{side}Door")

        if door is None:
            return

        if button.get_subid() == "off":

            button.set_subid("on")

            button.change_image(
                "./assets/sprites/Mechanics/Buttons/Doors-Button-On.png"
            )

            door.set_subid("closed")
            door.set_alpha(255)

            if side == "Left":
                self.LEFT_DOOR = "Closed"
            else:
                self.RIGHT_DOOR = "Closed"

        else:

            button.set_subid("off")

            button.change_image(
                "./assets/sprites/Mechanics/Buttons/Doors-Button.png"
            )

            door.set_subid("open")
            door.set_alpha(0)

            if side == "Left":
                self.LEFT_DOOR = "Open"
            else:
                self.RIGHT_DOOR = "Open"

    def add_script(self, script_class):
        script = script_class(self)
        self.scripts.append(script)

    def add_script(self, script_class):
        self.scripts.append(script_class(self))

    def load_resources(self):

        #
        # Animatronics
        #

        self.maurello = Animatronic(
            1,
            "Maurello",
            get_fromSave("animatronics.Maurello.ai")
        )

        self.furry = Animatronic(
            1,
            "Maurello",
            get_fromSave("animatronics.Maurello.ai")
        )

        #
        # Tips
        #

        self.RANDOM_TIPS = [

            "If you watch cam H1 while recharging Cat Spawner, It'll charge twice as fast!",

            "You can get rid of Pou by pressing 'Shift' if he's in a top position.",

            "You can slow down Sonic when the cameras are up, making him unable to jump cams. \nWell... most of the time.",

            "Bob doesn't like being watched.",

            "Hold 'Shift' to keep using the keyboard shortcuts when the password \nprompt is up!",

            "Agressive Dad makes noise when reaching the closet, but regular dad doesn't.",

            "Hellish can imitate hazards like Darkbloom, be careful with what you hear."

        ]

        #
        # Texts
        #

        self.WARNING_TEXTS = [
            Text(0,"Warning", self.H3, "white", 0, False, 575, 300),

            Text(0,
                "This game was made with only joke purposes \n"
                "     and must no be taken offensively. \n"
                "      This game contains loud noises, \n"
                "             and jumpscares.",
                self.H3,
                "white",
                0,
                False,
                275,
                350
            )
    ]

        self.CUSTOM_NIGHT_TEXTS = [
            Text(0, "Custom Night", self.H1, "white", 255, False, 450, 50,"2ndlayered"),
            Text(1, "Set All 0",self.H2,"white",255,True,1070,430),
            Text(2, "Add All 1",self.H2,"white",255,True,1070,475),
            Text(3, "Set All 5",self.H2,"white",255,True,1070,520),
            Text(4, "Set All 10",self.H2,"white",255,True,1065,565),
            Text(5, "Set All 20",self.H2,"white",255,True,1065,610),
            Text(6, "START",self.H1,"white",255,True,1110,665),
            Text(7, "Settings",self.H2,"white",255,True,1075,370),
            Text(8, "Back", self.H1, "white", 255, True, -1020, 640, "Config"),
            Text(101, str(self.maurello.get_nombre()), self.H3, "white", 255, False, 90 ,202,"layered"),
            Text(111, str(self.maurello.get_ai()), self.H1, "white", 255, False, 148 ,365,"layered"),
        ]

        self.LOAD_NIGHT_TEXTS = [
            Text(0, "\n Night", self.H1, "white", 0, False, 550, 280),
            Text(1, "12", self.H1, "white", 0, False, 570, 280, "Hour"),
            Text(2, "AM", self.H1, "white", 0, False, 630, 280, "Period"),
            Text(3, "Tip: " + self.RANDOM_TIPS[random.randrange(7)], self.H4, "white", 0, False, 30, 800, "Tips")
        ]

        self.INGAME_TEXTS = [
            Text(0, "12", self.H1, "white", 255, False, 1150, 15, "Hour"),
            Text(0, "AM", self.H1, "white", 255, False, 1210, 15, "Period"),
            Text(0, "Custom Night", self.H4, "white", 255, False, 1080, 60),
        ]

        #
        # Images
        #

        self.WARNING_IMG = self.create_images(
            "WARNING"
        )

        self.CUSTOM_NIGHT_IMG = self.create_images(
            "CUSTOM_NIGHT"
        )

        self.LOAD_NIGHT_IMG = self.create_images(
            "LOAD_NIGHT"
        )

        self.INGAME_IMG = self.create_images(
            "INGAME_COMPACTOFFICE"
        )

        #
        # Default screen
        #

        self.texts = self.WARNING_TEXTS.copy()

        self.images = self.WARNING_IMG.copy()

    def handle_events(self):

        self.mouse_clicked = False

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():

            #
            # Cerrar juego
            #

            if event.type == pygame.QUIT:
                return False
            
            #
            # Usar Scripts
            #
            try:
                for script in self.scripts:
                    script.event(event)
            except:
                pass

            #
            # Scroll
            #

            if (
                event.type == pygame.MOUSEWHEEL
                and self.SUBGAMESTATE == "CustomNight"
            ):

                self.CUSTOM_NIGHT_SCROLL += event.y * 25

            #
            # Actualizar textos
            #

            for text in self.texts:

                if text.get_id() == 111:

                    text.set_text(
                        str(self.maurello.get_ai())
                    )

            #
            # Click izquierdo
            #

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                self.mouse_clicked = True

                #
                # Menu
                #

                if self.GAMESTATE == "menu":

                    self.handle_menu_click()

                #
                # Ingame
                #

                elif self.GAMESTATE == "ingame":

                    self.handle_ingame_click()
        return True

    def handle_menu_click(self):

        for text in self.texts:

            if not text.is_trigeable():
                continue

            rect = text.get_rect()

            if rect and rect.collidepoint(self.mouse_x, self.mouse_y):

                match text.get_id():

                    case 1:
                        self.maurello.set_ai(0)

                    case 2:
                        self.maurello.add_ai(1)

                    case 3:
                        self.maurello.set_ai(5)

                    case 4:
                        self.maurello.set_ai(10)

                    case 5:
                        self.maurello.set_ai(20)

                    case 6:

                        print("Start Game")

                        self.menu_start_time = time.time()

                        self.mixer.set_volume(
                            self.CHANNEL_MENU,
                            0.05
                        )

                        self.texts = self.LOAD_NIGHT_TEXTS
                        self.images = self.LOAD_NIGHT_IMG

                        self.discord.update_rpc(
                            "Loading night",
                            "In a Menu"
                        )

                        self.SUBGAMESTATE = "LoadNight"

                    case 7:

                        self.mixer.set_volume(
                            self.CHANNEL_MENU,
                            0.05
                        )

                        text.set_trigeable(False)

                        self.SETTINGS_STATE = "opening"

                    case 8:

                        self.mixer.set_volume(
                            self.CHANNEL_MENU,
                            0.1
                        )

                        text.set_trigeable(False)

                        self.SETTINGS_STATE = "closing"

        #
        # Botones de imágenes
        #

        for image in self.images:

            if not image.is_trigeable():
                continue

            rect = image.get_rect()

            if not rect:
                continue

            if not rect.collidepoint(
                self.mouse_x,
                self.mouse_y
            ):
                continue

            match image.get_subid():

                case "MaurelloMinusAi":
                    self.maurello.minus_ai(1)

                case "MaurelloAddAi":
                    self.maurello.add_ai(1)

    def handle_ingame_click(self):

        for image in self.images:

            if not image.is_trigeable():
                continue

            rect = image.get_rect()

            if rect is None:
                continue

            if not rect.collidepoint(
                self.mouse_x,
                self.mouse_y
            ):
                continue

            if image.get_id().endswith("Button"):

                self.toggle_door(image)
    
    def update_menu(self):

        #
        # WARNING SCREEN
        #

        if self.SUBGAMESTATE == "warningscreen":

            (
                self.SUBGAMESTATE,
                self.MENUSTATE,
                self.timer,
                self.menu_start_time

            ) = warning_main(

                texts=self.texts,
                img=self.images,

                delta_time=self.delta_time,

                fadein_speed=self.fadein_speed,
                fadeout_speed=self.fadeout_speed,

                timer=self.timer,
                menu_state=self.MENUSTATE,

                mouse_clicked=self.mouse_clicked,

                menu_start_time=self.menu_start_time,

                mixer_sound=self.mixer,

                discord=self.discord,

                channel_menu=self.CHANNEL_MENU

            )

        #
        # CUSTOM NIGHT
        #

        elif self.SUBGAMESTATE == "CustomNight":

            self.texts = self.CUSTOM_NIGHT_TEXTS
            self.images = self.CUSTOM_NIGHT_IMG

            self.menu_start_time = time.time()

            (
                self.CUSTOM_NIGHT_SCROLL,
                self.SETTINGS_SCROLL,
                self.SETTINGS_STATE

            ) = custom_night_main(

                texts=self.texts,

                delta_time=self.delta_time,

                custom_night_scroll=self.CUSTOM_NIGHT_SCROLL,

                settings_scroll=self.SETTINGS_SCROLL,

                settings_speed=self.SETTINGS_SPEED,

                settings_state=self.SETTINGS_STATE

            )

        #
        # LOAD NIGHT
        #

        elif self.SUBGAMESTATE == "LoadNight": 
            load_night_main(self)

    def update_ingame(self):

        self.texts = self.INGAME_TEXTS
        self.images = self.INGAME_IMG
        (

            self.player_x,

            self.night_timer,

            self.hour,

            self.INGAME_FADE_ALPHA

        ) = ingame_main(

            texts=self.texts,

            img=self.images,

            player=self.player,

            player_x=self.player_x,

            mouse_x=self.mouse_x,

            delta_time=self.delta_time,

            night_timer=self.night_timer,

            hour=self.hour,

            fade_alpha=self.INGAME_FADE_ALPHA,

            fade_speed=self.INGAME_FADE_SPEED,

            left_border=self.LEFT_BORDER,

            right_border=self.RIGHT_BORDER,

            width=self.WIDTH,

            max_speed=self.MAX_SPEED,

            discord=self.discord

        )

        self.maurello.update(self.delta_time)

    def update(self):

        for script in self.scripts:
            script.update(self.delta_time)

        #
        # MENU
        #

        if self.GAMESTATE == "menu":

            self.update_menu()

        #
        # INGAME
        #

        elif self.GAMESTATE == "ingame":

            self.update_ingame()



    def run(self):

        self.discord.initiate_rpc()

        running = True

        while running:

            self.delta_time = self.clock.tick(60) / 1000

            self.elapsed_time = time.time() - self.start_time
            self.menu_elapsed_time = time.time() - self.menu_start_time

            running = self.handle_events()
            self.update()
            if self.GAMESTATE == "menu":
                self.drawMenu()
            else:
                self.drawIngame()

        pygame.quit()