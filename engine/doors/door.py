from ..animation import Animation

class Door:

    def __init__(self, image, button):
        self.image = image
        self.button = button
        self.closed = False

    def open(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def toggle(self):
        if self.closed:
            self.open()
        else:
            self.close()