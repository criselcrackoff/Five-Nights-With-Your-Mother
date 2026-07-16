from engine.scripts import Script
import pygame
class PowerScript(Script):

    def __init__(self, game):
        super().__init__(game)
        self.power = 100
        self.power_images = {
            i: pygame.image.load(
                f"./assets/sprites/Mechanics/PowerUsage/power_usage_progression_{i}.png"
            ).convert_alpha()
            for i in range(1, 7)
        }

    def update(self, dt):

        self.game.usage = max(1, min(6, self.game.usage))
        usage = self.game.usage
        progress = self.game.get_image("PowerProgress")
        self.power -= dt * (usage / 10)
        if self.power <= 0:
            self.game.blackout = True
            self.power = 0
        if self.power < 10:
            if int(self.game.texts[3].get_x()) != 82:
                self.game.texts[3].set_x(82)
                try:
                    self.game.texts[4].set_x(106)
                except:
                    pass
            else:
                pass
        else:
            if int(self.game.texts[3].get_x()) != 67:
                self.game.texts[3].set_x(67)
                try:
                    self.game.texts[4].set_x(111)
                except:
                    pass
            else:
                pass
        progress.change_image(f"./assets/sprites/Mechanics/PowerUsage/power_usage_progression_{usage}.png")
        self.game.texts[3].set_text(str(int(self.power)))