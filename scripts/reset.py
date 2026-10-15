from engine.scripts import Script
from data.sounds import *
from data.game_images import *
import pygame
import time

from engine.images import Images


class ResetScript(Script):

    def __init__(self, game):
        super().__init__(game)

        # =====================================================
        # ESTADO
        # =====================================================

        self.resetting = False

        self.fade_out = False
        self.fade_in = False

        # =====================================================
        # TIPO DE RESET
        # =====================================================
        #
        # 1 = Reset normal
        #     F2 -> Warning Screen
        #
        # 2 = Reset de noche
        #     Game Over / 6 AM -> Custom Night
        #

        self.reset_type = 1

        # =====================================================
        # DURACIÓN DE LOS FADE
        # =====================================================

        # Reset normal
        self.normal_fade_duration = 1.5

        # Reset de noche
        # Mucho más rápido.
        self.night_fade_duration = 0.35

        self.fade_duration = self.normal_fade_duration

        # =====================================================
        # FADE
        # =====================================================

        self.fade_alpha = 0
        self.fade_image = None

        # =====================================================
        # AUDIO
        # =====================================================

        self.audio_channels = []

        # Volumen que tenía cada canal antes del reset.
        self.audio_volumes = {}

        # Volumen actual utilizado durante el fade.
        self.audio_fade_volumes = {}

        # Volumen objetivo después del reset.
        self.audio_target_volumes = {}

    # =========================================================
    # EVENTOS
    # =========================================================

    def event(self, event):

        if event.type == pygame.KEYDOWN:

            # F2 = Reset normal
            if event.key == pygame.K_F2:

                self.reset(1)

            # F3 = Reset de noche
            if event.key == pygame.K_F3:

                self.reset(2)

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self, dt):

        if not self.resetting:
            return

        # =====================================================
        # FADE OUT
        # =====================================================

        if self.fade_out:

            # -------------------------------------------------
            # FADE VISUAL
            # -------------------------------------------------

            self.fade_alpha += (
                255 * dt / self.fade_duration
            )

            if self.fade_alpha >= 255:

                self.fade_alpha = 255

            if self.fade_image:

                self.fade_image.set_alpha(
                    int(self.fade_alpha)
                )

            # -------------------------------------------------
            # FADE AUDIO
            # -------------------------------------------------

            fade_speed = dt / self.fade_duration

            for channel in self.audio_channels:

                original_volume = (
                    self.audio_volumes.get(
                        channel,
                        0
                    )
                )

                current_volume = (
                    self.audio_fade_volumes.get(
                        channel,
                        original_volume
                    )
                )

                current_volume -= (
                    original_volume * fade_speed
                )

                current_volume = max(
                    0,
                    current_volume
                )

                self.audio_fade_volumes[channel] = (
                    current_volume
                )

                try:

                    self.game.mixer.set_volume(
                        channel,
                        current_volume
                    )

                except Exception:
                    pass

            # -------------------------------------------------
            # TERMINÓ FADE OUT
            # -------------------------------------------------

            if self.fade_alpha >= 255:

                self.fade_out = False

                # -------------------------------------------------
                # SILENCIO ABSOLUTO
                # -------------------------------------------------

                for channel in self.audio_channels:

                    try:

                        self.game.mixer.set_volume(
                            channel,
                            0
                        )

                    except Exception:
                        pass

                # -------------------------------------------------
                # RESET REAL
                # -------------------------------------------------

                self.perform_reset()

                # -------------------------------------------------
                # COMENZAR FADE IN
                # -------------------------------------------------

                self.fade_in = True

                self.fade_alpha = 255

                for channel in self.audio_channels:

                    self.audio_fade_volumes[channel] = 0

                # -------------------------------------------------
                # TIPO 2
                # -------------------------------------------------
                #
                # El menú ya debe tener su música preparada.
                #
                if self.reset_type == 2:

                    self.start_custom_night_music()

            return

        # =====================================================
        # FADE IN
        # =====================================================

        if self.fade_in:

            # -------------------------------------------------
            # FADE VISUAL
            # -------------------------------------------------

            self.fade_alpha -= (
                255 * dt / self.fade_duration
            )

            if self.fade_alpha <= 0:

                self.fade_alpha = 0

                if self.fade_image:

                    self.fade_image.set_alpha(0)

                # -------------------------------------------------
                # TERMINAR RESET
                # -------------------------------------------------

                self.fade_in = False
                self.resetting = False

                # -------------------------------------------------
                # ELIMINAR FADE
                # -------------------------------------------------

                if self.fade_image in self.game.images:

                    self.game.images.remove(
                        self.fade_image
                    )

                self.fade_image = None

                # -------------------------------------------------
                # ASEGURAR VOLUMEN FINAL
                # -------------------------------------------------

                for channel in self.audio_channels:

                    target_volume = (
                        self.audio_target_volumes.get(
                            channel,
                            0
                        )
                    )

                    try:

                        self.game.mixer.set_volume(
                            channel,
                            target_volume
                        )

                    except Exception:
                        pass

                print("[RESET] Reset complete.")

                return

            # -------------------------------------------------
            # APLICAR FADE VISUAL
            # -------------------------------------------------

            if self.fade_image:

                self.fade_image.set_alpha(
                    int(self.fade_alpha)
                )

            # -------------------------------------------------
            # FADE AUDIO
            # -------------------------------------------------

            fade_speed = dt / self.fade_duration

            for channel in self.audio_channels:

                target_volume = (
                    self.audio_target_volumes.get(
                        channel,
                        0
                    )
                )

                current_volume = (
                    self.audio_fade_volumes.get(
                        channel,
                        0
                    )
                )

                current_volume += (
                    target_volume * fade_speed
                )

                current_volume = min(
                    target_volume,
                    current_volume
                )

                self.audio_fade_volumes[channel] = (
                    current_volume
                )

                try:

                    self.game.mixer.set_volume(
                        channel,
                        current_volume
                    )

                except Exception:
                    pass

    # =========================================================
    # INICIAR RESET
    # =========================================================

    def reset(self, reset_type=1):

        # No permitir otro reset mientras
        # este todavía está ejecutándose.

        if self.resetting:
            return

        # =====================================================
        # GUARDAR TIPO
        # =====================================================

        self.reset_type = reset_type

        # Seguridad

        if self.reset_type not in (1, 2):

            self.reset_type = 1

        # =====================================================
        # DURACIÓN
        # =====================================================

        if self.reset_type == 1:

            self.fade_duration = (
                self.normal_fade_duration
            )

        else:

            self.fade_duration = (
                self.night_fade_duration
            )

        # =====================================================
        # ACTIVAR RESET
        # =====================================================

        self.resetting = True

        self.fade_out = True
        self.fade_in = False

        self.fade_alpha = 0

        game = self.game

        print(
            f"[RESET] Starting reset "
            f"type {self.reset_type}..."
        )

        print(
            f"[RESET] Fade duration: "
            f"{self.fade_duration}s"
        )

        # =====================================================
        # CAPTURAR CANALES
        # =====================================================

        self.audio_channels = []

        # -----------------------------------------------------
        # MENÚ
        # -----------------------------------------------------

        if game.CHANNEL_MENU not in self.audio_channels:

            self.audio_channels.append(
                game.CHANNEL_MENU
            )

        # -----------------------------------------------------
        # AMBIENTE
        # -----------------------------------------------------

        if game.CHANNEL_AMBIENT not in self.audio_channels:

            self.audio_channels.append(
                game.CHANNEL_AMBIENT
            )

        # -----------------------------------------------------
        # MÚSICA
        # -----------------------------------------------------

        if game.CHANNEL_MUSIC not in self.audio_channels:

            self.audio_channels.append(
                game.CHANNEL_MUSIC
            )

        # -----------------------------------------------------
        # SFX
        # -----------------------------------------------------

        for channel in game.CHANNEL_SFX:

            if channel not in self.audio_channels:

                self.audio_channels.append(
                    channel
                )

        # -----------------------------------------------------
        # DOORS
        # -----------------------------------------------------

        for channel in game.CHANNEL_DOOR:

            if channel not in self.audio_channels:

                self.audio_channels.append(
                    channel
                )

        # -----------------------------------------------------
        # MONITOR
        # -----------------------------------------------------

        for channel in game.CHANNEL_MONITOR:

            if channel not in self.audio_channels:

                self.audio_channels.append(
                    channel
                )

        # -----------------------------------------------------
        # MASK
        # -----------------------------------------------------

        if game.CHANNEL_MASK not in self.audio_channels:

            self.audio_channels.append(
                game.CHANNEL_MASK
            )

        # =====================================================
        # CAPTURAR VOLUMEN REAL
        # =====================================================

        self.audio_volumes = {}
        self.audio_fade_volumes = {}
        self.audio_target_volumes = {}

        for channel in self.audio_channels:

            try:

                volume = pygame.mixer.Channel(
                    channel
                ).get_volume()

            except Exception:

                volume = 0

            self.audio_volumes[channel] = volume

            self.audio_fade_volumes[channel] = volume

            # Por defecto, después del reset
            # todos los canales permanecen en 0.

            self.audio_target_volumes[channel] = 0

        # =====================================================
        # TIPO 2
        # =====================================================
        #
        # El Custom Night utiliza la música del menú.
        #
        # Esta empieza en 0 y el fade-in la lleva hasta 0.1.
        #

        if self.reset_type == 2:

            self.audio_target_volumes[
                game.CHANNEL_MENU
            ] = 0.1

        # =====================================================
        # CREAR FADE
        # =====================================================

        self.fade_image = self.create_fade_image()

        self.fade_image.set_alpha(0)

        game.images.append(
            self.fade_image
        )

    # =========================================================
    # MÚSICA DEL CUSTOM NIGHT
    # =========================================================

    def start_custom_night_music(self):

        game = self.game

        try:

            # -------------------------------------------------
            # Detener cualquier sonido anterior
            # -------------------------------------------------

            try:

                game.mixer.stop(
                    game.CHANNEL_MENU
                )

            except Exception:
                pass

            # -------------------------------------------------
            # Iniciar música del menú
            # -------------------------------------------------

            game.mixer.play(
                Custom_Menu,
                0,
                game.CHANNEL_MENU,
                True
            )

            # -------------------------------------------------
            # Empezar desde 0.
            # El fade-in se encargará del volumen.
            # -------------------------------------------------

            try:

                game.mixer.set_volume(
                    game.CHANNEL_MENU,
                    0
                )

            except Exception:
                pass

            self.audio_fade_volumes[
                game.CHANNEL_MENU
            ] = 0

            print(
                "[RESET] Custom Night music started."
            )

        except Exception as error:

            print(
                "[RESET] Could not start "
                f"Custom Night music: {error}"
            )

    # =========================================================
    # CREAR IMAGEN DEL FADE
    # =========================================================

    def create_fade_image(self):

        surface = pygame.Surface(
            (
                self.game.WIDTH,
                self.game.HEIGHT
            ),
            pygame.SRCALPHA
        )

        surface.fill(
            (0, 0, 0, 255)
        )

        return Images(

            id="ResetFade",

            scr=surface,

            trigeable=False,

            alpha_cn=0,

            xPos=0,
            yPos=0,

            width=self.game.WIDTH,
            height=self.game.HEIGHT,

            ui_scale=self.game.UI_SCALE,

            isBG=True,

            sub_id=None
        )

    # =========================================================
    # RESET REAL
    # =========================================================

    def perform_reset(self):

        game = self.game

        print("[RESET] Restoring game state...")

        # =====================================================
        # 1. DETENER AUDIO
        # =====================================================

        try:

            game.mixer.stop_all()

        except AttributeError:

            try:

                pygame.mixer.stop()

            except Exception:
                pass

        # =====================================================
        # 2. GUARDAR FADE
        # =====================================================

        fade = self.fade_image

        # =====================================================
        # 3. LIMPIAR OBJETOS
        # =====================================================

        game.images = []
        game.texts = []

        # =====================================================
        # 4. RECREAR RECURSOS
        # =====================================================

        if hasattr(game, "load_resources"):

            game.load_resources()

        # =====================================================
        # 5. RECREAR IMÁGENES
        # =====================================================

        game.WARNING_IMG = None
        game.CUSTOM_NIGHT_IMG = None
        game.LOAD_NIGHT_IMG = None
        game.INGAME_IMG = None

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
        # 6. ESTADOS BASE
        # =====================================================

        game.GAMESTATE = "menu"

        # Por defecto será warning.
        # El tipo 2 lo cambia más abajo.

        game.SUBGAMESTATE = "warningscreen"

        game.MENUSTATE = "fade_in"

        # =====================================================
        # 7. TIMERS
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
        # 8. MOUSE
        # =====================================================

        game.mouse_x = 0
        game.mouse_y = 0
        game.mouse_clicked = False

        # =====================================================
        # 9. PLAYER
        # =====================================================

        game.player_x = 0.0

        game.player = pygame.Rect(
            0,
            game.HEIGHT * 0.5,
            game.PLAYER_WIDTH,
            game.PLAYER_HEIGHT
        )

        # =====================================================
        # 10. NOCHE
        # =====================================================

        game.hour = -4

        game.night_type = 1

        game.officetype = "Compact"

        game.LEFT_DOOR = "Open"

        game.RIGHT_DOOR = "Open"

        game.blackout = False

        # =====================================================
        # 11. MENU
        # =====================================================

        game.CUSTOM_NIGHT_SCROLL = -10

        game.SETTINGS_SCROLL = 0

        game.SETTINGS_STATE = "closed"

        # =====================================================
        # 12. AUDIO / FADE
        # =====================================================

        game.MUSIC_STOPPED = False

        game.INGAME_FADE_ALPHA = 255

        game.INGAME_FADE_SPEED = 500

        game.fadein_speed = 712.5

        game.fadeout_speed = 166.30

        # =====================================================
        # 13. GAMEPLAY
        # =====================================================

        # Valor inicial de Game.__init__
        game.usage = 1

        game.power = None

        game.monitor = None

        game.mask = None

        game.ismonitoropen = False

        game.ismaskopen = False

        # =====================================================
        # 14. DETERMINAR DESTINO
        # =====================================================

        if self.reset_type == 1:

            # -------------------------------------------------
            # RESET NORMAL
            # -------------------------------------------------

            game.images = game.WARNING_IMG

            game.texts = game.WARNING_TEXTS

            game.GAMESTATE = "menu"

            game.SUBGAMESTATE = "warningscreen"

            game.MENUSTATE = "fade_in"

            print(
                "[RESET] Destination: Warning Screen"
            )

        else:

            # -------------------------------------------------
            # RESET DE NOCHE
            # -------------------------------------------------

            game.images = game.CUSTOM_NIGHT_IMG
            game.texts = game.CUSTOM_NIGHT_TEXTS

            game.GAMESTATE = "menu"

            # IMPORTANTE: debe ser exactamente "CustomNight"
            game.SUBGAMESTATE = "CustomNight"

            game.MENUSTATE = "fade_in"

            # -------------------------------------------------
            # Reset del scroll
            # -------------------------------------------------

            game.CUSTOM_NIGHT_SCROLL = -10

            game.SETTINGS_SCROLL = 0

            game.SETTINGS_STATE = "closed"

            print(
                "[RESET] Destination: Custom Night"
            )

        # =====================================================
        # 15. RESTAURAR FADE
        # =====================================================

        self.fade_image = fade

        self.fade_image.set_alpha(255)

        game.images.append(
            self.fade_image
        )

        # =====================================================
        # 16. AUDIO DESDE 0
        # =====================================================

        for channel in self.audio_channels:

            self.audio_fade_volumes[channel] = 0

            try:

                game.mixer.set_volume(
                    channel,
                    0
                )

            except Exception:
                pass

        # =====================================================
        # 17. SCRIPTS
        # =====================================================

        if hasattr(game, "scripts"):

            # ResetScript permanece vivo.
            # Todos los scripts de gameplay se eliminan.

            game.scripts = [
                self
            ]

        print("[RESET] Game state restored.")