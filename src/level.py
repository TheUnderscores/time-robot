import Point from point

class Level:
    def __init__(self,ent_field=None,width=10,height=10):
        """Create a new level, optionally with an initial field of entities to start with. Requires either a field or dimensions"""
        if ent_field is None:
            self.ent_field = []
            for i in range(height):
                row = []
                self.ent_field.append(row)
                for j in range(width):
                    row.append([])
        else:
            self.ent_field = ent_field                    
        pass

    def cells(self):
        """Iterate over each cell in the level, get a position and list of things in that cell"""
        for y,row in enumerate(self.ent_field):
            for x,cell in enumerate(row):
                yield Point.new(x,y), cell
    
    def get(self,point):
        """Returns a LIST (not a single) of entities at the given point"""
        return self.ent_field[self.y][self.x]

    def empty(self,point):
        """Returns true if there is nothing at point"""
        return not self.get(point)

    def add(self,ent,point):
        """Adds an entity to the field at position point"""
        self.ent_field[point.y][point.x]

    def move(self, ent, to_point):
        """Moves an entity from wherever it is to to_point"""
        for point, cell in self.cells():
            for i, ent in enumerate(cell):
                if ent in cell:
                    self.add(cell.delete(ent),to_point)
                    return
                

    def destroy(self,point):
        """Destroys all entities at point"""
        self.ent_field[self.y][self.x] = []
