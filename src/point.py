class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, oth):
        """ Returns a new point containing the addition of the coordinates of a & b """
        return Point(self.x+oth.x,self.y+oth.y)

    def __iadd__(self, oth):
        self.x += oth.x
        self.y += oth.y
