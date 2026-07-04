import pygame
import time
import random

class Images:
    def __init__(self, id:str, scr: pygame.Surface, trigeable:bool, alpha_cn:int, xPos:int, yPos:int, width, height, ui_scale, isBG:bool=False, sub_id:str=None):
        self.__id = id
        self.__scr = scr
        self.__trigeable = trigeable
        self.__alpha = alpha_cn
        self.__x = xPos
        self.__y = yPos
        self.__rect = None
        self.__isBG = isBG
        self.__subid = sub_id

        # Guardamos estos datos para reutilizarlos
        self.__width = width
        self.__height = height
        self.__ui_scale = ui_scale

        if isBG:
            self.__scr = pygame.transform.scale(
                scr,
                (width, height)
            )
        else:
            self.__scr = pygame.transform.scale(
                scr,
                (
                    int(scr.get_width() * ui_scale),
                    int(scr.get_height() * ui_scale)
                )
            )
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
    
    def get_width(self):
        return self.__scr.get_width()

    def get_height(self):
        return self.__scr.get_height()
    
    def get_subid(self):
        return self.__subid

    def is_BG(self):
        return self.__isBG

    def set_scr (self, scr):
        self.__scr = scr

    def set_rect(self, rect):
        self.__rect = rect

    def is_trigeable(self):
        return self.get_trigeable()
    
    def set_alpha(self, alpha):
        self.__alpha = max(0, min(255, int(alpha)))

    def set_subid(self, subid):
        self.__subid = subid
        
    def change_image(self, path: str):

        surface = pygame.image.load(path).convert_alpha()

        if self.__isBG:
            surface = pygame.transform.scale(
                surface,
                (self.__width, self.__height)
            )
        else:
            surface = pygame.transform.scale(
                surface,
                (
                    int(surface.get_width() * self.__ui_scale),
                    int(surface.get_height() * self.__ui_scale)
                )
            )

        self.__scr = surface
    