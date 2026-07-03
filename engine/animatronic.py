import random


class Animatronic:

    def __init__(self, id: int, nombre: str, ai: int, max_ai: int = 20):

        self.__id = id
        self.__nombre = nombre

        self.max_ai = max(20, max_ai)

        self.__ai = max(
            0,
            min(ai, self.max_ai)
        )

        self.move_timer = 0.0
        self.move_interval = 4.0

    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_ai(self):
        return self.__ai

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

        # Dead zone:
        # AI 20 -> roll 20 fails.
        # AI 40 -> roll 40 fails.
        if roll < self.__ai:
            self.move()

    def move(self):
        print(f"{self.__nombre} moved!")