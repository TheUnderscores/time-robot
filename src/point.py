class Point:
    def __init__(x,y):
        self.x = x
        self.y = y

    def add(a, b):
        """ Returns a new point containing the addition of the coordinates of a & b """
        return Point(a.x+b.x,a.y+b.y)
