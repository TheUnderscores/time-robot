from entity import Entity
from freeze import Freeze
import clone
import robot-funs

class Robot(Entity):
    def __init__(self,level,code_string):
        """
        Makes a new robot with whatever niko uses 
        for the lua code runner thingy as well as a 
        state which possibly is included in the 
        code_thing
        """
        super().__init__(level)
        self.code_string = code_string
        self.state = {}
        self.level = level
        self.master = True

    def run(self,step_number):
        """
        Run this robot's code, return the action and amount
        in that order
        """
        namespace = {
            'governor':{
                'action': None,
                'time_tick': None
            }
            'position': Freeze(self.position()),
            'level': Freeze(self.level),
            'state': self.state
        }

        namespace.update(robot-funs) #add helper funcs to namespace
        
        #*drumroll*
        eval(codestring,namespace) #NOT secure, can still access os
        #Tah-dah!

        gov = namespace.get('governor',{})
        action = gov.get('action',None)
        amount = gov.get('time_tick',None)

        return action,amount
