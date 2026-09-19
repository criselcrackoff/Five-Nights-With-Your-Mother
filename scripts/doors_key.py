from engine.scripts import Script
import pygame

class Doors(Script):
    def __init__(self, game):
        super().__init__(game)
        for image in self.game.images:
            if image.get_id() == "LeftButton":
                self.left = image
            elif image.get_id() == "RightButton":
                self.right = image
    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                self.game.toggle_door(self.left)
            if event.key == pygame.K_c:
                self.game.toggle_door(self.right)