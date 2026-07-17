import random

class Animatronic:

    def __init__(
        self,
        id: int,
        nombre: str,
        ai: int,
        path: list,
        max_ai: int = 20
    ):

        self.__id = id
        self.__nombre = nombre

        self.max_ai = max(20, max_ai)

        self.__ai = max(
            0,
            min(ai, self.max_ai)
        )
        # Refresca el feed de camara 
        self.needs_refresh = False

        # Ruta completa del animatrónico
        self.path = path

        # Comienza en el primer nodo
        self.path_index = 0

        # Datos actuales
        self.current_cam = self.path[0]["cam"]
        self.current_sprite = self.path[0]["spritepath"]
        self.current_size = self.path[0]["size"]
        self.current_x = self.path[0]["x"]
        self.current_y = self.path[0]["y"]

        self.move_timer = 0.0
        self.move_interval = 4.0

    # -----------------------------------
    # Getters
    # -----------------------------------

    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_ai(self):
        return self.__ai

    def get_camera(self):
        return self.current_cam

    def get_sprite(self):
        return self.current_sprite

    def get_size(self):
        return self.current_size

    def get_position(self):
        return (
            self.current_x,
            self.current_y
        )
    def get_camera(self):
        return self.current_cam

    def get_sprite(self):
        return self.current_sprite

    def get_x(self):
        return self.current_x

    def get_y(self):
        return self.current_y

    def get_size(self):
        return self.current_size
    
    # -----------------------------------
    # AI
    # -----------------------------------

    def set_ai(self, new_ai):

        self.__ai = max(
            0,
            min(new_ai, self.max_ai)
        )

    def add_ai(self, value):
        self.set_ai(self.__ai + value)

    def minus_ai(self, value):
        self.set_ai(self.__ai - value)

    def set_move_interval(self, seconds):
        self.move_interval = seconds

    # -----------------------------------
    # Update
    # -----------------------------------

    def update(self, delta_time):

        self.move_timer += delta_time

        if self.move_timer >= self.move_interval:

            self.move_timer = 0

            self.roll_movement_opportunity()

    def roll_movement_opportunity(self):

        roll = random.randint(
            0,
            self.max_ai
        )

        print(
            f"[{self.__nombre}] "
            f"Roll: {roll}/{self.max_ai} | "
            f"AI: {self.__ai}"
        )

        if roll < self.__ai:
            self.move()
            self.needs_refresh = True

    # -----------------------------------
    # Movimiento
    # -----------------------------------

    def move(self):
        
        # Si ya llegó al final no sigue avanzando
        if self.path_index >= len(self.path) - 1:
            return

        self.path_index += 1

        node = self.path[self.path_index]

        self.current_cam = node["cam"]
        self.current_sprite = node["spritepath"]
        self.current_size = node["size"]
        self.current_x = node["x"]
        self.current_y = node["y"]

        print(
            f"{self.__nombre} -> CAM {self.current_cam}"
        )