import Point from point

class Level:
    def __init__(self,ent_field=None,width=10,height=10):
        """Create a new level, optionally with an initial field of entities to start with. Requires either a field or dimensions"""
        if ent_field is None:
            self.ent_field = []
            for i in range(width):
                row = []
                self.ent_field.append(row)
                for j in range(height):
                    row.append([])
        else:
            self.ent_field = ent_field                    
        pass

    def cells(self):
        """Iterate over each cell in the level, get a position and list of things in that cell"""
        for i,row in enumerate(self.ent_field):
            for j,cell in enumerate(row):
                yield Point.new(i,j)
        pass
    
    def get(self,point):
        """Returns a LIST (not a single) of entities at the given point"""
        pass

    def add(self,ent,point):
        """Adds an entity to the field at position point"""
        pass

    def move(self,from_point, to_point):
        """Moves an entity from one position to another"""
        pass

    def destroy(self,point):
        """Destroys an entity at point"""
        pass
