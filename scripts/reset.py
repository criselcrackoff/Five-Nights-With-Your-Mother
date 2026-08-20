from engine.scripts import Script
from data.sounds import *
from data.game_images import *
import pygame
import time


class ResetScript(Script):

    def __init__(self, game):
        super().__init__(game)

        self.resetting = False

    def event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_F2:
                self.reset()

    def update(self, dt):
        pass

    def reset(self):

        if self.resetting:
            return

        self.resetting = True

        game = self.game

        print("[RESET] Starting reset...")

        # =====================================================
        # 1. DETENER AUDIO
        # =====================================================

        try:
            game.mixer.stop_all()
        except AttributeError:

            # Compatibilidad por si tu Mixer todavía
            # no tiene stop_all()
            try:
                pygame.mixer.stop()
            except Exception:
                pass

        # =====================================================
        # 2. LIMPIAR OBJETOS ACTUALES
        # =====================================================

        # Las listas que actualmente están en pantalla
        # dejan de ser utilizadas.
        game.images = []
        game.texts = []

        # =====================================================
        # 3. RECREAR ANIMATRÓNICOS
        # =====================================================

        # Esto vuelve a crear Maurello/Furry/etc.
        # utilizando los valores originales del save.
        if hasattr(game, "load_resources"):
            game.load_resources()

        # =====================================================
        # 4. RECREAR TEXTOS
        # =====================================================

        game.WARNING_TEXTS = [
            text
            for text in game.WARNING_TEXTS
        ]

        game.CUSTOM_NIGHT_TEXTS = [
            text
            for text in game.CUSTOM_NIGHT_TEXTS
        ]

        game.LOAD_NIGHT_TEXTS = [
            text
            for text in game.LOAD_NIGHT_TEXTS
        ]

        game.INGAME_TEXTS = [
            text
            for text in game.INGAME_TEXTS
        ]

        # =====================================================
        # 5. RECREAR IMÁGENES DESDE IMAGES
        # =====================================================

        # IMPORTANTE:
        #
        # No reutilizamos los objetos antiguos.
        # Creamos objetos completamente nuevos.
        #
        # Esto elimina:
        #
        # set_alpha()
        # set_x()
        # set_y()
        # change_image()
        # set_subid()
        # animaciones modificadas
        # etc.

        game.WARNING_IMG = None
        game.CUSTOM_NIGHT_IMG = None
        game.LOAD_NIGHT_IMG = None
        game.INGAME_IMG = None

        # Ahora se vuelven a construir desde IMAGES.
        game.WARNING_IMG = game.create_images(
            "WARNING"
        )

        game.CUSTOM_NIGHT_IMG = game.create_images(
            "CUSTOM_NIGHT"
        )

        game.LOAD_NIGHT_IMG = game.create_images(
            "LOAD_NIGHT"
        )

        game.INGAME_IMG = game.create_images(
            "INGAME_COMPACTOFFICE"
        )

        # =====================================================
        # 6. ESTADO DE PANTALLA
        # =====================================================

        game.images = game.WARNING_IMG
        game.texts = game.WARNING_TEXTS

        # =====================================================
        # 7. GAME STATES
        # =====================================================

        game.GAMESTATE = "menu"
        game.SUBGAMESTATE = "warningscreen"
        game.MENUSTATE = "fade_in"

        # =====================================================
        # 8. TIMERS
        # =====================================================

        game.start_time = time.time()
        game.menu_start_time = time.time()

        game.elapsed_time = 0
        game.menu_elapsed_time = 0
        game.delta_time = 0

        game.timer = 0
        game.LOAD_NIGHT_TIMER = 0
        game.night_timer = 0

        # =====================================================
        # 9. MOUSE
        # =====================================================

        game.mouse_x = 0
        game.mouse_y = 0
        game.mouse_clicked = False

        # =====================================================
        # 10. PLAYER
        # =====================================================

        game.player_x = 0.0

        game.player = pygame.Rect(
            0,
            game.HEIGHT * 0.5,
            game.PLAYER_WIDTH,
            game.PLAYER_HEIGHT
        )

        # =====================================================
        # 11. NOCHE
        # =====================================================

        game.hour = -4
        game.night_type = 1
        game.officetype = "Compact"

        game.LEFT_DOOR = "Open"
        game.RIGHT_DOOR = "Open"

        # =====================================================
        # 12. MENÚ
        # =====================================================

        game.CUSTOM_NIGHT_SCROLL = -10

        game.SETTINGS_SCROLL = 0
        game.SETTINGS_STATE = "closed"

        # =====================================================
        # 13. AUDIO / FADE
        # =====================================================

        game.MUSIC_STOPPED = False

        game.INGAME_FADE_ALPHA = 255
        game.INGAME_FADE_SPEED = 500

        game.fadein_speed = 712.5
        game.fadeout_speed = 166.30

        # =====================================================
        # 14. RESTAURAR VOLUMEN DEL MENÚ
        # =====================================================

        try:
            game.mixer.set_volume(
                game.CHANNEL_MENU,
                0.1
            )
        except Exception:
            pass

        # =====================================================
        # 15. RESET DE VARIABLES DE GAMEPLAY
        # =====================================================

        if hasattr(game, "usage"):
            game.usage = 0

        if hasattr(game, "ismonitoropen"):
            game.ismonitoropen = False

        if hasattr(game, "ismaskopen"):
            game.ismaskopen = False

        # =====================================================
        # 16. REINICIAR SCRIPTS
        # =====================================================

        # Si tu Game posee una lista de scripts,
        # dejamos únicamente este ResetScript.
        #
        # Después Game puede volver a registrar los scripts
        # normales al entrar nuevamente al estado correspondiente.

        if hasattr(game, "scripts"):

            game.scripts = [
                self
            ]

        print("[RESET] Game state restored.")

        self.resetting = False