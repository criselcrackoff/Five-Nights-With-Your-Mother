from engine.scripts import Script
from scripts.cameras import CameraScript
from data.sounds import *
import pygame


class MaskScript(Script):

    def __init__(self, game):
        super().__init__(game)

        self.open = False
        self.ismaskopen = self.game.ismaskopen
        self.maskanimation = self.game.mask
        self.waiting_animation = False

        self.mouse_in_trigger = False
        self.trigger_padding = 10

        self.button = self.game.get_image("MaskBar")

    def event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                self.toggle()

    def update(self, dt):

        mouse = (self.game.mouse_x, self.game.mouse_y)
        ui = self.game.UI_SCALE
        mask_zone = pygame.Rect(
            int(self.button.get_x() * ui) - self.trigger_padding,
            int(self.button.get_y() * ui) - self.trigger_padding,
            self.button.get_surface_width() + self.trigger_padding * 2,
            self.button.get_surface_height() + self.trigger_padding * 2
            )


        inside = mask_zone.collidepoint(mouse)

        if inside and not self.mouse_in_trigger:
            self.mouse_in_trigger = True
            self.toggle()

        elif not inside:
            self.mouse_in_trigger = False

        if self.waiting_animation and self.maskanimation.is_finished():

            if self.open:

                self.game.mixer.play(
                    Mask_Breathing,
                    volume=0.2,
                    channel=self.game.CHANNEL_MASK,
                    looping=True
                )

            else:

                self.game.mixer.stop(
                    self.game.CHANNEL_MASK
                )

                self.maskanimation.set_alpha(0)

            self.waiting_animation = False

    def toggle(self):

        if self.waiting_animation:
            return

        camera = self.game.get_script("CameraScript")

        if camera:

            if camera.waiting_animation:
                return

            if camera.open:
                # camera.close_camera()
                return None

        if self.open:
            self.close_mask()
        else:
            self.open_mask()

    def open_mask(self):

        self.open = True
        self.game.ismaskopen = True
        self.waiting_animation = True

        self.maskanimation.set_alpha(255)

        self.game.mixer.play(
            Mask_Open,
            volume=0.2,
            channel=self.game.CHANNEL_SFX
        )

        self.maskanimation.play()

    def close_mask(self):

        self.open = False
        self.game.ismaskopen = False
        self.waiting_animation = True

        self.game.mixer.play(
            Mask_Close,
            volume=0.2,
            channel=self.game.CHANNEL_SFX
        )

        self.maskanimation.play(reverse=True)