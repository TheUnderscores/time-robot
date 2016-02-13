class Level:
    def __init__(self,ent_field=None,width=10,height=10):
        """Create a new level, optionally with an initial field of entities to start with. Requires either a field or dimensions"""
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
