class Timeline:
    def __init__(self,init_level):
        """Initializes the Timeline with a starting level, IE the puzzle. Should have exactly 1 robot entity in it"""
        self.states = [init_level]

    def __len__(self): #PYTHON IS DUMB
        len(self.states)

    def previous_state(self,how_far_back):
        """Goes to a "previous state" so to speak of the timeline.
        Grabs the states from 0 (start) to how_far_back and puts them in a new timeline"""
        new_t = Timeline(self.states[0])
        if how_far_back > 0:
            for st in self.states[1:how_far_back]:
                new_t.add_state(st)
            return new_t
        else:
            raise Exception("cant go back to -1")    

    def add_state(self,state):
        """Adds a state to the end of the timeline. Should only be added once the state is FINALIZED"""
        self.states.append(state)
