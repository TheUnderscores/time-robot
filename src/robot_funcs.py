def move_up(robot):
        global governor
        governor.action = 'up'

def move_down(robot):
        global governor
        governor.action = 'down'

def move_left(robot):
        global governor
        governor.action = 'left'

def move_right(robot):
        global governor
        governor.action = 'right'

def reverse_time(ticks):
        global governor
        governor.action = 'time'
        governor.time_tick = current_tick - ticks

def set_time(tick):
        global governor
        governor.action = 'time'
        governor.time_tick = tick
