from engine.scripts import Script
from data.sounds import *
import pygame


class CameraScript(Script):

    def __init__(self, game):
        super().__init__(game)

        self.open = False
        self.camera = 1

        self.cameranimation = self.game.monitor
        self.waiting_animation = False

        self.mouse_in_trigger = False
        self.trigger_padding = 20

        self.button = self.game.get_image("CameraBar")

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
            self.button.get_x() - self.trigger_padding,
            self.button.get_y() - self.trigger_padding,
            self.button.get_surface_width() + self.trigger_padding * 2,
            self.button.get_surface_height() + self.trigger_padding * 2
        )

        inside = camera_zone.collidepoint(mouse)

        if inside and not self.mouse_in_trigger:
            self.mouse_in_trigger = True
            self.toggle()

        elif not inside:
            self.mouse_in_trigger = False

        if self.waiting_animation and self.cameranimation.is_finished():

            if self.open:

                self.left.set_y(990)
                self.right.set_y(990)

            self.waiting_animation = False
            self.cameranimation.set_alpha(0)

    def toggle(self):

        if self.waiting_animation:
            return

        mask = self.game.get_script("MaskScript")

        if mask:

            if mask.waiting_animation:
                return

            if mask.open:
                mask.close_mask()

        self.game.mixer.play(
            Tablet,
            volume=0.2,
            channel=self.game.CHANNEL_SFX
        )

        if self.open:
            self.close_camera()
        else:
            self.open_camera()

    def open_camera(self):

        self.open = True
        self.game.ismonitoropen = True
        self.game.usage += 1

        self.waiting_animation = True

        self.cameranimation.set_alpha(255)
        self.cameranimation.play()

    def close_camera(self):

        self.open = False
        self.game.ismonitoropen = False
        self.game.usage -= 1

        self.waiting_animation = True

        self.left.set_y(390)
        self.right.set_y(390)

        self.cameranimation.set_alpha(255)
        self.cameranimation.play(reverse=True)