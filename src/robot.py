from entity import Entity

class Robot(Entity):
    def __init__(self,code_thing,state=None):
        """
        Makes a new robot with whatever niko uses 
        for the lua code runner thingy as well as a 
        state which possibly is included in the 
        code_thing
        """
        pass

    def run(self,level,step_number):
        """
        Run this robot's code, return the action and amount
        in that order
        """
        pass
