from engine.scripts import Script
from data.sounds import *
import pygame


class CameraScript(Script):

    def __init__(self, game):
        super().__init__(game)

        self.open = False
        self.camera = 1
        self.trigger_height = 40
        self.cameranimation = self.game.monitor
        self.waiting_animation = False
        # Evita que se dispare varias veces mientras el cursor sigue dentro
        self.mouse_in_trigger = False
        # Consigue el id de las puertas
        for image in self.game.images:
            if image.get_id() == "LeftButton":
                self.left = image
            elif image.get_id() == "RightButton":
                self.right = image
    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.toggle()

    def update(self, dt):

        mouse = (self.game.mouse_x, self.game.mouse_y)

        camera_zone = pygame.Rect(
            0,
            self.game.HEIGHT - self.trigger_height,
            self.game.WIDTH,
            self.trigger_height
        )

        inside = camera_zone.collidepoint(mouse)

        # El cursor acaba de entrar
        if inside and not self.mouse_in_trigger:
            self.mouse_in_trigger = True
            self.toggle()

        # El cursor salió, listo para el próximo toggle
        elif not inside:
            self.mouse_in_trigger = False

        if self.waiting_animation and self.cameranimation.is_finished():
            if self.open:
                self.left.set_y(990)
                self.right.set_y(990)
            self.waiting_animation = False
            self.cameranimation.set_alpha(0)
    def toggle(self):
        self.game.mixer.play(
                        Tablet,
                        volume=0.2,
                        channel=self.game.CHANNEL_DOOR
                    )
        if self.open:
            self.close_camera()
        else:
            self.open_camera()
        print(self.open)
    def open_camera(self):

        self.open = True
        self.game.camera_open = True
        self.game.usage += 1
        self.waiting_animation = True
        self.cameranimation.set_alpha(255)
        self.cameranimation.play()
    def close_camera(self):

        self.open = False
        self.game.camera_open = False
        self.game.usage -= 1
        self.waiting_animation = True
        self.left.set_y(390)
        self.right.set_y(390)
        self.cameranimation.set_alpha(255)
        self.cameranimation.play(reverse=True)