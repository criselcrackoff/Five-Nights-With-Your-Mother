from .door import Door

class StaticDoor(Door):

    def open(self):

        self.closed = False

        self.image.set_alpha(0)
        self.image.set_subid("open")

        self.button.set_subid("off")
        self.button.change_image(
            "./assets/sprites/Mechanics/Buttons/Doors-Button.png"
        )

    def close(self):

        self.closed = True

        self.image.set_alpha(255)
        self.image.set_subid("closed")

        self.button.set_subid("on")
        self.button.change_image(
            "./assets/sprites/Mechanics/Buttons/Doors-Button-On.png"
        )