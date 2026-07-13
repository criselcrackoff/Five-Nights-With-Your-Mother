from engine.scripts import Script
class PowerScript(Script):

    def __init__(self, game):
        super().__init__(game)
        self.power = 100

    def update(self, dt):

        self.power -= dt * 0.3
        if self.power <= 0:
            self.game.blackout = True
            self.power = 0
        print(f"Energía: {int(self.power)}")