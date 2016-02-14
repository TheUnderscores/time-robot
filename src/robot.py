from entity import Entity
from frozen import Frozen
from point import Point
from exitdoor import ExitDoor
from wall import Wall
from level import Level
from button import Button
import robot_funcs

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
            },
            'step': step_number,
            'position': self.position(self.level),
            'level': self.level,
            'state': self.state,
            'move_up': robot_funcs.move_up, #TODO: dont do this manually
            'move_down': robot_funcs.move_down,
            'move_left': robot_funcs.move_left,
            'move_right':robot_funcs.move_right,
            'reverse_time': robot_funcs.reverse_time,
            'set_time': robot_funcs.set_time,
            'Point': Point,
            'Entity': Entity,
            'ExitDoor': ExitDoor,
            'Button': Button,
            'Robot': Robot,
            'Wall': Wall,
            'Level': Level,            
        }
        
        #*drumroll*
        exec(self.code_string,namespace) #NOT secure, can still access os
        #Tah-dah!
        
        gov = namespace.get('governor',{})
        action = gov.get('action',None)
        amount = gov.get('time_tick',None)

        return action,amount
