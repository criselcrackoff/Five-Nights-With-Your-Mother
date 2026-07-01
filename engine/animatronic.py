class Animatronic:
    def __init__(self,id:int,nombre:str,ai:int):
        self.__id=id
        self.__nombre=nombre
        self.__ai=ai
    def get_id(self):
        return self.__id
    def get_nombre(self):
        return self.__nombre
    def get_ai(self):
        return self.__ai
    def set_ai(self,new_ai):
        if new_ai < 0:
            new_ai = 0
        self.__ai=new_ai
    def add_ai(self, ai):
        self.__ai+= ai
        if self.__ai > 20:
            self.__ai = 20
    def minus_ai(self, ai):
        self.__ai-= ai
        if self.__ai < 0:
            self.__ai = 0
