
import os
import pygame


class Images:

    # PNG originales compartidos entre instancias.
    _image_cache = {}

    def __init__(
        self,
        id: str,
        scr: pygame.Surface,
        trigeable: bool,
        alpha_cn: int,
        xPos: int,
        yPos: int,
        width,
        height,
        ui_scale,
        isBG: bool = False,
        sub_id: str = None,
        size=None
    ):

        self.__id = id
        self.__trigeable = trigeable
        self.__alpha = max(0, min(255, int(alpha_cn)))
        self.__x = xPos
        self.__y = yPos
        self.__rect = None
        self.__isBG = isBG
        self.__subid = sub_id

        self._width = width
        self._height = height
        self._ui_scale = ui_scale
        self._size = size

        self.__scr = self.scale_surface(scr)

        # Cache de renderizado por instancia.
        self._draw_source = None
        self._draw_alpha = None
        self._draw_surface = None

    # ==========================================================
    # GETTERS
    # ==========================================================

    def get_id(self):
        return self.__id

    def get_scr(self):
        return self.__scr

    def get_trigeable(self):
        return self.__trigeable

    def get_alpha(self):
        return self.__alpha

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_rect(self):
        return self.__rect

    def get_subid(self):
        return self.__subid

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_surface_width(self):
        return self.__scr.get_width()

    def get_surface_height(self):
        return self.__scr.get_height()

    def get_size(self):
        return self._size

    def is_BG(self):
        return self.__isBG

    # ==========================================================
    # SETTERS
    # ==========================================================

    def set_scr(self, scr):
        self.__scr = scr
        self.invalidate_draw_cache()

    def set_rect(self, rect):
        self.__rect = rect

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def set_trigeable(self, trigger):
        self.__trigeable = trigger

    def set_alpha(self, alpha):
        alpha = max(0, min(255, int(alpha)))

        if alpha != self.__alpha:
            self.__alpha = alpha
            self.invalidate_draw_cache()

    def set_subid(self, subid):
        self.__subid = subid

    def set_ifBG(self, istrue):
        self.__isBG = istrue

    def set_size(self, size):
        if size == self._size:
            return

        self._size = size

        # Conservamos el comportamiento anterior:
        # escalar la superficie actual.
        self.__scr = self.scale_surface(self.__scr)
        self.invalidate_draw_cache()

    # ==========================================================
    # CACHE DE RENDERIZADO
    # ==========================================================

    def invalidate_draw_cache(self):
        self._draw_source = None
        self._draw_alpha = None
        self._draw_surface = None

    def get_draw_surface(self):

        alpha = self.__alpha

        if alpha <= 0:
            return None

        source = self.__scr

        # La superficie y su transparencia no cambiaron.
        if (
            self._draw_source is source
            and self._draw_alpha == alpha
            and self._draw_surface is not None
        ):
            return self._draw_surface

        if alpha == 255:

            # No copiamos la superficie cuando es opaca
            # a nivel de transparencia global.
            surface = source

        else:

            # Nunca modificamos directamente el frame
            # original: puede ser compartido por Animation.
            surface = source.copy()
            surface.set_alpha(alpha)

        self._draw_source = source
        self._draw_alpha = alpha
        self._draw_surface = surface

        return surface

    # ==========================================================
    # UTILS
    # ==========================================================

    def is_trigeable(self):
        return self.get_trigeable()

    def change_surface(self, surface):
        self.__scr = self.scale_surface(surface)
        self.invalidate_draw_cache()

    def scale_surface(self, surface):

        if self.__isBG:

            target_size = (
                max(1, int(self._width)),
                max(1, int(self._height))
            )

            if surface.get_size() == target_size:
                return surface

            return pygame.transform.scale(
                surface,
                target_size
            )

        if self._size is not None:

            target_size = (
                max(1, int(self._size[0] * self._ui_scale)),
                max(1, int(self._size[1] * self._ui_scale))
            )

            if surface.get_size() == target_size:
                return surface

            return pygame.transform.smoothscale(
                surface,
                target_size
            )

        target_size = (
            max(1, int(surface.get_width() * self._ui_scale)),
            max(1, int(surface.get_height() * self._ui_scale))
        )

        if surface.get_size() == target_size:
            return surface

        return pygame.transform.scale(
            surface,
            target_size
        )

    # ==========================================================
    # CAMBIAR IMAGEN
    # ==========================================================

    def change_image(self, path):

        path_key = os.path.abspath(path)

        if path_key in Images._image_cache:

            surface = Images._image_cache[path_key]

        else:

            surface = pygame.image.load(
                path
            ).convert_alpha()

            Images._image_cache[path_key] = surface

        self.change_surface(surface)

    # ==========================================================
    # LIMPIAR CACHE DE ARCHIVOS
    # ==========================================================

    @classmethod
    def clear_image_cache(cls):
        Images._image_cache.clear()
