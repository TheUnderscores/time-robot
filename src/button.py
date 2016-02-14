from entity import Entity

class Button(Entity):
    def __init__(self):
        super().__init__()
        self.pressed = false

    def press(self):
        self.pressed = true

    def depress(self):
        self.pressed = false
