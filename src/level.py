from point import Point
from entity import Entity

class Level:
    def __init__(self,ent_field=None,width=20,height=20):
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
        self.height = len(self.ent_field)
        self.width  = len(self.ent_field[0])

    def cells(self):
        """Iterate over each cell in the level, get a position and list of things in that cell"""
        for y,row in enumerate(self.ent_field):
            for x,cell in enumerate(row):
                yield Point(x,y), cell
    
    def get(self,point):
        """Returns a LIST (not a single) of entities at the given point"""
        return self.ent_field[point.y][point.x]

    def is_empty(self,point):
        """Returns true if there is nothing at point"""
        return not self.get(point)

    def add(self,ent,point):
        """Adds an entity to the field at position point"""
        if ent is None:
            raise Exception("ent can't be None you dummy")
        print("adding entity at",point.x,point.y) #debug
        self.ent_field[point.y][point.x].append(ent)
        if len(self.get(point)) > 10: #DEBUG
            raise Exception("AAH TOO MANY ROBOTS") #DEBUG

    def move(self, ent, to_point):
        """Moves an entity from wherever it is to to_point"""
        for point, cell in self.cells():
            if ent in cell:
                cell.remove(ent)
                self.add(ent,to_point)
                return

    def remove(self,ent,point):
        """Delete ent from point"""
        self.get(point).remove(ent)

    def entities(self, typ=Entity):
        """Get all entities from the field, optionally constrain to a certain type"""
        for pos, ent in self.entities_pos(typ):
            yield ent

    def entities_pos(self, typ=Entity):
        """
        Get all the entities and their position
        """
        for pos,cell in self.cells():
            for ent in cell:
                if isinstance(ent, typ):
                    yield pos, ent

    def destroy(self,point):
        """Destroys all entities at point"""
        self.ent_field[point.y][point.x] = []

    def spot_has(self,point,typ):
        """Test if there is an entity of typ at point"""
        for ent in self.get(point):
            if isinstance(ent,typ):
                return True
        return False

    def move_at(self,typ,fpoint,tpoint):
        """Moves an entity of typ from fpoint to tpoint"""
        cell = self.get(fpoint)
        filtered = []
        for ent in cell:
            if isinstance(ent,typ):
                filtered.append(cell)
        if len(filtered) > 1:
            raise Exception("Trying to move more than one robot")
