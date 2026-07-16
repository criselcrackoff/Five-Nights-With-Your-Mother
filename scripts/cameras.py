from engine.scripts import Script
import pygame


class CameraScript(Script):

    def __init__(self, game):
        super().__init__(game)

        self.open = False
        self.camera = 1
        self.trigger_height = 40
        self.cameranimation = self.game.monitor
    def event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                self.toggle()

    def update(self, dt):

        mouse = (self.game.mouse_x, self.game.mouse_y)
        
        camera_zone = pygame.Rect(
            0,
            self.game.HEIGHT - self.trigger_height,
            self.game.WIDTH,
            self.trigger_height
        )

        if camera_zone.collidepoint(mouse):

            if not self.open:
                self.open_camera()

        else:

            if self.open:
                self.close_camera()
        
        print(self.open)
    def toggle(self):

        if self.open:
            self.close_camera()
    
        else:
            self.open_camera()
    

    def open_camera(self):

        self.open = True
        self.game.camera_open = True
        self.cameranimation.set_alpha(255)
        self.cameranimation.restart()

    def close_camera(self):

        self.open = False
        self.game.camera_open = False