import pygame


class Images:

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
        self.__scr = scr
        self.__trigeable = trigeable
        self.__alpha = alpha_cn
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

    # -----------------------------
    # Getters
    # -----------------------------

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

    # -----------------------------
    # Setters
    # -----------------------------

    def set_scr(self, scr):
        self.__scr = scr

    def set_rect(self, rect):
        self.__rect = rect

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def set_trigeable(self, trigger):
        self.__trigeable = trigger

    def set_alpha(self, alpha):
        self.__alpha = max(0, min(255, int(alpha)))

    def set_subid(self, subid):
        self.__subid = subid

    def set_size(self, size):
        self._size = size
        self.__scr = self.scale_surface(self.__scr)

    # -----------------------------
    # Utils
    # -----------------------------

    def is_trigeable(self):
        return self.get_trigeable()

    def change_surface(self, surface):
        self.__scr = self.scale_surface(surface)

    def scale_surface(self, surface):

        if self.__isBG:
            return pygame.transform.scale(
                surface,
                (self._width, self._height)
            )

        # Tamaño personalizado
        if self._size is not None:

            return pygame.transform.smoothscale(
                surface,
                (
                    int(self._size[0] * self._ui_scale),
                    int(self._size[1] * self._ui_scale)
                )
            )

        # Escalado automático por UI_SCALE
        return pygame.transform.scale(
            surface,
            (
                int(surface.get_width() * self._ui_scale),
                int(surface.get_height() * self._ui_scale)
            )
        )

    def change_image(self, path):

        surface = pygame.image.load(path).convert_alpha()

        self.change_surface(surface)