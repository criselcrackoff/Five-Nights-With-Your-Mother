import pygame
import time
import random

class Text:
    def __init__(self, id:int, text:str, size: pygame.font.Font, color:str, alpha_ch:int, trigeable:bool, xPos:int, yPos:int, sub_id:str=None):
        self.__id = id
        self.__text = text
        self.__size = size
        self.__color = color
        self.__alpha = alpha_ch
        self.__trigeable = trigeable
        self.__x = xPos
        self.__y = yPos
        self.__subid= sub_id
        self.__rect = None
        

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
        self.__text=text
    
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

        rendered = []

        for line in self.__text.split("\n"):
            rendered.append(
                self.__size.render(
                    line,
                    True,
                    self.__color
                )
            )

        return rendered