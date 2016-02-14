class EntityNotFound(BaseException):
    pass
    
class Entity:
    def __init__(self,level=None):
        """Creates a new entity. If level is not specified, some functions (such as position) may not work"""
        #self.__level = level

    def position(self,level):
        """Gets the entity's current position as a Point"""
        for pos,cell in level.cells():#self.__level.cells():
            if self in cell:
                return pos
        raise EntityNotFound("Wasn't able to find position of Entity in level")
