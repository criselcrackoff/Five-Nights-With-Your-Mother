
import pygame


class Text:
    FONT_PATHS = {
        "default": "./assets/fonts/OCRAEXT.TTF",
        "consolas": "./assets/fonts/Consolas-Regular.TTF",
    }

    FONT_CACHE = {}

    UI_SCALE = 1.0

    def __init__(
        self,
        id: int,
        text: str,
        size: int,
        color: str,
        alpha_ch: int,
        trigeable: bool,
        xPos: int,
        yPos: int,
        sub_id: str = None,
        font: str = "default"
    ):
        self.__id = id
        self.__text = text
        self.__size = size
        self.__color = color
        self.__alpha = alpha_ch
        self.__trigeable = trigeable
        self.__x = xPos
        self.__y = yPos
        self.__subid = sub_id
        self.__font = font
        self.__rect = None

    @classmethod
    def register_font(cls, name, path):
        cls.FONT_PATHS[name] = path

    @classmethod
    def set_ui_scale(cls, scale):
        cls.UI_SCALE = scale

    @classmethod
    def clear_font_cache(cls):
        cls.FONT_CACHE.clear()

    @classmethod
    def get_cached_font(cls, size, font="default"):
        font_path = cls.FONT_PATHS.get(
            font,
            cls.FONT_PATHS["default"]
        )

        scaled_size = max(1, int(size * cls.UI_SCALE))
        key = (font_path, scaled_size)

        if key not in cls.FONT_CACHE:
            cls.FONT_CACHE[key] = pygame.font.Font(
                font_path,
                scaled_size
            )

        return cls.FONT_CACHE[key]

    def get_font(self):
        return self.__font

    def set_font(self, font):
        self.__font = font

    def get_font_object(self):
        font_path = self.FONT_PATHS.get(
            self.__font,
            self.FONT_PATHS["default"]
        )

        scaled_size = max(
            1,
            int(self.__size * self.UI_SCALE)
        )

        key = (font_path, scaled_size)

        if key not in self.FONT_CACHE:
            self.FONT_CACHE[key] = pygame.font.Font(
                font_path,
                scaled_size
            )

        return self.FONT_CACHE[key]

    def get_id(self):
        return self.__id

    def get_text(self):
        return self.__text

    def get_size(self):
        return self.__size

    def get_color(self):
        return self.__color

    def get_alpha(self):
        return self.__alpha

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_subid(self):
        return self.__subid

    def is_trigeable(self):
        return self.__trigeable

    def set_text(self, text):
        self.__text = text

    def set_alpha(self, alpha):
        self.__alpha = max(0, min(255, int(alpha)))

    def set_rect(self, rect):
        self.__rect = rect

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def set_trigeable(self, trigeable):
        self.__trigeable = trigeable

    def get_rect(self):
        return self.__rect

    def get_lines(self):
        return self.__text.split("\n")

    def get_rendered_lines(self):
        font = self.get_font_object()

        rendered = []

        for line in self.get_lines():
            rendered.append(
                font.render(
                    line,
                    True,
                    self.__color
                )
            )

        return rendered
