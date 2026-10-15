
import os
import pygame
from .images import Images


class Animation(Images):

    # Cache compartida entre instancias.
    # Clave: (carpeta, tamaño final)
    _frame_cache = {}

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

        self.animation_folder = folder
        self.animation_size = size

        self._animation_scale = scale
        self._animation_fullscreen = fullscreen
        self._animation_width = width
        self._animation_height = height

        # Se conserva para compatibilidad.
        self.frame_cache = self._frame_cache

        self.frames = []

        self.load_frames(folder)

        if not self.frames:
            raise Exception(
                f"No animation frames found in '{folder}'."
            )

        # Images.__init__ necesita una superficie inicial.
        # Posteriormente reemplazamos esa superficie por
        # el frame previamente escalado.
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

        self.current_frame = 0
        self.animation_speed = fps
        self.loop = loop
        self.playing = True
        self.timer = 0.0
        self.reverse = False

        # Evita volver a escalar al cambiar de frame.
        self._set_current_surface()

    # ==========================================================
    # TAMAÑO FINAL
    # ==========================================================

    def _get_target_size(self, original_size):

        if self._animation_fullscreen:
            return (
                int(self._animation_width),
                int(self._animation_height)
            )

        if self.animation_size is not None:
            return (
                max(
                    1,
                    int(
                        self.animation_size[0]
                        * self._animation_scale
                    )
                ),
                max(
                    1,
                    int(
                        self.animation_size[1]
                        * self._animation_scale
                    )
                )
            )

        return (
            max(
                1,
                int(
                    original_size[0]
                    * self._animation_scale
                )
            ),
            max(
                1,
                int(
                    original_size[1]
                    * self._animation_scale
                )
            )
        )

    # ==========================================================
    # CARGAR FRAMES
    # ==========================================================

    def load_frames(self, folder):

        # La carpeta por sí sola no identifica correctamente
        # un conjunto de frames escalados. Dos animaciones
        # pueden utilizar tamaños distintos.
        cache_key = (
            os.path.abspath(folder),
            self.animation_size,
            self._animation_scale,
            self._animation_fullscreen,
            self._animation_width if self._animation_fullscreen else None,
            self._animation_height if self._animation_fullscreen else None
        )

        if cache_key in self._frame_cache:
            self.frames = self._frame_cache[cache_key]
            return

        frames = []

        try:
            files = sorted(os.listdir(folder))

        except Exception as error:
            print(
                f"[Animation] Error leyendo carpeta "
                f"'{folder}': {error}"
            )
            self.frames = []
            return

        for file in files:

            if not file.lower().endswith(".png"):
                continue

            path = os.path.join(folder, file)

            try:
                frame = pygame.image.load(
                    path
                ).convert_alpha()

                target_size = self._get_target_size(
                    frame.get_size()
                )

                if frame.get_size() != target_size:

                    # Conservamos smoothscale para las
                    # animaciones que usan size explícito.
                    if self.animation_size is not None:
                        frame = pygame.transform.smoothscale(
                            frame,
                            target_size
                        )
                    else:
                        frame = pygame.transform.scale(
                            frame,
                            target_size
                        )

                frames.append(frame)

            except Exception as error:
                print(
                    f"[Animation] Error cargando "
                    f"'{path}': {error}"
                )

        if frames:
            self._frame_cache[cache_key] = frames

        self.frames = frames

    # ==========================================================
    # CAMBIAR SUPERFICIE SIN REESCALAR
    # ==========================================================

    def _set_current_surface(self):

        if not self.frames:
            return

        self.set_scr(
            self.frames[self.current_frame]
        )

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(self, delta_time):

        if not self.playing:
            return

        if not self.frames:
            return

        if self.animation_speed <= 0:
            return

        frame_time = 1.0 / self.animation_speed

        self.timer += delta_time

        # Si todavía no corresponde cambiar de frame,
        # no hacemos ninguna transformación ni asignación.
        if self.timer < frame_time:
            return

        previous_frame = self.current_frame

        while self.timer >= frame_time:

            self.timer -= frame_time

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

        # Solo actualizamos la superficie si cambió
        # realmente el frame visible.
        if self.current_frame != previous_frame:
            self._set_current_surface()

    # ==========================================================
    # PLAY
    # ==========================================================

    def play(self, reverse=False):

        if not self.frames:
            return

        self.reverse = reverse
        self.playing = True
        self.timer = 0.0

        if reverse:
            self.current_frame = len(self.frames) - 1
        else:
            self.current_frame = 0

        self._set_current_surface()

    # ==========================================================
    # STOP
    # ==========================================================

    def stop(self):
        self.playing = False

    # ==========================================================
    # RESTART
    # ==========================================================

    def restart(self):
        self.play(reverse=self.reverse)

    # ==========================================================
    # FRAME
    # ==========================================================

    def set_frame(self, frame):

        if not self.frames:
            return

        frame = max(
            0,
            min(int(frame), len(self.frames) - 1)
        )

        if frame != self.current_frame:
            self.current_frame = frame
            self._set_current_surface()

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

        if self.loop or not self.frames:
            return False

        if self.reverse:
            return (
                not self.playing
                and self.current_frame == 0
            )

        return (
            not self.playing
            and self.current_frame == len(self.frames) - 1
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

        if folder != self.animation_folder:

            self.load_frames(folder)

            if not self.frames:
                raise Exception(
                    f"No animation frames found in '{folder}'."
                )

            self.animation_folder = folder

        elif not self.frames:

            self.load_frames(folder)

        self.current_frame = 0
        self.timer = 0.0
        self.reverse = False
        self.playing = False

        self._set_current_surface()

    # ==========================================================
    # LIMPIAR CACHE
    # ==========================================================

    @classmethod
    def clear_cache(cls):
        cls._frame_cache.clear()
