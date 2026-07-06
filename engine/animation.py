import os
import pygame
from .images import Images
class Animation(Images):

    def __init__(
        self,
        id,
        folder,
        trigger,
        alpha,
        x,
        y,
        width,
        height,
        scale,
        fullscreen=False,
        subid=None,
        fps=12,
        loop=True
    ):

        self.frames = []

        # Cargar todos los frames
        files = sorted(os.listdir(folder))

        for file in files:
            if file.endswith(".png"):
                self.frames.append(
                    pygame.image.load(
                        os.path.join(folder, file)
                    ).convert_alpha()
                )

        if len(self.frames) == 0:
            raise Exception(f"No animation frames found in {folder}")

        super().__init__(
            id=id,
            scr=self.frames[0],
            trigeable=trigger,
            alpha_cn=alpha,
            xPos=x,
            yPos=y,
            width=width,
            height=height,
            ui_scale=scale,
            isBG=fullscreen,
            sub_id=subid
        )

        self.current_frame = 0

        self.animation_speed = fps
        self.loop = loop

        self.playing = True

        self.timer = 0
    
    def update(self, delta_time):

        if not self.playing:
            return

        self.timer += delta_time

        if self.timer >= 1 / self.animation_speed:

            self.timer = 0

            self.current_frame += 1

            if self.current_frame >= len(self.frames):

                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.playing = False

            self.change_surface(self.frames[self.current_frame])
    
    def play(self):
        self.playing = True


    def stop(self):
        self.playing = False


    def restart(self):
        self.current_frame = 0
        self.timer = 0
        self.playing = True
        self.change_surface(self.frames[0])


    def set_frame(self, frame):

        frame = max(0, min(frame, len(self.frames)-1))

        self.current_frame = frame
        self.change_surface(self.frames[frame])