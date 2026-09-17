import random


class Animatronic:

    def __init__(
        self,
        id: int,
        nombre: str,
        ai: int,
        jumpscare: list,
        path: list,
        ignoremask: bool = False,
        max_ai: int = 20
    ):

        # Identificación
        self.__id = id
        self.__nombre = nombre

        # Inteligencia artificial
        self.max_ai = max(20, max_ai)

        self.__ai = max(
            0,
            min(ai, self.max_ai)
        )

        # Comportamiento de ataque
        self.ignoremask = ignoremask
        self.jumpscare = jumpscare

        # Ruta
        self.path = path
        self.path_index = 0

        # Estado actual
        self.needs_refresh = False

        # Obtener información del primer nodo
        self.current_cam = None
        self.current_sprite = None
        self.current_size = None
        self.current_x = None
        self.current_y = None

        self.update_current_node()

        # Movimiento
        self.move_timer = 0.0
        self.move_interval = 4.0

    # ==========================================================
    # GETTERS
    # ==========================================================

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__nombre

    def get_ai(self):
        return self.__ai

    def get_ignoremask(self):
        return self.ignoremask

    def get_jumpscare(self):
        return self.jumpscare

    def get_path(self):
        return self.path

    def get_path_index(self):
        return self.path_index

    def get_camera(self):
        return self.current_cam

    def get_sprite(self):
        return self.current_sprite

    def get_size(self):
        return self.current_size

    def get_x(self):
        return self.current_x

    def get_y(self):
        return self.current_y

    # ==========================================================
    # AI
    # ==========================================================

    def set_ai(self, new_ai):
        self.__ai = max(
            0,
            min(new_ai, self.max_ai)
        )

    def add_ai(self, value):
        self.set_ai(self.__ai + value)

    def minus_ai(self, value):
        self.set_ai(self.__ai - value)

    # ==========================================================
    # MOVIMIENTO
    # ==========================================================

    def set_move_interval(self, seconds):
        self.move_interval = seconds

    def update(self, delta_time):
        self.move_timer += delta_time

        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.roll_movement_opportunity()

    def roll_movement_opportunity(self):
        roll = random.randint(0, self.max_ai)

        print(
            f"[{self.__nombre}] "
            f"Roll: {roll}/{self.max_ai} | "
            f"AI: {self.__ai}"
        )

        if roll < self.__ai:
            self.move()
            self.needs_refresh = True

    def move(self):
        if not self.path:
            return

        if self.path_index >= len(self.path) - 1:
            return

        self.path_index += 1

        self.update_current_node()

        print(
            f"{self.__nombre} -> "
            f"{self.current_cam}"
            f"{self.is_camera()}"
            f"{self.is_door()}"
            f"{self.is_office()}"
        )

    # ==========================================================
    # NODO ACTUAL
    # ==========================================================

    def update_current_node(self):
        if not self.path:
            return

        node = self.path[self.path_index]

        # El nodo siempre debería tener "cam"
        self.current_cam = node.get("cam")

        # Los siguientes valores solamente existen
        # en los nodos que representan una cámara normal.
        self.current_sprite = node.get("spritepath")
        self.current_size = node.get("size")
        self.current_x = node.get("x")
        self.current_y = node.get("y")

    # ==========================================================
    # TIPO DE NODO
    # ==========================================================

    def is_camera(self):
        return isinstance(self.current_cam, int)

    def is_door(self):
        return self.current_cam in (
            "door_left",
            "door_right"
        )

    def is_office(self):
        return self.current_cam == "office"

    # ==========================================================
    # POSICIÓN
    # ==========================================================

    def reset_position(self):
        if not self.path:
            return

        self.path_index = 0

        self.update_current_node()

        self.needs_refresh = True

        print(
            f"{self.__nombre} "
            f"ha vuelto a su posición inicial."
        )