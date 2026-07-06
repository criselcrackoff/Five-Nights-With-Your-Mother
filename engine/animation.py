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
        loop=True,
        size=None
    ):

        self.frames = []

        files = sorted(os.listdir(folder))

        for file in files:

            if not file.endswith(".png"):
                continue

            frame = pygame.image.load(
                os.path.join(folder, file)
            ).convert_alpha()

            if size is not None:
                frame = pygame.transform.smoothscale(
                    frame,
                    size
                )

            self.frames.append(frame)

        if len(self.frames) == 0:
            raise Exception(
                f"No animation frames found in '{folder}'."
            )

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

        frame_time = 1 / self.animation_speed

        self.timer += delta_time

        while self.timer >= frame_time:

            self.timer -= frame_time

            self.current_frame += 1

            if self.current_frame >= len(self.frames):

                if self.loop:
                    self.current_frame = 0

                else:
                    self.current_frame = len(self.frames) - 1
                    self.playing = False
                    break

        self.change_surface(
            self.frames[self.current_frame]
        )

    def play(self):
        self.playing = True

    def stop(self):
        self.playing = False

    def restart(self):
        self.current_frame = 0
        self.timer = 0
        self.playing = True
        self.change_surface(
            self.frames[0]
        )

    def set_frame(self, frame):

        frame = max(
            0,
            min(frame, len(self.frames) - 1)
        )

        self.current_frame = frame

        self.change_surface(
            self.frames[frame]
        )

    def get_frame(self):
        return self.current_frame

    def get_total_frames(self):
        return len(self.frames)

    def is_playing(self):
        return self.playing

    def is_finished(self):

        return (
            not self.loop
            and not self.playing
            and self.current_frame == len(self.frames) - 1
        )

    def set_fps(self, fps):
        self.animation_speed = fps