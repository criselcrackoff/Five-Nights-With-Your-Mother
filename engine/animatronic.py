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

        # ==========================================================
        # IDENTIFICACIÓN
        # ==========================================================

        self.__id = id
        self.__nombre = nombre

        # ==========================================================
        # AI
        # ==========================================================

        self.max_ai = max_ai

        self.__ai = max(
            0,
            min(ai, self.max_ai)
        )

        # ==========================================================
        # ATAQUE
        # ==========================================================

        self.ignoremask = ignoremask
        self.jumpscare = jumpscare

        # ==========================================================
        # PATH
        # ==========================================================

        self.path = path
        self.path_index = 0

        # ==========================================================
        # ESTADO
        # ==========================================================

        self.needs_refresh = False

        self.attacking = False
        self.blackout = False
        self.jumpscaring = False

        # ==========================================================
        # POSICIÓN ACTUAL
        # ==========================================================

        self.current_cam = None
        self.current_sprite = None
        self.current_size = None
        self.current_x = None
        self.current_y = None

        # Sprite utilizado cuando está en la oficina
        self.office_sprite = None

        self.update_current_node()

        # ==========================================================
        # MOVIMIENTO
        # ==========================================================

        self.move_timer = 0.0
        self.move_interval = 5.0

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

    def get_office_sprite(self):
        return self.office_sprite

    def get_size(self):
        return self.current_size

    def get_position(self):
        return (
            self.current_x,
            self.current_y
        )

    def get_x(self):
        return self.current_x

    def get_y(self):
        return self.current_y

    # ==========================================================
    # ESTADO
    # ==========================================================

    def is_attacking(self):
        return self.attacking

    def is_blackout(self):
        return self.blackout

    def is_jumpscaring(self):
        return self.jumpscaring

    # ==========================================================
    # AI
    # ==========================================================

    def set_ai(self, new_ai):

        self.__ai = max(
            0,
            min(new_ai, self.max_ai)
        )

    def add_ai(self, value):

        self.set_ai(
            self.__ai + value
        )

    def minus_ai(self, value):

        self.set_ai(
            self.__ai - value
        )

    # ==========================================================
    # TIMER
    # ==========================================================

    def get_move_interval(self):
        return self.move_interval

    def set_move_interval(self, seconds):

        self.move_interval = seconds

    def get_move_timer(self):
        return self.move_timer

    def set_move_timer(self, seconds):

        self.move_timer = max(
            0.0,
            seconds
        )

    def reset_move_timer(self):

        self.move_timer = 0.0

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(self, delta_time):

        # No puede seguir moviéndose durante un ataque
        if self.attacking:
            return

        self.move_timer += delta_time

        if self.move_timer >= self.move_interval:

            self.move_timer = 0.0

            self.roll_movement_opportunity()

    # ==========================================================
    # OPORTUNIDAD DE MOVIMIENTO
    # ==========================================================

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

    # ==========================================================
    # MOVIMIENTO
    # ==========================================================

    def move(self):

        if not self.path:
            return

        if self.path_index >= len(self.path) - 1:
            return

        self.path_index += 1

        self.update_current_node()

        print(
            f"[{self.__nombre}] -> "
            f"{self.current_cam}"
        )

        # ======================================================
        # OFFICE
        # ======================================================

        if self.is_office():

            self.attack()

    # ==========================================================
    # NODO ACTUAL
    # ==========================================================

    def update_current_node(self):

        if not self.path:
            return

        node = self.path[
            self.path_index
        ]

        # ------------------------------------------------------
        # CAM
        # ------------------------------------------------------

        self.current_cam = node.get(
            "cam"
        )

        # ------------------------------------------------------
        # DATOS DE CÁMARA
        # ------------------------------------------------------

        self.current_sprite = node.get(
            "spritepath"
        )

        self.current_size = node.get(
            "size"
        )

        self.current_x = node.get(
            "x"
        )

        self.current_y = node.get(
            "y"
        )

        # ------------------------------------------------------
        # SPRITE DE OFICINA
        # ------------------------------------------------------

        self.office_sprite = node.get(
            "office_sprite"
        )

    # ==========================================================
    # TIPOS DE NODO
    # ==========================================================

    def is_camera(self):

        return isinstance(
            self.current_cam,
            int
        )

    def is_door(self):

        return self.current_cam in (
            "door_left",
            "door_right"
        )

    def is_wait_room(self):

        return self.current_cam == "wait_room"

    def is_office(self):

        return self.current_cam == "office"

    # ==========================================================
    # ATAQUE
    # ==========================================================

    def attack(self):

        if self.attacking:
            return None

        if not self.is_office():
            return None

        self.attacking = True

        self.blackout = False
        self.jumpscaring = False

        print(
            f"[{self.__nombre}] "
            f"ha llegado a la oficina."
        )

        # ======================================================
        # IGNOREMASK
        # ======================================================

        if self.ignoremask:

            self.jumpscaring = True

            print(
                f"[{self.__nombre}] "
                f"ignoremask=True -> JUMPSCARE"
            )

            return {
                "type": "jumpscare",
                "animatronic": self,
                "sound": self.get_jumpscare_sound(),
                "animation": self.get_jumpscare_animation()
            }

        # ======================================================
        # BLACKOUT
        # ======================================================

        self.blackout = True

        print(
            f"[{self.__nombre}] "
            f"ignoremask=False -> BLACKOUT"
        )

        return {
            "type": "blackout",
            "animatronic": self
        }

    # ==========================================================
    # JUMPSCARE
    # ==========================================================

    def get_jumpscare_sound(self):

        if not self.jumpscare:
            return None

        if len(self.jumpscare) < 1:
            return None

        return self.jumpscare[0]

    def get_jumpscare_animation(self):

        if not self.jumpscare:
            return None

        if len(self.jumpscare) < 2:
            return None

        return self.jumpscare[1]

    # ==========================================================
    # EVITAR ATAQUE
    # ==========================================================

    def avoid_attack(self):

        if not self.attacking:
            return

        print(
            f"[{self.__nombre}] "
            f"ataque evitado."
        )

        self.attacking = False
        self.blackout = False
        self.jumpscaring = False

        self.reset_position()

    # ==========================================================
    # TERMINAR JUMPSCARE
    # ==========================================================

    def finish_jumpscare(self):

        if not self.jumpscaring:
            return

        self.jumpscaring = False

        print(
            f"[{self.__nombre}] "
            f"jumpscare terminado."
        )

    # ==========================================================
    # RESET
    # ==========================================================

    def reset_position(self):

        if not self.path:
            return

        self.path_index = 0

        self.attacking = False
        self.blackout = False
        self.jumpscaring = False

        self.move_timer = 0.0

        self.update_current_node()

        self.needs_refresh = True

        print(
            f"[{self.__nombre}] "
            f"ha vuelto a su posición inicial."
        )