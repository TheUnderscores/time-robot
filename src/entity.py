class Entity:
    def __init__(self,level=None):
        """Creates a new entity. If level is not specified, some functions (such as position) may not work"""
        self.__level = level

    def position(self):
        """Gets the entity's current position as a Point"""
        pass
    
