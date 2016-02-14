#Does not implement fallthrough

class Switch():
    def __init__(self,value):
        self.value = value

    def __iter__(self):
        yield self.match

    def match(self,*args):
        return self.value in args

#Use like:
#for case in Switch(val):
#    if case(3):
#        doStuff()
#    if case(4):
#        doOtherStuff()
    
    
