from entity import Entity

class Button(Entity):
    def __init__(self, level):
        super().__init__(level)
        self.pressed = False

    def press(self):
        self.pressed = True

    def depress(self):
        self.pressed = False
