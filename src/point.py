class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, a, b):
        """ Returns a new point containing the addition of the coordinates of a & b """
        return Point(a.x+b.x,a.y+b.y)

    def __sub__(self, i):
        return Point(self.x-i.x, self.y-i.y)

    def __mul__(self, i):
        if isinstance(i, Point):
            return Point(self.x*i.x, self.y*i.y)
        else:
            return Point(self.x*i, self.y*i)

    def __truediv__(self, i):
        if isinstance(i, Point):
            return Point(self.x/i.x, self.y/i.y)
        else:
            return Point(self.x/i, self.y/i)

    def __floordiv__(self, i):
        if isinstance(i, Point):
            return Point(self.x//i.x, self.y//i.y)
        else:
            return Point(self.x//i, self.y//i)
