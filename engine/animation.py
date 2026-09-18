import os
import pygame
from .images import Images


class Animation(Images):

    def __init__(
        self,
        id,
        folder,
        trigger,
        alpha,
        x,
        y,
        width,
        height,
        scale,
        fullscreen=False,
        subid=None,
        fps=12,
        loop=True,
        size=None
    ):

        self.frames = []

        self.animation_folder = folder
        self.animation_size = size

        # ==========================================================
        # CACHE DE ANIMACIONES
        # ==========================================================
        #
        # Guarda los frames ya cargados para evitar volver a leer
        # los PNG del disco durante el gameplay.
        #

        self.frame_cache = {}

        self.load_frames(folder)

        if len(self.frames) == 0:
            raise Exception(
                f"No animation frames found in '{folder}'."
            )

        super().__init__(
            id=id,
            scr=self.frames[0],
            trigeable=trigger,
            alpha_cn=alpha,
            xPos=x,
            yPos=y,
            width=width,
            height=height,
            ui_scale=scale,
            isBG=fullscreen,
            sub_id=subid
        )

        # ==========================================================
        # ESTADO
        # ==========================================================

        self.current_frame = 0
        self.animation_speed = fps
        self.loop = loop
        self.playing = True
        self.timer = 0
        self.reverse = False

    # ==========================================================
    # CARGAR FRAMES
    # ==========================================================

    def load_frames(self, folder):

        # ==========================================================
        # USAR CACHE
        # ==========================================================

        if folder in self.frame_cache:

            self.frames = self.frame_cache[folder]

            return

        frames = []

        try:

            files = sorted(
                os.listdir(folder)
            )

        except Exception as error:

            print(
                f"[Animation] Error leyendo carpeta "
                f"'{folder}': {error}"
            )

            self.frames = []

            return

        # ==========================================================
        # CARGAR PNG
        # ==========================================================

        for file in files:

            if not file.lower().endswith(".png"):
                continue

            path = os.path.join(
                folder,
                file
            )

            try:

                frame = pygame.image.load(
                    path
                ).convert_alpha()

            except Exception as error:

                print(
                    f"[Animation] Error cargando "
                    f"'{path}': {error}"
                )

                continue

            # ======================================================
            # ESCALA
            # ======================================================

            if self.animation_size is not None:

                frame = pygame.transform.smoothscale(
                    frame,
                    self.animation_size
                )

            frames.append(frame)

        # ==========================================================
        # GUARDAR CACHE
        # ==========================================================

        self.frame_cache[folder] = frames

        self.frames = frames

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(self, delta_time):

        if not self.playing:
            return

        if len(self.frames) == 0:
            return

        frame_time = 1 / self.animation_speed

        self.timer += delta_time

        while self.timer >= frame_time:

            self.timer -= frame_time

            # ======================================================
            # REPRODUCCIÓN NORMAL
            # ======================================================

            if not self.reverse:

                self.current_frame += 1

                if self.current_frame >= len(self.frames):

                    if self.loop:

                        self.current_frame = 0

                    else:

                        self.current_frame = (
                            len(self.frames) - 1
                        )

                        self.playing = False

                        break

            # ======================================================
            # REPRODUCCIÓN INVERSA
            # ======================================================

            else:

                self.current_frame -= 1

                if self.current_frame < 0:

                    if self.loop:

                        self.current_frame = (
                            len(self.frames) - 1
                        )

                    else:

                        self.current_frame = 0
                        self.playing = False

                        break

        self.change_surface(
            self.frames[self.current_frame]
        )

    # ==========================================================
    # PLAY
    # ==========================================================

    def play(self, reverse=False):

        if len(self.frames) == 0:
            return

        self.reverse = reverse
        self.playing = True
        self.timer = 0

        if reverse:

            self.current_frame = (
                len(self.frames) - 1
            )

        else:

            self.current_frame = 0

        self.change_surface(
            self.frames[self.current_frame]
        )

    # ==========================================================
    # STOP
    # ==========================================================

    def stop(self):

        self.playing = False

    # ==========================================================
    # RESTART
    # ==========================================================

    def restart(self):

        self.play(
            reverse=self.reverse
        )

    # ==========================================================
    # FRAME
    # ==========================================================

    def set_frame(self, frame):

        if len(self.frames) == 0:
            return

        frame = max(
            0,
            min(
                frame,
                len(self.frames) - 1
            )
        )

        self.current_frame = frame

        self.change_surface(
            self.frames[frame]
        )

    def get_frame(self):

        return self.current_frame

    def get_total_frames(self):

        return len(self.frames)

    # ==========================================================
    # ESTADO
    # ==========================================================

    def is_playing(self):

        return self.playing

    def is_finished(self):

        if self.loop:
            return False

        if self.reverse:

            return (
                not self.playing
                and self.current_frame == 0
            )

        return (
            not self.playing
            and
            self.current_frame ==
            len(self.frames) - 1
        )

    # ==========================================================
    # FPS
    # ==========================================================

    def set_fps(self, fps):

        self.animation_speed = fps

    # ==========================================================
    # CAMBIAR CARPETA
    # ==========================================================

    def change_folder(self, folder):

        # ==========================================================
        # MISMA CARPETA
        # ==========================================================
        #
        # Si ya estamos utilizando esta carpeta, NO volvemos a
        # cargar absolutamente nada del disco.
        #

        if folder == self.animation_folder:

            if len(self.frames) == 0:
                self.load_frames(folder)

            self.current_frame = 0
            self.timer = 0
            self.reverse = False
            self.playing = False

            if len(self.frames) > 0:

                self.change_surface(
                    self.frames[0]
                )

            return

        # ==========================================================
        # NUEVA CARPETA
        # ==========================================================

        self.animation_folder = folder

        self.load_frames(folder)

        if len(self.frames) == 0:

            raise Exception(
                f"No animation frames found "
                f"in '{folder}'."
            )

        # ==========================================================
        # REINICIAR ESTADO
        # ==========================================================

        self.current_frame = 0
        self.timer = 0
        self.reverse = False
        self.playing = False

        self.change_surface(
            self.frames[0]
        )