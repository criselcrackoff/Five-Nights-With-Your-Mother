from engine.scripts import Script
class PowerScript(Script):

    def __init__(self, game):
        super().__init__(game)
        self.power = 100

    def update(self, dt):

        self.power -= dt * 3
        if self.power <= 0:
            self.game.blackout = True
            self.power = 0
        if self.power < 10:
            if int(self.game.texts[3].get_x()) != 82:
                self.game.texts[3].set_x(82)
                self.game.texts[4].set_x(106)
            else:
                pass
        else:
            if int(self.game.texts[3].get_x()) != 67:
                self.game.texts[3].set_x(67)
                self.game.texts[4].set_x(111)
            else:
                pass
        self.game.texts[3].set_text(str(int(self.power)))