_events = {
    'quit' : False
}

def setEvent(e, b):
    """
    Sets an event to True or False.
    e -- event name; case insensitive
    b -- boolean value to set event to
    """
    e = e.lower()
    eventKeys = set(k.lower for k in _events)
    if not e in eventKeys:
        print("Error: no event named {}".format(e))
        return False
    else:
        _events[e] = b
    
def clearEvents():
    """
    Sets all events to false.
    """
    global _events
    for e in _events:
        _events[e] = False

def checkEvents():
    """
    Parses events and manipulate game accordingly.
    """
    pass

def startGameLoop():
    """
    Initiates the game loop. Will continue to run until the 'quit' event is set to True.
    """
    while not _events['quit']:
        checkEvents()
        clearEvents()
